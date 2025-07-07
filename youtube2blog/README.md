# Fairo Trace Quick‑Start  
*Record every agent step in seconds*

---

## Prerequisites

| You need | Why it matters | How to provide it |
|----------|----------------|-------------------|
| **Python 3.11+** | Fairo SDK requires 3.11 or newer | `python --version` |
| **Virtual environment** | Isolate SDK dependencies | `python -m venv fairo_env && source fairo_env/bin/activate` |

---

## 1 · Install the SDK

The package is available on <a href="https://pypi.org/project/fairo" target="_blank">PyPI</a>:

```bash
pip install fairo
```

## 2 · Authentication

Generate your API key, secret and export them in your environment:

```bash
export FAIRO_API_ACCESS_KEY_ID=<your-key>
export FAIRO_API_SECRET=<your-secret>
```

Export your OPENAI_API_KEY in your environment:

```bash
export OPENAI_API_KEY=<your-key>
```

## 3 · Run your agent
```

Run your agent
```bash
python execute.py
```

Once your `run` is completed, you can see your traces on the UI.

---