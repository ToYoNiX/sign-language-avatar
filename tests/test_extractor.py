import csv
import json
import os
import tempfile

import pytest

from tests.extract_data_word_list import FileExtractor


def make_source(base, categories):
    """Create a temporary source directory with fake .sigml files."""
    for cat, words in categories.items():
        cat_dir = os.path.join(base, cat)
        os.makedirs(cat_dir)
        for word in words:
            open(os.path.join(cat_dir, word + ".sigml"), "w").close()


@pytest.fixture
def simple_source(tmp_path):
    src = str(tmp_path / "source")
    make_source(src, {
        "أرقام": ["1", "2", "3"],
        "أفعال": ["يذهب", "يأكل"],
    })
    return src


@pytest.fixture
def output_dir(tmp_path):
    out = str(tmp_path / "output")
    os.makedirs(out)
    return out


# --- JSON ---

def test_json_contains_all_categories(simple_source, output_dir):
    fe = FileExtractor(simple_source, output_dir)
    fe.run("json")
    with open(os.path.join(output_dir, "categories_files.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert "أرقام" in data
    assert "أفعال" in data


def test_json_words_match_files(simple_source, output_dir):
    fe = FileExtractor(simple_source, output_dir)
    fe.run("json")
    with open(os.path.join(output_dir, "categories_files.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert set(data["أرقام"]) == {"1", "2", "3"}
    assert set(data["أفعال"]) == {"يذهب", "يأكل"}


# --- Wordlist ---

def test_wordlist_file_created(simple_source, output_dir):
    FileExtractor(simple_source, output_dir).run("wordlist")
    assert os.path.exists(os.path.join(output_dir, "wordlist.csv"))


def test_wordlist_has_header(simple_source, output_dir):
    FileExtractor(simple_source, output_dir).run("wordlist")
    with open(os.path.join(output_dir, "wordlist.csv"), encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
    assert header == ["File Name", "Category", "Translation"]


def test_wordlist_contains_all_words(simple_source, output_dir):
    FileExtractor(simple_source, output_dir).run("wordlist")
    with open(os.path.join(output_dir, "wordlist.csv"), encoding="utf-8") as f:
        rows = list(csv.reader(f))[1:]  # skip header
    words = {row[0] for row in rows}
    assert words == {"1", "2", "3", "يذهب", "يأكل"}


# --- Categories ---

def test_categories_file_created(simple_source, output_dir):
    FileExtractor(simple_source, output_dir).run("categories")
    assert os.path.exists(os.path.join(output_dir, "categories.csv"))


def test_categories_lists_all_categories(simple_source, output_dir):
    FileExtractor(simple_source, output_dir).run("categories")
    with open(os.path.join(output_dir, "categories.csv"), encoding="utf-8") as f:
        content = f.read()
    assert "أرقام" in content
    assert "أفعال" in content


# --- Statistics ---

def test_statistics_file_created(simple_source, output_dir):
    FileExtractor(simple_source, output_dir).run("statistics")
    assert os.path.exists(os.path.join(output_dir, "statistics.csv"))


def test_statistics_correct_counts(simple_source, output_dir):
    FileExtractor(simple_source, output_dir).run("statistics")
    with open(os.path.join(output_dir, "statistics.csv"), encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        counts = {row[0]: int(row[1]) for row in reader}
    assert counts["أرقام"] == 3
    assert counts["أفعال"] == 2


# --- All ---

def test_run_all_creates_every_output(simple_source, output_dir):
    FileExtractor(simple_source, output_dir).run("all")
    assert os.path.exists(os.path.join(output_dir, "wordlist.csv"))
    assert os.path.exists(os.path.join(output_dir, "categories.csv"))
    assert os.path.exists(os.path.join(output_dir, "statistics.csv"))
    assert os.path.exists(os.path.join(output_dir, "categories_files.json"))


# --- Edge cases ---

def test_empty_source_produces_empty_json(tmp_path):
    src = str(tmp_path / "empty_source")
    os.makedirs(src)
    out = str(tmp_path / "out")
    os.makedirs(out)
    fe = FileExtractor(src, out)
    fe.run("json")
    with open(os.path.join(out, "categories_files.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert data == {}


def test_single_category_single_word(tmp_path):
    src = str(tmp_path / "src")
    out = str(tmp_path / "out")
    os.makedirs(out)
    make_source(src, {"حروف": ["أ"]})
    fe = FileExtractor(src, out)
    fe.run("json")
    with open(os.path.join(out, "categories_files.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"حروف": ["أ"]}
