"""Sabit kaynağı ve yama uyumunu indirme/checkout yapmadan denetler."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from .common import Parser, ROOT, ToolError, emit, run_command
from .environment import workspace_problem
from .metadata import load_patches, load_versions, matches, unique_object

SOURCE_BASE = "https://chromium.googlesource.com/chromium/src"
TOOLS_BASE = "https://chromium.googlesource.com/chromium/tools/depot_tools"
RELEASE_URL = "https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Mac&num=1"
MAX_RESPONSE_BYTES = 4 * 1024 * 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Meta veri istemcisi başka bir uca yönlendirilemez."""

    def redirect_request(self, request, file, code, message, headers, new_url):
        raise ToolError("Meta veri uç noktası yönlendirme döndürdü; istek reddedildi.")


def fetch_bytes(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc not in {"chromiumdash.appspot.com", "chromium.googlesource.com"}:
        raise ToolError("Meta veri adresi izin verilen HTTPS kaynağı değil.")
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(url, timeout=15) as response:
            payload = response.read(MAX_RESPONSE_BYTES + 1)
        if len(payload) > MAX_RESPONSE_BYTES:
            raise ToolError("Upstream yanıtı boyut sınırını aşıyor.")
        return payload
    except (OSError, urllib.error.URLError, ValueError) as error:
        raise ToolError("Upstream meta verisi alınamadı; güvenlik veya ağ hatası gizlenmedi.") from error


def parse_json(payload, *, gitiles=False):
    if gitiles:
        if not payload.startswith(b")]}'\n"):
            raise ToolError("Gitiles meta veri öneki geçersiz.")
        payload = payload[5:]
    try:
        return json.loads(payload, object_pairs_hook=unique_object)
    except (ValueError, UnicodeError) as error:
        raise ToolError("Upstream meta verisi geçerli JSON değil.") from error


def read_release(release_platform, fetch, now):
    url = RELEASE_URL.replace("platform=Mac", f"platform={release_platform}")
    data = parse_json(fetch(url))
    if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], dict):
        raise ToolError("Stable kanal yanıtının yapısı beklenenden farklı.")
    release = data[0]
    hashes = release.get("hashes")
    if release.get("channel") != "Stable" or release.get("platform") != release_platform or not isinstance(hashes, dict):
        raise ToolError("Yanlış platform/kanal veya eksik kaynak kimliği alındı.")
    if not matches(release.get("version"), r"\d+\.\d+\.\d+\.\d+") or not matches(hashes.get("chromium"), r"[0-9a-f]{40}"):
        raise ToolError("Stable sürüm veya commit kimliği geçersiz.")
    timestamp = release.get("time")
    if type(timestamp) is not int or timestamp <= 0:
        raise ToolError("Stable yayın zamanı geçersiz.")
    age = now.timestamp() - timestamp / 1000
    if age < -86400 or age > 14 * 86400:
        raise ToolError("Stable verisinin zamanı güvenli aralıkta değil; saat/kaynak tekrar incelenmeli.")
    return release


