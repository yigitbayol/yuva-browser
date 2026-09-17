"""Sabit iki Git kökünü dış alana getirir; indirilen kodu veya hook'u çalıştırmaz."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .common import ROOT, ToolError, run_command
from .environment import workspace_problem
from .lockfile import file_digest, load_lock
from .metadata import MAX_METADATA_BYTES, read_json

STATE_NAME = ".yuva-bootstrap.json"
LEASE_NAME = ".yuva-bootstrap.lock"
HOOKS_NAME = ".yuva-empty-hooks"


def isolated_environment():
    # Kullanıcının URL yeniden yazımı, özel filtreleri, credential helper'ı ve Git hook'ları alınmaz.
    environment = {key: value for key, value in os.environ.items() if not key.upper().startswith("GIT_")}
    environment.update({
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0", "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_NO_LAZY_FETCH": "1", "GIT_ATTR_NOSYSTEM": "1",
        "GIT_LFS_SKIP_SMUDGE": "1", "GIT_OPTIONAL_LOCKS": "0",
    })
    return environment


def git(directory, *arguments, timeout=120):
    hooks = directory.parent / HOOKS_NAME
    command = [
        "git", "-c", f"core.hooksPath={hooks}", "-c", "core.autocrlf=false",
        "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false",
        "-c", "submodule.recurse=false", "-c", "protocol.allow=never",
        "-c", "protocol.https.allow=always", "-c", "http.followRedirects=false",
        "-c", "fetch.fsckObjects=true", "-c", "transfer.fsckObjects=true",
        *arguments,
    ]
    result = run_command(command, cwd=directory, env=isolated_environment(), timeout=timeout)
    if result is None:
        raise ToolError("Git işlemi başlatılamadı veya süre sınırını aştı; kısmi kaynak tamamlandı sayılmadı.")
    if result.returncode:
        detail = result.stderr.strip()[-2000:]
        raise ToolError(f"Git işlemi başarısız (kod {result.returncode}): {detail}")
    return result.stdout.strip()


def fetch_commit(directory, url, revision):
    git(directory, "fetch", "--quiet", "--depth=1", "--no-tags", "--no-recurse-submodules", url, revision, timeout=1800)


def destination(workspace, root):
    problem = workspace_problem(workspace, root)
    if problem:
        raise ToolError(problem)
    absolute = workspace.expanduser().absolute()
    for path in (absolute, *absolute.parents):
        if path.is_symlink():
            raise ToolError("Kaynak hazırlama yolunda sembolik bağlantı kullanılamaz.")
    if not absolute.parent.is_dir():
        raise ToolError("Çalışma alanının üst dizini önceden var olmalıdır; üst dizinler otomatik oluşturulmaz.")
    return absolute


def write_state(workspace, state):
    destination_path = workspace / STATE_NAME
    if destination_path.is_symlink():
        raise ToolError("Hazırlama durumu sembolik bağlantı olamaz.")
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=workspace, prefix=".yuva-state-", delete=False) as stream:
            temporary_path = Path(stream.name)
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, destination_path)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


def verify_roots(workspace, lock, versions):
    heads = {}
    for entry in lock["roots"]:
        directory = workspace / entry["directory"]
        if directory.is_symlink() or not directory.is_dir() or not (directory / ".git").is_dir() or (directory / ".git").is_symlink():
            raise ToolError("Kaynak kökü gerçek, bağımsız Git dizini olmalıdır.")
        # Bu ilk aşamada yerel config yalnız aracın oluşturduğu origin kaydını taşır.
        config = git(directory, "config", "--local", "--list").splitlines()
        allowed = {"core.repositoryformatversion", "core.filemode", "core.bare", "core.logallrefupdates", "core.ignorecase", "core.precomposeunicode", "core.symlinks", "remote.origin.url"}
        if any(line.split("=", 1)[0] not in allowed for line in config):
            raise ToolError("Kaynakta beklenmeyen yerel Git yapılandırması var; otomatik kullanım durduruldu.")
        if git(directory, "remote", "get-url", "origin") != entry["url"]:
            raise ToolError("Kaynak origin adresi kilitle eşleşmiyor.")
        head = git(directory, "rev-parse", "--verify", "HEAD^{commit}")
        if head != entry["revision"]:
            raise ToolError("Kaynak HEAD revizyonu kilitle eşleşmiyor.")
        if git(directory, "status", "--porcelain", "--ignored", "--untracked-files=all"):
            raise ToolError("Kaynakta değişmiş, izlenmeyen veya yok sayılan dosya var; üzerine yazılmayacak.")
        heads[entry["id"]] = head
    deps_path = workspace / "src/DEPS"
    if deps_path.is_symlink() or not deps_path.is_file() or deps_path.stat().st_size > MAX_METADATA_BYTES:
        raise ToolError("Yerel DEPS dosyası geçersiz.")
    if file_digest(deps_path) != versions["chromium_deps_sha256"]:
        raise ToolError("Getirilen DEPS özeti sabit kaynak kaydıyla eşleşmiyor.")
    version_path = workspace / "src/chrome/VERSION"
    if (version_path.parent).is_symlink() or version_path.is_symlink() or not version_path.is_file() or version_path.stat().st_size > 1024:
        raise ToolError("Chromium VERSION dosyası geçersiz.")
    try:
        values = dict(line.split("=", 1) for line in version_path.read_text(encoding="utf-8").splitlines() if line)
        actual_version = ".".join(values[key] for key in ("MAJOR", "MINOR", "BUILD", "PATCH"))
    except (ValueError, KeyError, UnicodeError) as error:
        raise ToolError("Chromium VERSION içeriği çözümlenemedi.") from error
    if actual_version != versions["chromium_version"]:
        raise ToolError("Getirilen Chromium sürümü beklenen sürüm değil.")
    return heads


def prepare_roots(workspace, versions, root=ROOT):
    """Yeni alana getirir; tamamlanmış temiz alanda tekrar çağrı salt doğrulamadır."""
    lock = load_lock(root)
    lock_digest = file_digest(root / "config/upstream.lock.json")
    workspace = destination(workspace, root)
    created = False
    if not workspace.exists():
        workspace.mkdir(mode=0o700)
        created = True
    state_path = workspace / STATE_NAME
    lease_path = workspace / LEASE_NAME
    try:
        lease = os.open(lease_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise ToolError("Başka veya kesilmiş bir hazırlama işleminin kilidi var; otomatik devam edilmiyor.") from error
    os.close(lease)
    state = {"schema_version": 1, "phase": "fetching", "lock_sha256": lock_digest, "heads": {}}
    try:
        if not created:
            if state_path.is_symlink() or not state_path.is_file():
                raise ToolError("Mevcut çalışma alanı Yuva tarafından tamamlanmış değil; üzerine yazılmayacak.")
            previous = read_json(state_path)
            expected_heads = {entry["id"]: entry["revision"] for entry in lock["roots"]}
            if not isinstance(previous, dict) or type(previous.get("schema_version")) is not int or previous != dict(state, phase="roots_ready", heads=expected_heads):
                raise ToolError("Çalışma alanı eksik, farklı kilide ait veya başarısız durumda; veri korunuyor. Yeni bir dış dizin seçin.")
            hooks = workspace / HOOKS_NAME
            if hooks.is_symlink() or not hooks.is_dir() or any(hooks.iterdir()):
                raise ToolError("Yalıtılmış hook dizini boş ve gerçek bir dizin olmalıdır.")
            heads = verify_roots(workspace, lock, versions)
            return {"phase": "roots_ready", "reused": True, "heads": heads, "build_ready": False}
        write_state(workspace, state)
        hooks = workspace / HOOKS_NAME
        hooks.mkdir()
        try:
            for entry in lock["roots"]:
                directory = workspace / entry["directory"]
                directory.mkdir()
                git(directory, "init", "--quiet", f"--template={hooks}")
                git(directory, "remote", "add", "origin", entry["url"])
                # remote add refspec'i üretir; bu aşamada URL dışındaki uzak ayara ihtiyaç yoktur.
                git(directory, "config", "--unset-all", "remote.origin.fetch")
                fetch_commit(directory, entry["url"], entry["revision"])
                if git(directory, "rev-parse", "--verify", "FETCH_HEAD^{commit}") != entry["revision"]:
                    raise ToolError("Sunucudan gelen commit beklenen revizyon değil.")
                git(directory, "checkout", "--quiet", "--detach", entry["revision"], timeout=600)
            heads = verify_roots(workspace, lock, versions)
            if load_lock(root) != lock or file_digest(root / "config/upstream.lock.json") != lock_digest:
                raise ToolError("İşlem sırasında kaynak/yama kilidi değişti; başarı kaydı oluşturulmadı.")
            write_state(workspace, dict(state, phase="roots_ready", heads=heads))
        except BaseException:
            write_state(workspace, dict(state, phase="failed"))
            raise
        return {"phase": "roots_ready", "reused": False, "heads": heads, "build_ready": False}
    finally:
        lease_path.unlink()
