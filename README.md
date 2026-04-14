# Arabic Sign Language Avatar

A web-based system that translates Arabic text into Arabic Sign Language (ARSL) animations rendered by a 3D avatar in real time.

> This is a fork of [linuxscout/algerianSignLanguage-avatar](https://github.com/linuxscout/algerianSignLanguage-avatar).

---

## How It Works

The pipeline has three stages:

**1. Input**
The user types Arabic text into the web interface. A sliding-window algorithm matches each word (or phrase) against a built-in dictionary of ARSL words across categories: numbers, nouns, verbs, letters, adjectives, pronouns, adverbs, and miscellaneous.

**2. Lookup**
Each matched word maps to a [SiGML](https://vh.cmp.uea.ac.uk/index.php/SiGML) (Signing Gesture Markup Language) file. SiGML is an XML-based format derived from [HamNoSys](https://www.sign-lang.uni-hamburg.de/hamnosys.html) (Hamburg Notation System), a phonetic notation for sign languages. The dictionary index lives in `data/categories_files.json`; the SiGML files themselves live in `data/sigml/`.

**3. Rendering**
The [CWASA](https://vh.cmp.uea.ac.uk/index.php/CWA_Signing_Avatars) (CWA Signing Avatars) JavaScript library (`web-simulator/cwa/allcsa.js`) loads each SiGML file and drives a 3D avatar through the corresponding gesture sequence, playing one sign every ~1650 ms.

```
Arabic text  →  word lookup  →  SiGML files  →  CWASA renderer  →  3D avatar animation
```

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| Python 3.7+ | Only used to serve static files; no pip packages needed |
| A modern web browser | Chrome, Firefox, Safari, or Edge |

The web interface is pure HTML/CSS/JavaScript with no build step. The CWASA rendering library is bundled in the repo (`web-simulator/cwa/allcsa.js`).

The Python utility scripts in `tests/` and `tools/` also use only the standard library (`os`, `sys`, `csv`, `json`, `argparse`).

---

## Running Locally

### With Poetry (recommended)

[Poetry](https://python-poetry.org/) manages the Python environment and pins the interpreter version.

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install the project (creates a virtual env, nothing to download)
poetry install

# Serve the web interface
cd web-simulator
poetry run python3 -m http.server 8000
```

### Without Poetry

```bash
cd web-simulator
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Data Utilities

These scripts regenerate the processed data files from the raw SiGML source in `source-data/`.

```bash
# Generate all output files
make test_all

# Or individually:
make test_json        # data/categories_files.json
make test_wordlist    # CSV word list
make test_categories  # category breakdown
make test_stat        # statistics
```

You can also call the script directly:

```bash
cd tests
python3 extract_data_word_list.py -s ../source-data -o output -a all
```

---

## Project Structure

```
.
├── data/
│   ├── categories_files.json   # Word→SiGML index (loaded by the web app)
│   └── sigml/                  # SiGML animation files
├── docs/                       # Documentation and screenshots
├── source-data/                # Raw SiGML files organised by category
├── tests/
│   └── extract_data_word_list.py
├── tools/
│   └── import_fr_sigml_to_arabic.py
├── web-simulator/
│   ├── index.html              # Main web interface
│   ├── cwa/
│   │   ├── allcsa.js           # CWASA avatar rendering library
│   │   └── cwacfg.json         # Avatar list and renderer config
│   ├── avatars/                # 3D avatar models (JAR files)
│   └── shaders/
├── Makefile
├── pyproject.toml
└── LICENSE                     # CC BY-NC-4.0
```

---

## Resources

- [HamNoSys Notation System](https://www.sign-lang.uni-hamburg.de/hamnosys.html)
- [SiGML (Signing Gesture Markup Language)](https://vh.cmp.uea.ac.uk/index.php/SiGML)
- [CWASA Signing Avatars](https://vh.cmp.uea.ac.uk/index.php/CWA_Signing_Avatars)
- [DictaSign Project](https://www.sign-lang.uni-hamburg.de/dicta-sign/portal/concepts/concepts_fre.html)

## License

[CC BY-NC-4.0](LICENSE)
