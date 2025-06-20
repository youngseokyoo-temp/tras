from langchain_core.language_models import BaseChatModel
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

from app.agents.planner_agent.prompts import (
    PLANNER_AGENT_PROMPT,
)
from app.agents.planner_agent.tools import (
    get_naver_blog_search_tool,
    get_naver_cafe_search_tool,
    get_web_loader_tool,
)
from app.agents.research_agent.tools import (
    get_gplaces_search_tool, 
    get_kakao_search_tool
)


def get_planner_agent(
    llm: BaseChatModel,
) -> CompiledGraph:
    """Get a travel planning agent.

    Args:
        llm (BaseChatModel): LLM model to use

    Returns:
        CompiledGraph: Generated travel planning agent
    """
    return create_react_agent(
        model=llm,
        tools=[
            get_naver_blog_search_tool(),
            get_naver_cafe_search_tool(),
            get_gplaces_search_tool(),
            get_kakao_search_tool(),
            get_web_loader_tool(),
        ],
        prompt=PLANNER_AGENT_PROMPT,
    )


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    agent = get_planner_agent(llm)

    # Test
    response = agent.invoke(
        {
            "messages": [
               {"role": "user", "content": "파리 여행으로 3박 4일 계획서를 작성해줘. 맛있는 음식을 즐기는 커플 여행이야."} 
            ]
        }
    )
