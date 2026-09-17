"""Ortak komut satırı ve sınırlı süreç yardımcıları."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ToolError(Exception):
    """Kullanıcıya Türkçe açıklanabilen denetim hatası."""


class Parser(argparse.ArgumentParser):
    """Seçenek kimlikleri İngilizce, yardım ve hatalar Türkçedir."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, add_help=False, **kwargs)
        self._positionals.title = "Konum argümanları"
        self._optionals.title = "Seçenekler"
        self.add_argument("-h", "--help", action="help", help="Yardımı göster.")

    def format_help(self):
        return super().format_help().replace("usage:", "Kullanım:", 1)

    def error(self, message):
        self.exit(2, "Geçersiz veya eksik seçenek. Kullanım için --help çalıştırın.\n")


def run_command(arguments, *, cwd=None, env=None, timeout=15, input_text=None):
    """Shell kullanmadan ve süre sınırıyla yerel araç çalıştırır."""
    try:
        result = subprocess.run(
            arguments, cwd=cwd, env=env, capture_output=True, timeout=timeout,
            text=True, encoding="utf-8", errors="replace", check=False, input=input_text,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result


def emit(report, output_format):
    if output_format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print(report["summary"])
    labels = {"pass": "GEÇTİ", "warning": "NOT", "blocked": "ENGEL"}
    for check in report.get("checks", []):
        print(f"[{labels[check['status']]}] {check['message']}")
    for note in report.get("notes", []):
        print(note)
