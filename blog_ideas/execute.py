from fairo.core.execution.executor import FairoExecutor
from blog_ideas_agent import ideasforblogpost
from fairo.core.runnable.runnable import Runnable
FairoExecutor(
    agents=[ideasforblogpost],
).run("LLMs")