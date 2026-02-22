from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterable

from .config import settings

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def list_projects() -> list[Path]:
    return sorted([p for p in settings.projects_dir.iterdir() if p.is_dir()])


def create_project(name: str) -> Path:
    cleaned = "".join(ch for ch in name.strip() if ch.isalnum() or ch in {"_", "-", " "}).strip()
    if not cleaned:
        raise ValueError("Название проекта пустое после очистки")

    project_path = settings.projects_dir / cleaned
    project_path.mkdir(parents=True, exist_ok=True)
    return project_path


def get_project(name: str) -> Path:
    project_path = settings.projects_dir / name
    if not project_path.exists() or not project_path.is_dir():
        raise FileNotFoundError(f"Проект не найден: {name}")
    return project_path


def list_project_images(project: Path) -> list[Path]:
    return sorted(
        [f for f in project.iterdir() if f.is_file() and f.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS]
    )


def list_project_text_results(project: Path) -> list[Path]:
    return sorted([f for f in project.iterdir() if f.is_file() and f.suffix.lower() == ".txt"])


def detect_downloads_dirs() -> list[Path]:
    candidates = [
        Path.home() / "Downloads",
        Path.home() / "Загрузки",
        Path("/sdcard/Download"),
        Path("/storage/emulated/0/Download"),
    ]
    return [path for path in candidates if path.exists() and path.is_dir()]


def list_download_files() -> list[Path]:
    files: list[Path] = []
    for directory in detect_downloads_dirs():
        files.extend(
            f for f in directory.iterdir() if f.is_file() and f.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS
        )
    return sorted(files)


def copy_files_to_project(files: Iterable[Path], project: Path) -> list[Path]:
    copied: list[Path] = []
    for src in files:
        if not src.exists() or not src.is_file():
            continue
        if src.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            continue
        dest = project / src.name
        shutil.copy2(src, dest)
        copied.append(dest)
    return copied
