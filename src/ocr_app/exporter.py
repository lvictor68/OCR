from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build_exe(entrypoint: Path, app_name: str = "OCRManager") -> subprocess.CompletedProcess[str]:
    """Build .exe with PyInstaller (works on Windows hosts)."""
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--name",
        app_name,
        str(entrypoint),
    ]
    return subprocess.run(cmd, check=False, text=True, capture_output=True)


def build_apk(project_dir: Path) -> subprocess.CompletedProcess[str]:
    """Build .apk via Buildozer (Linux/mobile-friendly toolchain)."""
    cmd = ["buildozer", "android", "debug"]
    return subprocess.run(cmd, cwd=project_dir, check=False, text=True, capture_output=True)
