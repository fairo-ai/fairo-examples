from fairo.core.execution.executor import FairoExecutor
from fairo.core.runnable.runnable import Runnable
from due_diligence_agent import due_diligence
FairoExecutor(
    agents=[due_diligence],
    input_fields=["input"]
).run({"input": "Tesla"})