"""Kaynak köklerini kilitler; çözülmemiş bağımlılıkları tam derleme saymaz."""

from __future__ import annotations

import hashlib

from .common import Parser, ROOT, ToolError, emit
from .metadata import load_patches, load_versions, read_json
from .upstream import SOURCE_BASE, TOOLS_BASE

PENDING_STAGES = [
    "dependency_graph", "cipd_instances", "gcs_objects", "hook_review",
    "toolchains", "patch_application", "build_configuration", "platform_builds",
]
TARGETS = [
    "windows-x86_64", "macos-arm64", "macos-x86_64", "linux-x86_64",
    "pardus-23-x86_64", "pardus-25-x86_64",
]


def file_digest(path):
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise ToolError("Kilit girdisinin özeti okunamadı.") from error


def expected_lock(versions, root=ROOT):
    """Şema 1 yalnız kök getirme yetkisi verir; sonraki aşamalar ayrı inceleme ister."""
    return {
        "schema_version": 1,
        "scope": "source_roots",
        "source_baseline_sha256": file_digest(root / "config/versions.json"),
        "patch_manifest_sha256": file_digest(root / "patches/series.json"),
        "roots": [
            {"id": "depot_tools", "directory": "depot_tools", "url": TOOLS_BASE,
             "revision": versions["depot_tools_revision"]},
            {"id": "chromium", "directory": "src", "url": SOURCE_BASE,
             "revision": versions["chromium_revision"]},
        ],
        "targets": TARGETS,
        "pending_stages": PENDING_STAGES,
    }


def load_lock(root=ROOT):
    versions = load_versions(root)
    load_patches(versions, root)
    data = read_json(root / "config/upstream.lock.json")
    # Eşitlik kaynak/yama bağlantısını, sabit URL/yolları ve çözülmemiş kapıları da denetler.
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data != expected_lock(versions, root):
        raise ToolError("Upstream kilidi kaynak/yama kaydı veya desteklenen kök şemasıyla eşleşmiyor; elle incelenerek yenilenmeli.")
    return data


def main(argv=None):
    parser = Parser(description="Kök kaynak kilidini doğrula; tam bağımlılık çözümünü ayrı raporla.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Çıktı biçimi.")
    arguments = parser.parse_args(argv)
    report = {"summary": "Upstream kök kilidi denetimi", "checks": [], "build_ready": False}
    try:
        data = load_lock()
        report["scope"] = data["scope"]
        report["pending_stages"] = data["pending_stages"]
        report["checks"].append({"id": "source_lock", "status": "pass", "message": "Kök revizyonlar, kaynak/yama özetleri ve ayrı Pardus hedefleri tutarlı."})
        report["notes"] = ["Bu başarı yalnız kök kilidi içindir; DEPS alt grafiği, CIPD/GCS, hook ve araç zinciri çözülmedi. Derleme hazır değildir."]
        status = 0
    except ToolError as error:
        report["checks"].append({"id": "source_lock", "status": "blocked", "message": str(error)})
        status = 1
    emit(report, arguments.format)
    return status
