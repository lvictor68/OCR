from ocr_app.text_utils import split_text_by_size


def test_split_text_by_size_splits_large_content():
    line = "привет мир\n"
    text = line * 100
    chunks = split_text_by_size(text, max_bytes=100)

    assert len(chunks) > 1
    assert "".join(chunks) == text
    assert all(len(c.encode("utf-8")) <= 100 for c in chunks)
