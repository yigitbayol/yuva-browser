"""İndirme veya kurulum yapmadan yerel derleme önkoşullarını denetler."""

from __future__ import annotations

import platform
import plistlib
import shutil
import sys
from pathlib import Path

from .common import Parser, ROOT, emit, run_command

GIB = 1024 ** 3
MINIMUM_FREE_GIB = 200


def nearest_existing(path):
    while not path.exists() and path != path.parent:
        path = path.parent
    return path


def workspace_problem(workspace, root=ROOT):
    try:
        resolved = workspace.expanduser().resolve()
        repository = root.resolve()
    except (OSError, RuntimeError):
        return "Çalışma alanı yolu çözümlenemedi."
    if resolved.is_relative_to(repository) or repository.is_relative_to(resolved):
        return "Chromium çalışma alanı Yuva deposuyla iç içe olamaz; kardeş bir dizin seçin."
    if any(character.isspace() for character in str(resolved)):
        return "Chromium çalışma alanı yolunda boşluk bulunamaz."
    if resolved.exists() and not resolved.is_dir():
        return "Çalışma alanı mevcut bir dosyayı gösteriyor."
    return None


def linux_identity():
    """os-release verisini çalıştırmadan okur; ID_LIKE Pardus sayılmaz."""
    try:
        values = {}
        for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                values[key] = value.strip().strip('"').strip("'")
        return values
    except OSError:
        return {}


def inspect_environment(workspace, root=ROOT):
    checks = []

    def add(identifier, status, message):
        checks.append({"id": identifier, "status": status, "message": message})

    system = platform.system()
    architecture = platform.machine().lower()
    target = {"Darwin": "macos", "Windows": "windows", "Linux": "linux"}.get(system, "unsupported")
    identity = linux_identity() if target == "linux" else {}
    if identity.get("ID", "").lower() == "pardus":
        target = "pardus"
    add("python", "pass" if sys.version_info >= (3, 11) else "blocked", "Python 3.11 veya üzeri gerekiyor.")
    git = run_command(["git", "--version"])
    add("git", "pass" if git and git.returncode == 0 else "blocked", "Git komutu çalışabilmelidir.")
    supported_architecture = architecture in ("arm64", "aarch64", "x86_64", "amd64")
    add("host", "pass" if target != "unsupported" and supported_architecture else "blocked", f"Algılanan ortam: {target}, {architecture}.")
    if target in ("windows", "linux", "pardus") and architecture in ("arm64", "aarch64"):
        add("target_architecture", "blocked", "İlk masaüstü planında bu platformun ARM64 hedefi henüz nitelendirilmedi.")

    problem = workspace_problem(workspace, root)
    add("workspace", "blocked" if problem else "pass", problem or "Chromium çalışma alanı Yuva deposunun dışında.")
    free_gib = None
    if not problem:
        try:
            volume = nearest_existing(workspace.expanduser().resolve())
            free_gib = shutil.disk_usage(volume).free / GIB
            add("disk", "pass" if free_gib >= MINIMUM_FREE_GIB else "blocked", f"Boş alan {free_gib:.1f} GiB; Yuva'nın ilk indirme için ihtiyatlı bütçesi {MINIMUM_FREE_GIB} GiB.")
            if target == "macos":
                # diskutil sıradan bir dizini kabul etmez; df ile o dizinin aygıtını buluruz.
                usage = run_command(["df", "-P", str(volume)])
                rows = usage.stdout.splitlines() if usage and usage.returncode == 0 else []
                device = rows[-1].split()[0] if len(rows) > 1 and rows[-1].split() else ""
                disk = run_command(["diskutil", "info", "-plist", device]) if device.startswith("/dev/") else None
                try:
                    info = plistlib.loads(disk.stdout.encode()) if disk and disk.returncode == 0 else {}
                except (ValueError, plistlib.InvalidFileException):
                    info = {}
                add("filesystem", "pass" if info.get("FilesystemType", "").lower() == "apfs" else "blocked", "Chromium macOS çalışma alanı APFS üzerinde olmalıdır.")
        except OSError:
            add("disk", "blocked", "Hedef diskin boş alanı belirlenemedi.")

    memory_gib = None
    if target == "macos":
        memory = run_command(["sysctl", "-n", "hw.memsize"])
        try:
            memory_gib = int(memory.stdout.strip()) / GIB if memory and memory.returncode == 0 else None
        except ValueError:
            pass
        xcode = run_command(["xcodebuild", "-version"])
        add("xcode", "pass" if xcode and xcode.returncode == 0 and xcode.stdout.startswith("Xcode ") else "blocked", "Tam Xcode seçili olmalıdır; yalnız Command Line Tools yeterli değildir.")
        sdk = run_command(["xcrun", "--sdk", "macosx", "--show-sdk-path"])
        sdk_available = sdk and sdk.returncode == 0 and Path(sdk.stdout.strip()).is_dir()
        add("sdk", "pass" if sdk_available else "blocked", "macOS SDK yolu erişilebilir olmalıdır; sabit revizyona uygun SDK ayrıca nitelendirilecek.")
    else:
        add("platform_toolchain", "blocked", "Bu ilk araçta Windows/Linux/Pardus araç zinciri yeterliliği henüz uygulanmadı; hazır sonucu verilemez.")
        if target == "pardus":
            release = identity.get("VERSION_ID", "").split(".")[0]
            add("pardus_release", "pass" if release in ("23", "25") else "blocked", "Pardus desteği ayrı kapıdır; başlangıç matrisi 23.x ve 25.x, her yayın öncesi tekrar incelenir.")

    if memory_gib is not None:
        status = "blocked" if memory_gib < 8 else "warning" if memory_gib < 32 else "pass"
        add("memory", status, f"RAM {memory_gib:.1f} GiB; 32 GiB altı derlemelerde paralellik ve swap kullanımı ölçülmelidir.")
    else:
        add("memory", "warning", "RAM miktarı bu platformda otomatik doğrulanmadı.")
    ready = not any(check["status"] == "blocked" for check in checks)
    return {
        "scope": "host_preflight", "preflight_ready": ready, "build_verified": False,
        "platform": target, "architecture": architecture,
        "workspace": str(workspace.expanduser()), "free_gib": round(free_gib, 1) if free_gib is not None else None,
        "memory_gib": memory_gib,
        "summary": "Yerel önkoşul denetimi geçti." if ready else "Derleme hazırlığında giderilmesi gereken engeller var.",
        "checks": checks,
        "notes": [
            "Bu komut salt okunurdur; araç kurmaz, Chromium indirmez ve ağ isteği yapmaz.",
            "200 GiB bütçesi Yuva'nın ihtiyatlı başlangıç politikasıdır, Chromium'un evrensel asgari gereksinimi değildir.",
            "Bu sonuç tam bağımlılık kilidi, başarılı derleme veya platform desteği kanıtı değildir.",
        ],
    }


def main(argv=None):
    parser = Parser(description="Yerel derleme ortamını değiştirmeden denetle.")
    parser.add_argument("--workspace", type=Path, default=ROOT.parent / "yuva-chromium", help="Depo dışındaki hedef çalışma alanı.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Çıktı biçimi.")
    arguments = parser.parse_args(argv)
    report = inspect_environment(arguments.workspace)
    emit(report, arguments.format)
    return 0 if report["preflight_ready"] else 1
