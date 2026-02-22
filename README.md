# OCR Project Manager (EasyOCR + OpenCV)

Веб-приложение для управления OCR-проектами с распознаванием текста на Python.

## Возможности

- Проекты хранятся как папки в `./projects`.
- Импорт изображений (jpg/png/...) из стандартных папок `Downloads` / `Загрузки`.
- OCR через EasyOCR + предобработка OpenCV.
- Автоматическое ускорение на GPU, если доступна CUDA (`torch.cuda.is_available()`).
- Пакетный режим включается, если файлов больше порога (`15` по умолчанию, настраивается в UI).
- Сохранение результата в `.txt`; если текст больше 1 МБ — автоматическое разбиение на несколько файлов.
- Встроенный файловый браузер в веб-интерфейсе: удобно скачивать результаты на ПК/мобильном устройстве.
- Модуль экспорта в исполняемые форматы:
  - `.exe` через PyInstaller;
  - `.apk` через Buildozer.

## Почему порог пакетной обработки = 15

15 — хороший стартовый компромисс между накладными расходами и удобством. Если в проекте типично много мелких файлов, можно снизить порог до 8–10; если файлы крупные и OCR долгий — увеличить до 20+.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python main.py
```

Открыть: `http://localhost:8000`.

## Экспорт в exe/apk

```python
from pathlib import Path
from ocr_app.exporter import build_exe, build_apk

# EXE
result = build_exe(Path("main.py"), app_name="OCRManager")
print(result.returncode, result.stdout, result.stderr)

# APK (нужен buildozer и Android toolchain)
result = build_apk(Path("."))
print(result.returncode, result.stdout, result.stderr)
```

## Структура

- `main.py` — точка входа.
- `src/ocr_app/web.py` — веб-UI и файловый браузер.
- `src/ocr_app/ocr_engine.py` — OCR/предобработка/сохранение txt.
- `src/ocr_app/project_service.py` — операции с проектами и импортом файлов.
- `src/ocr_app/exporter.py` — сборка в `.exe`/`.apk`.
