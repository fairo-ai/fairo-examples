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