def verify_network(versions, fetch=fetch_bytes, now=None):
    """Kaynak kimliği doğrulaması yayın imzası veya tam bağımlılık kilidi değildir."""
    now = now or datetime.now(timezone.utc)
    releases = [read_release(target, fetch, now) for target in ("Mac", "Windows", "Linux")]
    release = releases[0]
    hashes = release["hashes"]
    version = versions["chromium_version"]
    revision = versions["chromium_revision"]
    tag = parse_json(fetch(f"{SOURCE_BASE}/+/refs/tags/{version}?format=JSON"), gitiles=True)
    if not isinstance(tag, dict) or tag.get("commit") != revision:
        raise ToolError("Chromium etiketi sabitlenmiş commit ile eşleşmiyor.")
    try:
        deps = base64.b64decode(fetch(f"{SOURCE_BASE}/+/{revision}/DEPS?format=TEXT").strip(), validate=True)
    except ValueError as error:
        raise ToolError("DEPS aktarımı geçerli base64 değil.") from error
    if hashlib.sha256(deps).hexdigest() != versions["chromium_deps_sha256"]:
        raise ToolError("Chromium DEPS özeti beklenen değerle eşleşmiyor.")
    tool_revision = versions["depot_tools_revision"]
    tool = parse_json(fetch(f"{TOOLS_BASE}/+/{tool_revision}?format=JSON"), gitiles=True)
    if not isinstance(tool, dict) or tool.get("commit") != tool_revision:
        raise ToolError("depot_tools sabit revizyonu doğrulanamadı.")
    current = tuple(map(int, release["version"].split(".")))
    pinned = tuple(map(int, version.split(".")))
    if current < pinned or (current == pinned and hashes["chromium"] != revision):
        raise ToolError("Stable yanıtı gerileme veya aynı sürümde farklı commit gösteriyor.")
    return {
        "version": release["version"], "revision": hashes["chromium"],
        "update_available": any(tuple(map(int, item["version"].split("."))) > pinned for item in releases),
        "platform_releases": [{"platform": item["platform"], "version": item["version"], "revision": item["hashes"]["chromium"]} for item in releases],
    }


def check_patches(source_dir, revision, patches, root=ROOT):
    """Geçici Git indeksinde sıralı uygulama dener; checkout ve asıl indeks değişmez."""
    if not matches(revision, r"[0-9a-f]{40}"):
        raise ToolError("Hedef revizyon tam Git commit kimliği olmalıdır.")
    problem = workspace_problem(source_dir, root)
    if problem:
        raise ToolError(problem)
    source_dir = source_dir.resolve()
    top = run_command(["git", "rev-parse", "--show-toplevel"], cwd=source_dir)
    if not top or top.returncode or Path(top.stdout.strip()).resolve() != source_dir:
        raise ToolError("Kaynak dizini ayrı bir Git çalışma ağacının kökü olmalıdır.")
    origin = run_command(["git", "remote", "get-url", "origin"], cwd=source_dir)
    if not origin or origin.returncode or origin.stdout.strip().removesuffix(".git") != SOURCE_BASE:
        raise ToolError("Kaynak deposunun origin adresi beklenen Chromium kaynağı değil.")
    partial = run_command(["git", "config", "--get-regexp", r"remote\..*\.promisor"], cwd=source_dir)
    if partial is None or partial.returncode not in (0, 1) or (partial.returncode == 0 and partial.stdout.strip()):
        raise ToolError("Kısmi/promisor kaynakta örtük ağ erişimi riski var; tam yerel nesnelerle yeniden deneyin.")
    object_path = run_command(["git", "rev-parse", "--git-path", "objects"], cwd=source_dir)
    if not object_path or object_path.returncode:
        raise ToolError("Yerel Git nesne deposu belirlenemedi.")
    objects = Path(object_path.stdout.strip())
    if not objects.is_absolute():
        objects = source_dir / objects
    results = []
    with tempfile.TemporaryDirectory(prefix="yuva-patch-check-") as directory:
        environment = dict(os.environ)
        environment["GIT_INDEX_FILE"] = str(Path(directory) / "index")
        environment["GIT_NO_REPLACE_OBJECTS"] = "1"
        environment["GIT_NO_LAZY_FETCH"] = "1"
        # git apply --cached yeni blob yazar; onları da geçici dizinde tutarız.
        temporary_objects = Path(directory) / "objects"
        temporary_objects.mkdir()
        environment["GIT_OBJECT_DIRECTORY"] = str(temporary_objects)
        environment["GIT_ALTERNATE_OBJECT_DIRECTORIES"] = str(objects.resolve())
        base = run_command(["git", "read-tree", revision], cwd=source_dir, env=environment)
        if not base or base.returncode:
            raise ToolError("Hedef commit yerel kaynakta bulunamadı; araç otomatik fetch yapmaz.")
        for index, patch in enumerate(patches):
            result = run_command(
                ["git", "apply", "--cached", "--whitespace=error-all", str(root / patch["file"])],
                cwd=source_dir, env=environment,
            )
            applied = bool(result and result.returncode == 0)
            results.append({"id": patch["id"], "status": "applies" if applied else "conflict", "components": patch["components"]})
            if not applied:
                results.extend({"id": item["id"], "status": "not_checked", "components": item["components"]} for item in patches[index + 1:])
                break
    return results


