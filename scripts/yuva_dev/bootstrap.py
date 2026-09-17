"""Büyük indirme öncesi plan; açık seçenekle yalnız sabit kaynak köklerini hazırlar."""

from __future__ import annotations

import sys
from pathlib import Path

from .common import Parser, ROOT, ToolError, emit
from .environment import MINIMUM_FREE_GIB, inspect_environment, workspace_problem
from .lockfile import load_lock
from .metadata import load_patches, load_versions
from .sources import prepare_roots
from .upstream import verify_network


def main(argv=None):
    parser = Parser(description="Chromium indirmeden önce kaynak planını ve ortam önkoşullarını göster.")
    parser.add_argument("--workspace", type=Path, default=ROOT.parent / "yuva-chromium", help="Depo dışında, boşluk içermeyen çalışma alanı.")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--plan", action="store_true", help="Yalnız planı göster; sistem araçlarını çalıştırma.")
    action.add_argument("--fetch-roots", action="store_true", help="Önkoşullar geçerse sabit Chromium/depot_tools köklerini getir; DEPS/hook çalıştırma.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Çıktı biçimi.")
    arguments = parser.parse_args(argv)
    report = {"summary": "Yuva kaynak hazırlama planı", "checks": [], "notes": [], "source_prepared": False, "source_roots_prepared": False, "build_ready": False}
    try:
        versions = load_versions()
        patches = load_patches(versions)
        lock = load_lock()
        problem = workspace_problem(arguments.workspace)
        if problem:
            raise ToolError(problem)
        report["plan"] = {
            "chromium_version": versions["chromium_version"], "chromium_revision": versions["chromium_revision"],
            "yuva_version": versions["yuva_version"], "patchset_version": versions["patchset_version"],
            "patch_count": len(patches), "workspace": str(arguments.workspace.expanduser().resolve()),
            "minimum_free_gib": MINIMUM_FREE_GIB, "downloads_enabled": arguments.fetch_roots,
            "scope": lock["scope"], "roots": lock["roots"], "pending_stages": lock["pending_stages"],
        }
        report["notes"] = [
            f"Chromium: {versions['chromium_version']} / {versions['chromium_revision']}",
            f"Hedef dizin: {report['plan']['workspace']}",
            f"Kaynak, bağımlılık ve çıktılar için yaklaşık 100–200 GB veya daha fazla alan gerekebilir; ilk indirme kapısı {MINIMUM_FREE_GIB} GiB boş alan ister.",
            "Varsayılan komut indirme yapmaz. --fetch-roots yalnız kaynak köklerini getirir; bağımlılık/hook/yama çalıştırmaz, derlemeye hazır saymaz.",
        ]
        if not arguments.plan:
            host = inspect_environment(arguments.workspace)
            report["checks"] = host["checks"]
            report["preflight_ready"] = host["preflight_ready"]
            if arguments.fetch_roots:
                # JSON çıktı tek belge kalır; büyük indirme bildirimi önce stderr'e yazılır.
                print("\n".join(report["notes"]), file=sys.stderr, flush=True)
                if not host["preflight_ready"]:
                    raise ToolError("Ortam önkoşulları geçmedi; ağ isteği veya kaynak indirmesi başlatılmadı.")
                upstream = verify_network(versions)
                if upstream["update_available"]:
                    raise ToolError("Daha yeni Stable sürümü var; önce kaynak/yama kilidi incelenip güncellenmeli.")
                report["preparation"] = prepare_roots(arguments.workspace, versions)
                report["source_roots_prepared"] = True
                report["checks"].append({"id": "source_roots", "status": "pass", "message": "Sabit kökler ve DEPS/VERSION kimlikleri doğrulandı. Alt bağımlılık/araç hazırlığı tamamlanmadı."})
            else:
                report["checks"].append({"id": "source_preparation", "status": "blocked", "message": "Kaynak getirme açık --fetch-roots seçeneği ister; bu komut yalnız önkoşulları denetledi."})
    except ToolError as error:
        report["checks"].append({"id": "configuration", "status": "blocked", "message": str(error)})
    except OSError as error:
        report["checks"].append({"id": "filesystem", "status": "blocked", "message": f"Dosya sistemi işlemi tamamlanamadı (kod {error.errno}); mevcut veri korunuyor."})
    except KeyboardInterrupt:
        report["checks"].append({"id": "interrupted", "status": "blocked", "message": "Hazırlama kesildi; kısmi kaynak başarılı sayılmadı."})
    emit(report, arguments.format)
    return 1 if any(check["status"] == "blocked" for check in report["checks"]) else 0
