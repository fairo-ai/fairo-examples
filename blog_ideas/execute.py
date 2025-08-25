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