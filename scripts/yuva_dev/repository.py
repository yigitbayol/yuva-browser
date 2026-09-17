"""Git indeksinin Chromium ağacı, ikili çıktı veya önbellek taşımamasını denetler."""

from __future__ import annotations

from pathlib import PurePosixPath

from .common import Parser, ROOT, ToolError, emit, run_command

MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TOTAL_BYTES = 100 * 1024 * 1024
MAX_FILES = 20000
BLOCKED_ROOTS = {"chromium", "chromium-src", "chromium-workspace", "upstream", "workspace", "workspaces", "depot_tools", "src", "chrome", "content"}
BLOCKED_DIRECTORIES = {"depot_tools", "out", "dist", "artifacts", "downloads", "node_modules", "__pycache__", ".cipd", "_cipd", ".cache", "cache", ".git_cache", ".venv", "venv", "profiles", "test-profiles", "target", ".git"}
BLOCKED_SUFFIXES = {".dmg", ".pkg", ".deb", ".rpm", ".exe", ".dll", ".dylib", ".so", ".o", ".obj", ".a", ".lib", ".pdb", ".zip", ".tar", ".gz", ".xz", ".7z", ".pyc", ".pyo", ".key", ".p12", ".pfx", ".log"}


def path_problem(name):
    path = PurePosixPath(name)
    parts = tuple(part.lower() for part in path.parts)
    if not parts or path.is_absolute() or ".." in parts or any(ord(character) < 32 for character in name):
        return "Güvenli olmayan dosya yolu"
    if parts[0] in BLOCKED_ROOTS or any(part in BLOCKED_DIRECTORIES or part.endswith((".app", ".dsym")) for part in parts[:-1]):
        return "Kaynak bağımlılığı, çıktı veya önbellek dizini"
    if path.suffix.lower() in BLOCKED_SUFFIXES or parts[-1].startswith(".gclient"):
        return "İkili/üretilmiş çıktı, yerel araç ayarı veya özel anahtar"
    if (parts[-1] == ".env" or parts[-1].startswith(".env.")) and parts[-1] != ".env.example":
        return "Yerel ortam/sır dosyası"
    if "third_party/blink/" in name.lower() or name.lower().endswith("chrome/version"):
        return "Chromium kaynak ağacı işareti"
    return None


def inspect_index(root=ROOT):
    listing = run_command(["git", "ls-files", "--stage", "-z"], cwd=root)
    if not listing or listing.returncode:
        raise ToolError("Git indeksi okunamadı.")
    entries = []
    for record in listing.stdout.split("\0"):
        if not record:
            continue
        try:
            header, name = record.split("\t", 1)
            mode, object_id, stage = header.split()
        except ValueError as error:
            raise ToolError("Git indeks girdisi beklenen biçimde değil.") from error
        entries.append((mode, object_id, stage, name))
    if len(entries) > MAX_FILES:
        raise ToolError("Dosya sayısı ince Yuva deposu bütçesini aşıyor; kaynak ağacı eklenmiş olabilir.")
    violations = []
    for mode, _, stage, name in entries:
        problem = path_problem(name)
        if stage != "0" or mode not in {"100644", "100755"}:
            problem = "Çözülmemiş birleştirme, sembolik bağlantı veya alt modül"
        if problem:
            violations.append(f"{name!r}: {problem}.")
    object_ids = sorted({entry[1] for entry in entries if entry[0] in {"100644", "100755"}})
    sizes = {}
    if object_ids:
        objects = run_command(
            ["git", "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
            cwd=root, input_text="\n".join(object_ids) + "\n",
        )
        if not objects or objects.returncode:
            raise ToolError("İndeksteki gerçek Git nesnelerinin boyutu doğrulanamadı.")
        try:
            for line in objects.stdout.splitlines():
                object_id, kind, size = line.split()
                if kind != "blob" or object_id not in object_ids or int(size) < 0:
                    raise ValueError()
                sizes[object_id] = int(size)
        except ValueError as error:
            raise ToolError("Git nesne boyutu yanıtı geçersiz.") from error
        if set(sizes) != set(object_ids):
            raise ToolError("Bazı Git nesneleri denetlenemedi.")
    total = 0
    for mode, object_id, _, name in entries:
        if mode in {"100644", "100755"}:
            size = sizes[object_id]
            total += size
            if size > MAX_FILE_BYTES:
                violations.append(f"{name!r}: tek dosya bütçesi 5 MiB aşıldı.")
    if total > MAX_TOTAL_BYTES:
        violations.append("İndeksteki dosyaların toplamı 100 MiB bütçesini aşıyor.")
    return {
        "summary": "Depo indeksi denetimi geçti." if not violations else "Depo indeksi yayınlanamayacak girdiler içeriyor.",
        "passed": not violations, "file_count": len(entries), "total_bytes": total,
        "checks": [{"id": "repository_contents", "status": "blocked" if violations else "pass", "message": message} for message in (violations or ["İndekste büyük kaynak ağacı, bilinen çıktı/önbellek yolu veya aşırı büyük dosya yok."])],
        "notes": ["Denetim çalışma dosyası yerine commit edilecek Git nesnesini inceler; eski Git geçmişini veya bütün sır türlerini taradığı iddia edilmez."],
    }


def main(argv=None):
    parser = Parser(description="Commit edilecek Yuva ağacında kaynak/ikili/önbellek sızıntısını denetle.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Çıktı biçimi.")
    arguments = parser.parse_args(argv)
    try:
        report = inspect_index()
    except ToolError as error:
        report = {"summary": str(error), "passed": False}
    emit(report, arguments.format)
    return 0 if report["passed"] else 1
