# ailib - Agent Interruption Hook Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)

`ailib` is a small Python library that enables scripts executed by AI agents to pause execution and request decisions or inputs from the host agent (e.g., Gemini, GPT, Claude).

It is designed to work in setups where the “agent executor” can read special request markers and then provide a response back to the running script.

---

## ✅ Installation (Local / Development)

> **Note:** `ailib` is not yet published on PyPI. The recommended way to use it is by installing it from the repository.

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

> On Windows (PowerShell):
> ```powershell
> python -m venv .venv
> .\.venv\Scripts\Activate.ps1
> ```

### 2) Install from the local source (editable)

```bash
pip install -e .
```

This installs `ailib` in “editable” mode, so changes you make to the source files are reflected immediately without reinstalling.

---

## 🧪 Running the Library Without Installing

If you prefer not to install the package, you can run scripts against the source tree directly by adding the repo root to `PYTHONPATH`: 

```bash
export PYTHONPATH="$PWD"
python -c "import ailib; print(ailib.__version__ if hasattr(ailib, '__version__') else 'no version')"
```

Or run a script with:

```bash
PYTHONPATH="$PWD" python scripts/your_script.py
```

---

## 📖 Quick Start

### 1) Simple Question (`ask`)

```python
import ailib

summary = ailib.ask("Can you summarize the current code?", context={"files": ["main.py", "utils.py"]})
print(f"AI said: {summary}")
```

### 2) Structured Response (`ask_json`)

```python
data = ailib.ask_json("Extract name and age from text", context="John is 25 years old.")
print(data["name"])  # 'John'
```

### 3) Decision Making (`decide`)

```python
action = ailib.decide("What to do next?", options=["retry", "abort", "ignore"])
```

---

## ⚙️ Configuration & Backends

### Available Backends

1. **`StdinBackend` (default)**
   - Writes a JSON request to `stderr` and waits for a response on `stdin`.
   - Ideal for interactive agents that can inspect stderr and respond on stdin.

2. **`FileBackend`**
   - Uses request/response files (default: `ailib_request.json` / `ailib_response.json`).
   - Useful when stdin/stdout is not reliable or when an agent polls for new requests.

### Environment Variables

Configure the library without changing code:

- `AILIB_BACKEND`: `stdin` or `file`
- `AILIB_TIMEOUT`: seconds to wait for a response (default `60`)
- `AILIB_FILE_REQUEST`: path for the request file
- `AILIB_FILE_RESPONSE`: path for the response file
- `AILIB_LOG_FILE`: path to the log file
- `AILIB_LOG_MAX_BYTES`: max size before log rotation
- `AILIB_LOG_LEVEL`: logging verbosity (`INFO`, `DEBUG`, `ERROR`)

### Switching Backends at Runtime

```python
from ailib import FileBackend, use_backend

# Globally
ailib.set_backend(FileBackend(poll_interval=0.1))

# Temporarily using a context manager
with ailib.use_backend(FileBackend()):
    result = ailib.ask("Running via files...")
```

---

## 🛠️ Protocol for AI Agents

AI agents should look for request markers on `stderr` to detect when a script is asking for input:

```json
<<<AILIB_REQUEST_START>>>
{
  "prompt": "...",
  "context": "...",
  "options": ["..."]
}
<<<AILIB_REQUEST_END>>>
```

When these markers appear, the agent should generate a response and write it back to the process’s `stdin` (followed by a newline).

---

## 🧪 Tests

Run the test suite with:

```bash
python -m unittest
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.

