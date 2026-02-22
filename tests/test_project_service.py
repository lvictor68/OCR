from ocr_app import config
from ocr_app.project_service import create_project


def test_create_project_sanitizes_name(tmp_path):
    original = config.settings.projects_dir
    object.__setattr__(config.settings, "projects_dir", tmp_path)
    try:
        project = create_project(" Test:*Name ")
        assert project.exists()
        assert "TestName" in project.name.replace(" ", "")
    finally:
        object.__setattr__(config.settings, "projects_dir", original)
