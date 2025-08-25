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

## 3 · Create your first agent
##### `blog_ideas_agent.py`
```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from fairo.core.chat import ChatFairo
def ideasforblogpost():
    template = """
    You are an expert Blog-Post Idea Generator.
    When given a topic, you must output a list of 10 creative blog post titles,
    each on its own line.

    Topic: {topic}
    """
    prompt = PromptTemplate(
        input_variables=["topic"],
        template=template
    )
    chain = LLMChain(
        llm=ChatFairo(),
        prompt=prompt,
        verbose=False,
    )
    return chain
```

---

## 4 · Run with **`FairoExecutor`**

Create a new file to invoke the execution and build your chain.

##### `execute.py`
```python
from pydantic import BaseModel, Field
from fairo.core.execution.executor import FairoExecutor
from blog_ideas_agent import ideasforblogpost
class InputSchema(BaseModel):
        topic: str = Field(description="The subject you want generate ideas for")
FairoExecutor(
    input_schema=InputSchema,
    agents=[ideasforblogpost],
    input_fields=["topic"]
).run({"topic": "LLMs"})
```

Run your agent
```bash
python execute.py
```

Once your `run` is completed, you can see your traces on the UI.

---