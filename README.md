# Arabic Sign Language Avatar

A web-based system that translates Arabic text into Arabic Sign Language (ARSL) animations rendered by a 3D avatar in real time.

> This is a fork of [linuxscout/algerianSignLanguage-avatar](https://github.com/linuxscout/algerianSignLanguage-avatar).

---

## How It Works

The pipeline has three stages:

**1. Input**
The user types Arabic text into the web interface. A sliding-window algorithm matches each word (or phrase) against a built-in flat dictionary of ARSL words.

**2. Lookup**
Each matched word maps to a [SiGML](https://vh.cmp.uea.ac.uk/index.php/SiGML) (Signing Gesture Markup Language) file. SiGML is an XML-based format derived from [HamNoSys](https://www.sign-lang.uni-hamburg.de/hamnosys.html) (Hamburg Notation System), a phonetic notation for sign languages. The dictionary index lives in `data/words.json` (and `data/categories_files.json` for compatibility); the SiGML files themselves live in `data/sigml/`.

**3. Rendering**
The [CWASA](https://vh.cmp.uea.ac.uk/index.php/CWA_Signing_Avatars) (CWA Signing Avatars) JavaScript library (`web-simulator/cwa/allcsa.js`) loads each SiGML file and drives a 3D avatar through the corresponding gesture sequence, playing one sign every ~1650 ms.

```
Arabic text  →  word lookup  →  SiGML files  →  CWASA renderer  →  3D avatar animation
```

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| Python 3.9+ | FastAPI + uvicorn |
| A modern web browser | Chrome, Firefox, Safari, or Edge |

---

## Running Locally

### Setup

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Copy the env template and edit if needed
cp .env.example .env
```

### Start the server

```bash
poetry run python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Full standalone UI |
| `http://localhost:8000/avatar` | Avatar-only iframe endpoint |
| `http://localhost:8000/playground` | SiGML playground — paste raw SiGML and watch the avatar sign it |

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ALLOWED_ORIGIN` | `*` | Origin of the parent page embedding `/avatar`. Set to your frontend URL in production (e.g. `https://your-frontend.com`). |

---

## Avatar Iframe Endpoint

`GET /avatar` serves a full-viewport, controls-free page designed to be embedded as an iframe in another frontend.

### Embedding

```html
<iframe
  id="avatar"
  src="http://localhost:8000/avatar"
  width="400"
  height="500"
  style="border: none; background: transparent;"
></iframe>
```

### Sending commands (`parent → iframe`)

Use `postMessage` to control the avatar from the parent page:

```js
const avatar = document.getElementById('avatar').contentWindow;

// Sign Arabic text — words are looked up against the dictionary automatically.
// Unrecognised words are silently skipped.
avatar.postMessage({ type: 'sign', text: 'مرحبا كيف حالك' }, '*');

// Stop the current signing sequence
avatar.postMessage({ type: 'stop' }, '*');
```

### Receiving status events (`iframe → parent`)

The iframe posts status events back so the parent can react to the animation lifecycle:

```js
window.addEventListener('message', (event) => {
  const { type, ...payload } = event.data;

  switch (type) {
    case 'ready':
      // Dictionary loaded, avatar is ready to receive commands
      break;

    case 'signing':
      // Fired for each word as it starts playing
      // payload: { word: 'مرحبا', index: 0, total: 3 }
      break;

    case 'done':
      // Full sequence finished
      break;

    case 'error':
      // No matching words were found in the dictionary
      // payload: { reason: 'no matching words found' }
      break;
  }
});
```

### Origin security

In development `ALLOWED_ORIGIN=*` allows any parent page to send commands. In production set it to your frontend's exact origin in `.env`:

```
ALLOWED_ORIGIN=https://your-frontend.com
```

The iframe will silently ignore `postMessage` events from any other origin.

---

## Running Tests

```bash
poetry run python -m pytest -v
```

| Test file | What it covers |
|-----------|---------------|
| `tests/test_api.py` | FastAPI routes — `GET /`, `GET /avatar`, static assets, CORS headers, origin injection, 404 behaviour |
| `tests/test_extractor.py` | `FileExtractor` — flat JSON word index, CSV wordlist, category/statistics outputs, edge cases (empty source, single word) |

---

## Data Utilities

These scripts regenerate processed data files from `data/sigml/`.

```bash
# Generate all output files
make test_all

# Or individually:
make test_json        # data/categories_files.json (flat word list)
make test_wordlist    # CSV word list
make test_categories  # category breakdown
make test_stat        # statistics
```

You can also call the script directly:

```bash
cd tests
python3 extract_data_word_list.py -s ../data/sigml -o output -a all
```

---

## Project Structure

```
.
├── templates/
│   └── avatar.html             # Iframe-only avatar endpoint (served at /avatar)
├── data/
│   ├── words.json              # Flat word index (loaded by the web app)
│   ├── categories_files.json   # Flat word index (legacy filename)
│   └── sigml/                  # SiGML animation files
├── sigml-reference.md          # SiGML reference
├── tests/
│   └── extract_data_word_list.py
├── web-simulator/
│   ├── index.html              # Full standalone UI (served at /)
│   ├── cwa/
│   │   ├── allcsa.js           # CWASA avatar rendering library
│   │   └── cwacfg.json         # Avatar list and renderer config
│   ├── avatars/                # 3D avatar models (JAR files)
│   └── shaders/
├── app.py                      # FastAPI server
├── .env                        # Local env vars (not committed)
├── .env.example                # Env var template
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
