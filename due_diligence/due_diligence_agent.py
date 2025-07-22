from fairo.core.chat.chat import ChatFairo
from langchain_community.utilities.requests import RequestsWrapper
from langchain.tools import tool
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from fairo.core.workflow.dependency import FairoVectorStore
from fairo.core.execution.executor import FairoExecutor
from fairo.settings import get_fairo_api_secret, get_fairo_api_key, get_fairo_base_url

def due_diligence():
    """
    Create a Due Diligence Agent which output due diligence for an input company
    """
    llm = ChatFairo()

    from langchain_community.tools import RequestsGetTool
    requests_wrapper = RequestsWrapper()
    requests_tool = RequestsGetTool(requests_wrapper=requests_wrapper, allow_dangerous_requests=True)

    class SearchArgs(BaseModel):
      query: str = Field(..., description="Web search query for up-to-date market info")

    @tool(args_schema=SearchArgs)
    def web_search(query: str) -> str:
        """
        Perform a generic web search and return raw page text (uses the built-in
        Requests tool under the hood).  In production you'd swap this for a
        SerpAPI / Tavily / Bing tool with proper API keys.
        """
        url = f"https://duckduckgo.com/html/?q={query}"
        return requests_tool.run({"url": url})

    competitive_store = FairoVectorStore(
        collection_name="competitive_data",
        username=get_fairo_api_key(),
        password=get_fairo_api_secret(),
        api_url=get_fairo_base_url(),
    )

    class CompQueryArgs(BaseModel):
        query: str = Field(..., description="Question comparing the company with its competitors")

    @tool(args_schema=CompQueryArgs)
    def competitor_qa(query: str) -> str:
        """
        Retrieve relevant competitive‑analysis snippets from the vector DB.
        """
        docs = competitive_store.similarity_search(query, k=5)
        if not docs:
            return "No competitive data found."
        return "\n\n".join(doc.page_content for doc in docs)

    analysis_store = FairoVectorStore(
        collection_name="competitive_analysis_reports",
        username=get_fairo_api_key(),
        password=get_fairo_api_secret(),
        api_url=get_fairo_base_url(),
    )

    class SaveArgs(BaseModel):
        text: str = Field(..., description="Markdown competitive-analysis report to save")

    @tool(args_schema=SaveArgs)
    def save_analysis(text: str) -> str:
        """Persist the completed competitive analysis into a shared vector DB."""
        analysis_store.add_texts([text], metadatas=[{"company": "Tesla"}])
        return "Analysis stored successfully."

    tools = [web_search, competitor_qa, save_analysis]
    
    template = """
    You are an **AI Investment Analyst - Due-Diligence Assistant**.
    Goal: Perform rapid, comprehensive due-diligence on a target company by collecting up-to-date market-landscape data, harvesting online reviews, and producing a structured report that flags market size, growth, competitive landscape, risks, opportunities, and customer sentiment.

    Backstory: You are an experienced equity-research analyst who can dynamically craft web queries, judge source reliability, and distil findings into a crisp two-page investment memo with citations and clear go/no-go signals.

    Available tools: {tools}
    Tool names: {tool_names}
    
    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: Return a full due-diligence report in markdown format, with sections: Executive summary, Market Landscape, Competitive Positioning, Customer Sentiment, Risks & Red Flags, Opportunities, Sources.

    User Input:
    {input}
    
    Intermediate answer: {agent_scratchpad}
    """.strip()

    prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
        template=template,
    )
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    executor = AgentExecutor(
        name="Due Diligence Agent",
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    return executor