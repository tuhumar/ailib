# Contribution Guide

We are happy that you want to contribute to `ailib`! 🚀

## How to contribute

1.  **Fork** the repository.
2.  Create a **Branch** for your feature (`git checkout -b feature/new-feature`).
3.  **Commit** your changes (`git commit -m 'Add new feature'`).
4.  **Push** to the branch (`git push origin feature/new-feature`).
5.  Open a **Pull Request**.

## Local Development

To set up the development environment:

```bash
# Clone your fork
git clone https://github.com/your-username/ailib.git
cd ailib

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode with test dependencies
pip install -e .[test]
```

## Running Tests

Always run tests before submitting a PR:
```bash
python3 tests/test_ailib_unittest.py
```

## Code Style

- Follow **PEP 8**.
- Use Type Hints whenever possible.
- Add tests for new features.
