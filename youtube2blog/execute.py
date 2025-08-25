from fairo.core.execution.executor import FairoExecutor
from youtube2blog_agent import youtube2blog, InputSchema
FairoExecutor(
    input_schema=InputSchema,
    agents=[youtube2blog],
    input_fields=["input", "language"]
).run({"input": "https://www.youtube.com/watch?v=vcila2Dp3fg", "language": "en"})
