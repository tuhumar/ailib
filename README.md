# ailib - Agent Interruption Hook Library

[![Python CI](https://github.com/diego/ailib/actions/workflows/python-ci.yml/badge.svg)](https://github.com/diego/ailib/actions/workflows/python-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)

`ailib` is an advanced Python library designed to allow scripts executed by AI Agents (like Gemini, GPT, Claude) to request actions or decisions directly from the host agent during execution.

Unlike standard API calls, `ailib` pauses script execution so that the executing AI can provide the necessary input to proceed.

---

## 🚀 Installation

```bash
pip install ailib
```

Or install locally for development:
```bash
pip install -e .
```

---

## 📖 Quick Start

### 1. Simple Question (`ask`)
Request a free-text response from the AI.

```python
import ailib

summary = ailib.ask("Can you summarize the current code?", context={"files": ["main.py", "utils.py"]})
print(f"AI said: {summary}")
```

### 2. Structured Response (`ask_json`)
Ensures the response is parsed as a Python dictionary or list. Supports automatic extraction from markdown code blocks.

```python
data = ailib.ask_json("Extract name and age from text", context="John is 25 years old.")
print(data['name']) # 'John'
```

### 3. Decision Making (`decide`)
Forces the AI to choose from a predefined set of options.

```python
action = ailib.decide("What to do next?", options=["retry", "abort", "ignore"])
```

---

## ⚙️ Configuration & Backends

### Available Backends

1.  **`StdinBackend` (Default)**: Prints JSON markers to `stderr` and waits for a response on `stdin`. Perfect for agents running in interactive terminals.
2.  **`FileBackend`**: Uses files (`ailib_request.json` and `ailib_response.json`) for communication. Useful in environments where `stdin` is not reliable.

### Environment Variables

Configure the library without changing your code:

- `AILIB_BACKEND`: "stdin" or "file".
- `AILIB_TIMEOUT`: Time in seconds to wait for AI (default 60s).
- `AILIB_FILE_REQUEST`: Custom path for the request file.
- `AILIB_FILE_RESPONSE`: Custom path for the response file.
- `AILIB_LOG_FILE`: Path to the log file.
- `AILIB_LOG_MAX_BYTES`: Max log size before rotation.
- `AILIB_LOG_LEVEL`: Log verbosity (INFO, DEBUG, ERROR).

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

For an AI to respond to scripts, it should be instructed to monitor `stderr` for:

```json
<<<AILIB_REQUEST_START>>>
{
  "prompt": "...",
  "context": "...",
  "options": ["..."]
}
<<<AILIB_REQUEST_END>>>
```

Upon finding these markers, the agent should generate the response and write it to the process's `stdin` (followed by a `\n`).

---

## 🧪 Testing

The library uses `unittest`. To run tests:

```bash
python3 tests/test_ailib_unittest.py
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

