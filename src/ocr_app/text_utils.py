from __future__ import annotations

from pathlib import Path

from .config import settings


def split_text_by_size(text: str, max_bytes: int) -> list[str]:
    if len(text.encode("utf-8")) <= max_bytes:
        return [text]

    chunks: list[str] = []
    current = []
    current_bytes = 0

    for line in text.splitlines(keepends=True):
        line_bytes = len(line.encode("utf-8"))
        if current and current_bytes + line_bytes > max_bytes:
            chunks.append("".join(current))
            current = []
            current_bytes = 0

        if line_bytes > max_bytes:
            encoded = line.encode("utf-8")
            for start in range(0, len(encoded), max_bytes):
                part = encoded[start : start + max_bytes].decode("utf-8", errors="ignore")
                if part:
                    chunks.append(part)
            continue

        current.append(line)
        current_bytes += line_bytes

    if current:
        chunks.append("".join(current))

    return chunks


def save_result_files(project_dir: Path, combined_text: str, base_name: str = "ocr_result") -> list[Path]:
    chunks = split_text_by_size(combined_text, settings.result_chunk_size_bytes)
    output_files: list[Path] = []

    for idx, chunk in enumerate(chunks, start=1):
        suffix = "" if len(chunks) == 1 else f"_part{idx:02d}"
        output_path = project_dir / f"{base_name}{suffix}.txt"
        output_path.write_text(chunk, encoding="utf-8")
        output_files.append(output_path)

    return output_files
