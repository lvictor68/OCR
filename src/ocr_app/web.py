from __future__ import annotations

from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

from .config import settings
from .ocr_engine import OCREngine
from .text_utils import save_result_files
from .project_service import (
    copy_files_to_project,
    create_project,
    get_project,
    list_download_files,
    list_project_images,
    list_project_text_results,
    list_projects,
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "ocr-manager-secret"

    @app.get("/")
    def index():
        projects = list_projects()
        downloads = list_download_files()
        return render_template("index.html", projects=projects, downloads=downloads)

    @app.post("/projects")
    def create_project_route():
        name = request.form.get("name", "")
        try:
            create_project(name)
            flash("Проект создан", "success")
        except ValueError as exc:
            flash(str(exc), "error")
        return redirect(url_for("index"))

    @app.get("/projects/<project_name>")
    def project_page(project_name: str):
        project = get_project(project_name)
        images = list_project_images(project)
        texts = list_project_text_results(project)
        downloads = list_download_files()
        return render_template(
            "project.html",
            project=project,
            images=images,
            texts=texts,
            downloads=downloads,
            batch_threshold=settings.batch_threshold,
        )

    @app.post("/projects/<project_name>/upload")
    def upload_from_downloads(project_name: str):
        project = get_project(project_name)
        selected = request.form.getlist("download_files")
        files = [Path(p) for p in selected]
        copied = copy_files_to_project(files, project)
        flash(f"Скопировано файлов: {len(copied)}", "success")
        return redirect(url_for("project_page", project_name=project_name))

    @app.post("/projects/<project_name>/ocr")
    def run_ocr(project_name: str):
        project = get_project(project_name)
        images = list_project_images(project)
        if not images:
            flash("В проекте нет изображений для OCR", "error")
            return redirect(url_for("project_page", project_name=project_name))

        try:
            threshold = int(request.form.get("batch_threshold", settings.batch_threshold))
        except ValueError:
            threshold = settings.batch_threshold

        engine = OCREngine()
        recognized = engine.recognize_many(images, batch_threshold=max(1, threshold))
        combined = "\n\n".join(f"===== {name} =====\n{text}" for name, text in recognized.items())
        out_files = save_result_files(project, combined)

        gpu_text = "GPU" if engine.use_gpu else "CPU"
        flash(f"OCR завершен ({gpu_text}). Создано txt-файлов: {len(out_files)}", "success")
        return redirect(url_for("project_page", project_name=project_name))

    @app.get("/projects/<project_name>/files/<path:filename>")
    def download_project_file(project_name: str, filename: str):
        project = get_project(project_name)
        return send_from_directory(project, filename, as_attachment=True)

    return app
