from __future__ import annotations

from pathlib import Path
from typing import Iterable

import cv2
import easyocr
import numpy as np
import torch

from .config import settings


class OCREngine:
    def __init__(self, languages: tuple[str, ...] | None = None) -> None:
        self.languages = list(languages or settings.default_langs)
        self._reader: easyocr.Reader | None = None

    @property
    def use_gpu(self) -> bool:
        return bool(torch.cuda.is_available())

    @property
    def reader(self) -> easyocr.Reader:
        if self._reader is None:
            self._reader = easyocr.Reader(self.languages, gpu=self.use_gpu)
        return self._reader

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 18, 7, 21)
        _, threshold = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return threshold

    def recognize_file(self, image_path: Path) -> str:
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Не удалось загрузить изображение: {image_path}")
        preprocessed = self.preprocess(image)
        result = self.reader.readtext(preprocessed, detail=0, paragraph=True)
        return "\n".join(result).strip()

    def recognize_many(self, image_paths: Iterable[Path], batch_threshold: int | None = None) -> dict[str, str]:
        paths = list(image_paths)
        threshold = batch_threshold if batch_threshold is not None else settings.batch_threshold
        should_batch = len(paths) > threshold

        result: dict[str, str] = {}
        if should_batch:
            for i in range(0, len(paths), threshold):
                for path in paths[i : i + threshold]:
                    result[path.name] = self.recognize_file(path)
        else:
            for path in paths:
                result[path.name] = self.recognize_file(path)
        return result
