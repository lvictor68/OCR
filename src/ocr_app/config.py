from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    base_dir: Path = Path(__file__).resolve().parents[2]
    projects_dir: Path = base_dir / "projects"
    default_langs: tuple[str, ...] = ("ru", "en")
    batch_threshold: int = 15
    result_chunk_size_bytes: int = 1_048_576  # 1 MB


settings = Settings()
settings.projects_dir.mkdir(parents=True, exist_ok=True)
