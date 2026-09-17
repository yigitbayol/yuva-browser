"""Büyük indirme öncesi plan ve önkoşul kapısı; henüz kaynak hazırlamaz."""

from __future__ import annotations

from pathlib import Path

from .common import Parser, ROOT, ToolError, emit
from .environment import MINIMUM_FREE_GIB, inspect_environment, workspace_problem
from .metadata import load_patches, load_versions


def main(argv=None):
    parser = Parser(description="Chromium indirmeden önce kaynak planını ve ortam önkoşullarını göster.")
    parser.add_argument("--workspace", type=Path, default=ROOT.parent / "yuva-chromium", help="Depo dışında, boşluk içermeyen çalışma alanı.")
    parser.add_argument("--plan", action="store_true", help="Yalnız planı göster; sistem araçlarını çalıştırma.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Çıktı biçimi.")
    arguments = parser.parse_args(argv)
    report = {"summary": "Yuva kaynak hazırlama planı", "checks": [], "notes": [], "source_prepared": False}
    try:
        versions = load_versions()
        patches = load_patches(versions)
        problem = workspace_problem(arguments.workspace)
        if problem:
            raise ToolError(problem)
        report["plan"] = {
            "chromium_version": versions["chromium_version"], "chromium_revision": versions["chromium_revision"],
            "yuva_version": versions["yuva_version"], "patchset_version": versions["patchset_version"],
            "patch_count": len(patches), "workspace": str(arguments.workspace.expanduser().resolve()),
            "minimum_free_gib": MINIMUM_FREE_GIB, "downloads_enabled": False,
        }
        report["notes"] = [
            f"Chromium: {versions['chromium_version']} / {versions['chromium_revision']}",
            f"Hedef dizin: {report['plan']['workspace']}",
            f"Kaynak, bağımlılık ve çıktılar için yaklaşık 100–200 GB veya daha fazla alan gerekebilir; ilk indirme kapısı {MINIMUM_FREE_GIB} GiB boş alan ister.",
            "Bu sürüm yalnız plan/önkoşul denetimidir; hiçbir indirme, kurulum, hook veya yama uygulaması yapmaz.",
        ]
        if not arguments.plan:
            host = inspect_environment(arguments.workspace)
            report["checks"] = host["checks"]
            report["preflight_ready"] = host["preflight_ready"]
            report["checks"].append({"id": "source_preparation", "status": "blocked", "message": "Kaynak getirme, DEPS/araç kilidi ve derleme yapılandırması henüz uygulanmadı; hazırlık tamamlandı sayılmaz."})
    except ToolError as error:
        report["checks"].append({"id": "configuration", "status": "blocked", "message": str(error)})
    emit(report, arguments.format)
    return 1 if any(check["status"] == "blocked" for check in report["checks"]) else 0
