from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph

from app.agents.planner_agent.prompts import (
    PLANNER_AGENT_PROMPT,
)
from app.agents.planner_agent.tools import (
    get_naver_blog_search_tool,
    get_naver_cafe_search_tool,    
)
from app.agents.research_agent.tools import get_kakao_search_tool


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
            get_kakao_search_tool(),
        ],
        prompt=PLANNER_AGENT_PROMPT,
    )


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = get_planner_agent(llm)

    # Test
    response = agent.invoke({
        "messages": [HumanMessage(content="서울 2박 3일 여행 계획서를 작성해줘. 예산은 30만원이고, 커플 여행이야.")]
    })
    
    print(response) 