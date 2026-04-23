# Arabic Sign Language Avatar

A web-based system that translates Arabic text into Arabic Sign Language (ArSL) animations rendered by a 3D avatar in real time.

> This is a fork of [linuxscout/algerianSignLanguage-avatar](https://github.com/linuxscout/algerianSignLanguage-avatar).

---

## How It Works

The pipeline has three stages:

**1. Input**
The user types Arabic text into the web interface. A sliding-window algorithm matches each word (or phrase) against the dictionary.

**2. Lookup**
Each matched word maps to a [SiGML](https://vh.cmp.uea.ac.uk/index.php/SiGML) (Signing Gesture Markup Language) file. SiGML is an XML-based format derived from [HamNoSys](https://www.sign-lang.uni-hamburg.de/hamnosys.html) (Hamburg Notation System), a phonetic notation for sign languages. The dictionary lives in `data/dict/dictionary.json`; the SiGML files live in `data/sigml/`. Both are symlinked into `web-simulator/` so the dev server and build see them automatically.

**3. Rendering**
The [CWASA](https://vh.cmp.uea.ac.uk/index.php/CWA_Signing_Avatars) (CWA Signing Avatars) JavaScript library (`web-simulator/cwa/allcsa.js`) loads each SiGML file and drives a 3D avatar through the corresponding gesture sequence. Timing and other runtime parameters are controlled via `web-simulator/avatar.json`.

```
Arabic text  →  dictionary lookup  →  SiGML files  →  CWASA renderer  →  3D avatar animation
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
| `http://localhost:8000/embed` | Avatar-only iframe endpoint |
| `http://localhost:8000/playground` | SiGML playground — paste raw SiGML and watch the avatar sign it |

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ALLOWED_ORIGIN` | `*` | Origin of the parent page embedding `/embed`. Set to your frontend URL in production (e.g. `https://your-frontend.com`). |

---

## Configuring the Avatar

All runtime tuning lives in **`web-simulator/avatar.json`**. Edit this file to change behaviour without touching any code:

```json
{
  "signDuration": 1000,
  "dictionary": "dict/dictionary.json"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `signDuration` | number (ms) | How long the avatar waits between signs. Increase if signs feel rushed, decrease if they feel slow. |
| `dictionary` | string (path) | Path to the dictionary file, relative to the page root. |

---

## Managing the Dictionary

The dictionary lives in **`data/dictionary.json`**. It is a JSON object where each key is a category name and each value is an array of words that have a corresponding SiGML file in `data/sigml/`.

```json
{
  "الارقام": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "16", "17", "18", "19", "20", "30", "40", "50", "70", "80", "90"]
}
```

### Adding a new word

1. Add the SiGML file for the word to `data/sigml/<word>.sigml`
2. Add the word string to the appropriate category array in `data/dict/dictionary.json`
3. If the word belongs to a new category, add a new key to the JSON object

That's it — the symlinks mean the dev server and static build both pick it up automatically.

### Adding a new category

Add a new top-level key to `data/dict/dictionary.json`:

```json
{
  "الارقام": ["1", "2", ...],
  "التحيات": ["مرحبا", "شكرا", ...]
}
```

Each word in the array must have a matching `.sigml` file in `data/sigml/`.

---

## Embed Iframe Endpoint

`GET /embed` serves a full-viewport, controls-free page designed to be embedded as an iframe in another frontend.

### Embedding

```html
<iframe
  id="avatar"
  src="http://localhost:8000/embed"
  width="400"
  height="500"
  style="border: none; background: transparent;"
></iframe>
```

### Sending commands (`parent → iframe`)

Use `postMessage` to control the avatar from the parent page:

```js
const avatar = document.getElementById('avatar').contentWindow;

// Sign Arabic text — words are matched against the dictionary automatically.
// Unrecognised words are silently skipped.
avatar.postMessage({ type: 'sign', text: '1 2 3' }, '*');

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
      // payload: { word: '1', index: 0, total: 3 }
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

## Deploying to GitHub Pages

The repository includes a build script and a GitHub Actions workflow that automatically deploys the avatar as a static site to GitHub Pages on every push to `master`.

### Setup

1. Go to your repository **Settings → Pages**
2. Under **Build and deployment**, set the source to **GitHub Actions**
3. Push to `master` — the workflow triggers automatically and deploys the site

### URLs after deployment

| URL | Description |
|-----|-------------|
| `https://<user>.github.io/<repo>/` | Full standalone UI |
| `https://<user>.github.io/<repo>/embed` | Avatar-only iframe endpoint |
| `https://<user>.github.io/<repo>/playground` | SiGML playground |

### Origin configuration

The GitHub Pages deployment builds with `ALLOWED_ORIGIN=*` by default, meaning any frontend can embed and use the iframe.

To restrict it to a specific frontend, pass `--origin` to `build.py` in the workflow:

```yaml
- name: Build static site
  run: python build.py --origin "https://your-frontend.com"
```

Or omit `--origin` entirely to keep the default `*`.

---

## Running Tests

```bash
poetry run python -m pytest -v
```

| Test file | What it covers |
|-----------|---------------|
| `tests/test_api.py` | FastAPI routes — `GET /`, `GET /embed`, static assets, CORS headers, origin injection, 404 behaviour |
| `tests/test_extractor.py` | `FileExtractor` — word index, CSV wordlist, category/statistics outputs, edge cases |

---

## Project Structure

```
.
├── app.py                        # FastAPI dev server
├── build.py                      # Static site build script for GitHub Pages
├── .github/workflows/
│   └── deploy.yml                # CI/CD — deploys to GitHub Pages on push to master
├── templates/
│   ├── embed.html                # Iframe-only embed page (/embed); __ALLOWED_ORIGIN__ injected at build/serve time
│   └── playground.html           # SiGML playground page (/playground)
├── web-simulator/
│   ├── index.html                # Full standalone UI (/)
│   ├── avatar.js                 # Shared avatar logic — loads config + dictionary, exposes Avatar.sign/stop
│   ├── avatar.json               # Runtime config (signDuration, dictionary path) — edit to tune behaviour
│   ├── sigml -> ../data/sigml         # Symlink — canonical SiGML files live in data/
│   ├── dictionary.json -> ../data/dictionary.json  # Symlink — canonical dictionary lives in data/
│   ├── cwa/
│   │   ├── allcsa.js             # CWASA avatar rendering library (bundled, do not edit)
│   │   └── cwacfg.json           # Avatar list and renderer config
│   ├── avatars/                  # 3D avatar models
│   ├── shaders/
│   ├── cwaclientcfg.json         # CWASA client config
│   ├── h2s.xsl                   # HamNoSys → SiGML XSLT transform
│   └── favicon.svg
├── data/
│   ├── sigml/                    # SiGML animation files — one file per word (<word>.sigml)
│   └── dictionary.json           # Categorised word list — single source of truth for all words
├── tests/
│   ├── test_api.py
│   ├── test_extractor.py
│   └── extract_data_word_list.py
├── sigml-reference.md            # SiGML format reference
├── CREDITS
├── .env                          # Local env vars (not committed)
├── .env.example                  # Env var template
├── Makefile
├── poetry.lock
├── pyproject.toml
└── LICENSE                       # CC BY-NC-4.0
```

### How the build works

`build.py` copies `web-simulator/` into `pages/` (resolving all symlinks into real files), then injects `__ALLOWED_ORIGIN__` into the embed template and copies the playground template. The `pages/` directory is .gitignored — it is generated output only.

The FastAPI dev server (`app.py`) serves `web-simulator/` directly with `follow_symlink=True`, so symlinks are transparent and no build step is needed during development.

---

## Resources

- [HamNoSys Notation System](https://www.sign-lang.uni-hamburg.de/hamnosys.html)
- [SiGML (Signing Gesture Markup Language)](https://vh.cmp.uea.ac.uk/index.php/SiGML)
- [CWASA Signing Avatars](https://vh.cmp.uea.ac.uk/index.php/CWA_Signing_Avatars)
- [DictaSign Project](https://www.sign-lang.uni-hamburg.de/dicta-sign/portal/concepts/concepts_fre.html)

## License

[CC BY-NC-4.0](LICENSE)
