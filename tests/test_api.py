import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("ALLOWED_ORIGIN", "*")

from app import app  # noqa: E402

client = TestClient(app)


def test_root_serves_index_html():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "CWASAAvatar" in resp.text


def test_avatar_route_ok():
    resp = client.get("/avatar")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_avatar_placeholder_is_replaced():
    resp = client.get("/avatar")
    assert "__ALLOWED_ORIGIN__" not in resp.text


def test_avatar_injects_wildcard_origin():
    resp = client.get("/avatar")
    assert 'const ALLOWED_ORIGIN = "*"' in resp.text


def test_avatar_injects_custom_origin(monkeypatch):
    monkeypatch.setenv("ALLOWED_ORIGIN", "https://my-frontend.com")
    # Re-read the template the same way the route does
    from pathlib import Path
    html = (Path(__file__).parent.parent / "templates" / "avatar.html").read_text(encoding="utf-8")
    html = html.replace("__ALLOWED_ORIGIN__", "https://my-frontend.com")
    assert 'const ALLOWED_ORIGIN = "https://my-frontend.com"' in html
    assert "__ALLOWED_ORIGIN__" not in html


def test_avatar_has_cwasa_div():
    resp = client.get("/avatar")
    assert "CWASAAvatar" in resp.text


def test_avatar_loads_cwasa_js():
    resp = client.get("/avatar")
    assert "allcsa.js" in resp.text


def test_static_favicon():
    resp = client.get("/favicon.svg")
    assert resp.status_code == 200
    assert "svg" in resp.headers["content-type"]


def test_static_cwasa_css():
    resp = client.get("/cwa/cwasa.css")
    assert resp.status_code == 200


def test_static_cwasa_js():
    resp = client.get("/cwa/allcsa.js")
    assert resp.status_code == 200


def test_static_categories_json():
    resp = client.get("/categories_files.json")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_static_words_json():
    resp = client.get("/words.json")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_cors_header_present():
    resp = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert "access-control-allow-origin" in resp.headers


def test_playground_route_ok():
    resp = client.get("/playground")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_playground_has_cwasa_div():
    resp = client.get("/playground")
    assert "CWASAAvatar" in resp.text


def test_playground_has_sigml_textarea():
    resp = client.get("/playground")
    assert "sigmlInput" in resp.text


def test_unknown_route_returns_404():
    resp = client.get("/does-not-exist-xyz")
    assert resp.status_code == 404