def main(argv=None):
    parser = Parser(description="Sabit Chromium kaynağını, yeni sürümü ve yerel yama uyumunu denetle.")
    parser.add_argument("--network", action="store_true", help="Yalnız küçük resmî meta verileri al; kaynak indirme veya komut çalıştırma yapma.")
    parser.add_argument("--source-dir", type=Path, help="Önceden hazırlanmış, depo dışındaki Chromium src dizini.")
    parser.add_argument("--target-revision", help="Yerelde bulunan alternatif tam commit; yama denetimi içindir, kilidi değiştirmez.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Çıktı biçimi.")
    arguments = parser.parse_args(argv)
    if arguments.target_revision and not arguments.source_dir:
        parser.error("missing-source")
    report = {"summary": "Chromium kaynak ve yama denetimi", "checks": [], "notes": [], "patch_compatibility": "not_checked"}
    exit_code = 0
    try:
        versions = load_versions()
        patches = load_patches(versions)
        report["pinned_base"] = {"version": versions["chromium_version"], "revision": versions["chromium_revision"], "patchset_version": versions["patchset_version"]}
        report["checks"].append({"id": "metadata", "status": "pass", "message": f"Sabit Chromium {versions['chromium_version']}; yama kümesi {versions['patchset_version']}, {len(patches)} yama."})
        if arguments.network:
            report["available_base"] = verify_network(versions)
            update = report["available_base"]["update_available"]
            description = "; ".join(f"{item['platform']}: {item['version']}" for item in report["available_base"]["platform_releases"])
            report["checks"].append({"id": "upstream", "status": "warning" if update else "pass", "message": f"Resmî Stable kaynakları — {description}."})
            if update:
                exit_code = 3
                report["notes"].append("Yeni upstream sürümü var; yayın öncesinde kaynak kaydı ve güvenlik kapsamı incelenmelidir.")
        else:
            report["notes"].append("Ağ kullanılmadı; yeni sürüm ve uzak kaynak kimliği denetlenmedi. Bunun için --network kullanın.")
        if arguments.source_dir:
            revision = arguments.target_revision or versions["chromium_revision"]
            report["patch_target_revision"] = revision
            results = check_patches(arguments.source_dir, revision, patches)
            report["patch_results"] = results
            failed = any(item["status"] == "conflict" for item in results)
            report["patch_compatibility"] = "conflict" if failed else "applies" if patches else "empty_patchset"
            status_labels = {"applies": "uygulanabilir", "conflict": "çakışma", "not_checked": "önceki çakışma nedeniyle denenmedi"}
            for item in results:
                report["checks"].append({"id": item["id"], "status": "pass" if item["status"] == "applies" else "blocked", "message": f"{item['id']}: {status_labels[item['status']]}; bileşenler: {', '.join(item['components'])}."})
            if failed:
                exit_code = 1
        report["notes"].append("Kaynak başlangıcı henüz derlenmedi; DEPS alt grafiği, araç zinciri ve bütün platformlar nitelendirilmiş değildir.")
        if not patches:
            report["notes"].append("Yama kümesi boş; uygulanmış Yuva tarayıcı özelliği yoktur.")
    except ToolError as error:
        report["checks"].append({"id": "verification", "status": "blocked", "message": str(error)})
        exit_code = 1
    emit(report, arguments.format)
    return exit_code
