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
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from fairo.core.chat.chat import FairoChat

def ideasforblogpost():
    llm = FairoChat(
        endpoint="chat",
    )
    tools = []
    role_prompt = """
    You are Ideas For Blogpost Agent, an expert at reading a subject and providing new blogpost ideas for that niche.
    You always:
    - Structure a list of 10 new blogpost titles based on the subject provided
    """
    suffix_prompt = "When given a subject, read it and output a structured list of 10 new blogpost titles."
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=False,
        agent_kwargs={
            "prefix": role_prompt,
            "suffix": suffix_prompt,
        },
    )
    return agent
```

---

## 4 · Run with **`FairoExecutor`**

Create a new file to invoke the execution and build your chain.

##### `execute.py`
```python
from fairo.core.execution.executor import FairoExecutor
from blog_ideas_agent import ideasforblogpost
FairoExecutor(
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