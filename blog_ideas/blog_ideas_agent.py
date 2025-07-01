# from langchain.chat_models import ChatOpenAI
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