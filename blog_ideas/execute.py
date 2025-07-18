from fairo.core.execution.executor import FairoExecutor
from blog_ideas_agent import ideasforblogpost
FairoExecutor(
    agents=[ideasforblogpost],
    input_fields=["topic"]
).run({"topic": "LLMs"})