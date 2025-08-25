# Due Diligence Quick‑Start  
A LangChain based agent that performs the market analysis of a company entered by the user by gathering, analyzing and summarizing up-to-date market intelligence of the company

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

```bash
python execute.py
```

Once your `run` is completed, you can see your traces on the UI.

## Why use the Due Diligence Agent?

By automating web queries, knowledge retrieval, and structured report writing, the Due Diligence Agent turns **days of manual research** into **minutes of automated insight**, ensuring the team’s decisions are backed by the latest, most accurate data.

- Automated queries, reducing comparison time in minutes instead of hours
- Uses HTTP search tools and vector store for the latest earnings, press releases and customer reviews
- Built on LangChain's agent architecture, every fact is traced back to a tool call, enabling transparency
- Delivers a structured report with clear sections:
  - **Executive summary:** General description
  - **Market Landscape:** Growth rates, Trends
  - **Competitive Positioning:** Competitors, Market share
  - **Customer Sentiment:** Customer reviews
  - **Risks & Red Flags:** Financial, Operational
  - **Opportunities:** Markets, Partnerships
  - **Sources:** URLs, Vector-store citations

---