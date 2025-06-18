from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph


from app.agents.research_agent.prompts import (
    RESEARCH_AGENT_PROMPT,
)
from app.agents.research_agent.tools import (
    get_kakao_search_tool,
    get_tavily_search_tool,
    get_wikipedia_tool,
)


def get_research_agent(
    llm: BaseChatModel,
) -> CompiledGraph:
    return create_react_agent(
        model=llm,
        tools=[get_kakao_search_tool(), get_tavily_search_tool(), get_wikipedia_tool()],
        prompt=RESEARCH_AGENT_PROMPT,
    )


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = get_research_agent(llm)

    # agent.invoke({"messages": HumanMessage(content="스페인에서 바다를 보고 싶은데 어떤 여행지가 좋을까?")})
    # agent.invoke({"messages": HumanMessage(content="서울에서 종로구 종로3가에 대해서 알려줘")})
    agent.invoke({"messages": HumanMessage(content="내년에 우크라이나 여행에 대해서는 어떻게 생각해?")})