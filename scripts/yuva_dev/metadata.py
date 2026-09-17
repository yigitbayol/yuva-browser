"""Kaynak kimliklerini ve yama sırasını katı biçimde doğrular."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path, PurePosixPath

from .common import ROOT, ToolError

MAX_METADATA_BYTES = 1024 * 1024
VERSION_FIELDS = {
    "schema_version", "scope", "qualification", "yuva_version", "patchset_version",
    "chromium_version", "chromium_revision", "chromium_deps_sha256",
    "depot_tools_revision", "channel", "release_platform", "reviewed_on",
    "release_announcement",
}
PATCH_FIELDS = {
    "id", "file", "sha256", "purpose", "security_impact", "privacy_impact",
    "upstream_conflict_risk", "feature", "tests", "components", "depends_on",
    "owner", "backup_owner", "upstream_revision", "license", "source", "removal_condition",
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ToolError("JSON içinde yinelenen anahtar var.")
        result[key] = value
    return result


def read_json(path):
    try:
        with path.open("rb") as stream:
            data = stream.read(MAX_METADATA_BYTES + 1)
        if len(data) > MAX_METADATA_BYTES:
            raise ToolError("Meta veri boyut sınırını aşıyor.")
        return json.loads(data, object_pairs_hook=unique_object)
    except (OSError, ValueError, UnicodeError) as error:
        raise ToolError("Meta veri okunamadı veya geçerli JSON değil.") from error


def matches(value, pattern):
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


def load_versions(root=ROOT):
    data = read_json(root / "config/versions.json")
    if not isinstance(data, dict) or set(data) != VERSION_FIELDS:
        raise ToolError("Sürüm kaydının alanları beklenen şemayla eşleşmiyor.")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ToolError("Sürüm şeması desteklenmiyor.")
    if data["scope"] != "source_baseline" or data["qualification"] != "unbuilt":
        raise ToolError("Bu araç yalnız derlenmemiş kaynak başlangıç kaydını destekler.")
    if not matches(data["yuva_version"], r"\d+\.\d+\.\d+-dev"):
        raise ToolError("Yuva geliştirme sürümü geçersiz.")
    if not matches(data["chromium_version"], r"\d+\.\d+\.\d+\.\d+"):
        raise ToolError("Chromium sürümü dört sayısal bölüm içermelidir.")
    for key in ("chromium_revision", "depot_tools_revision"):
        if not matches(data[key], r"[0-9a-f]{40}"):
            raise ToolError("Kaynak revizyonu tam Git kimliği olmalıdır.")
    if not matches(data["chromium_deps_sha256"], r"[0-9a-f]{64}"):
        raise ToolError("DEPS özeti geçerli SHA-256 değil.")
    if type(data["patchset_version"]) is not int or data["patchset_version"] < 1:
        raise ToolError("Yama kümesi sürümü pozitif tam sayı olmalıdır.")
    if data["channel"] != "Stable" or data["release_platform"] != "Mac":
        raise ToolError("İlk kaynak başlangıcı Mac Stable kanalına bağlı olmalıdır.")
    try:
        date.fromisoformat(data["reviewed_on"])
    except (ValueError, TypeError) as error:
        raise ToolError("Kaynak inceleme tarihi geçersiz.") from error
    if not matches(data["release_announcement"], r"https://chromereleases\.googleblog\.com/\d{4}/\d{2}/[a-z0-9_-]+\.html"):
        raise ToolError("Yayın duyurusu beklenen resmî kaynağa ait değil.")
    return data


def safe_relative_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute() and ".." not in path.parts
        and str(path) == value and all(re.fullmatch(r"[A-Za-z0-9_.-]+", part) for part in path.parts)
    )


def load_patches(versions, root=ROOT):
    manifest = read_json(root / "patches/series.json")
    if not isinstance(manifest, dict) or set(manifest) != {"schema_version", "patchset_version", "patches"}:
        raise ToolError("Yama sırası şeması geçersiz.")
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise ToolError("Yama şeması desteklenmiyor.")
    if type(manifest["patchset_version"]) is not int or manifest["patchset_version"] != versions["patchset_version"]:
        raise ToolError("Yama ve kaynak sürümü kaydı tutarsız.")
    patches = manifest["patches"]
    if not isinstance(patches, list) or len(patches) > 1000:
        raise ToolError("Yama listesi geçersiz veya boyut sınırını aşıyor.")
    seen_ids, seen_paths = set(), set()
    for patch in patches:
        if not isinstance(patch, dict) or set(patch) != PATCH_FIELDS:
            raise ToolError("Yamanın gerekçe, etki veya test alanları eksik/fazla.")
        if not matches(patch["id"], r"[a-z][a-z0-9_-]{0,79}") or patch["id"] in seen_ids:
            raise ToolError("Yama kimliği geçersiz veya yineleniyor.")
        name = patch["file"]
        if not safe_relative_path(name) or not name.startswith("patches/") or not name.endswith(".patch") or name in seen_paths:
            raise ToolError("Yama yolu güvenli, benzersiz ve patches/ altında olmalıdır.")
        path = root / name
        cursor = root
        has_symlink = False
        for part in PurePosixPath(name).parts:
            cursor = cursor / part
            has_symlink = has_symlink or cursor.is_symlink()
        if not path.resolve().is_relative_to(root.resolve()) or has_symlink:
            raise ToolError("Yama yolu sembolik bağlantıyla yönlendirilemez.")
        try:
            with path.open("rb") as stream:
                payload = stream.read(4 * MAX_METADATA_BYTES + 1)
        except OSError as error:
            raise ToolError("Yama dosyası okunamadı.") from error
        if len(payload) > 4 * MAX_METADATA_BYTES or not matches(patch["sha256"], r"[0-9a-f]{64}") or hashlib.sha256(payload).hexdigest() != patch["sha256"]:
            raise ToolError("Yamanın boyutu veya SHA-256 özeti beklenen değerle eşleşmiyor.")
        for key in ("purpose", "security_impact", "privacy_impact", "feature", "owner", "backup_owner", "license", "source", "removal_condition"):
            if not isinstance(patch[key], str) or not patch[key].strip():
                raise ToolError("Yamanın etki/gerekçe metni boş olamaz.")
        if not matches(patch["upstream_revision"], r"[0-9a-f]{40}"):
            raise ToolError("Yamanın incelenmiş upstream revizyonu tam Git kimliği olmalıdır.")
        if patch["upstream_conflict_risk"] not in ("low", "medium", "high"):
            raise ToolError("Yamanın upstream çakışma riski geçersiz.")
        for key in ("tests", "components", "depends_on"):
            if not isinstance(patch[key], list) or not all(isinstance(item, str) and item for item in patch[key]):
                raise ToolError("Yamanın test, bileşen veya bağımlılık listesi geçersiz.")
        if not patch["tests"] or not patch["components"] or not all(safe_relative_path(item) for item in patch["components"]):
            raise ToolError("Yamanın testi ve güvenli bileşen yolları belirtilmelidir.")
        if not set(patch["depends_on"]).issubset(seen_ids):
            raise ToolError("Yama bağımlılığı daha önceki bir yamayı göstermelidir.")
        seen_ids.add(patch["id"])
        seen_paths.add(name)
    return patches
