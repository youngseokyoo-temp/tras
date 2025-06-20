from langchain_core.language_models import BaseChatModel
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

from app.agents.twitter_agent.constants import (
    AGENT_NAME,
    AGENT_PROMPT_NAME,
    TWEETS_MAX_RESULTS,
)
from app.agents.twitter_agent.tools import (
    get_twitter_delete_tool,
    get_twitter_post_tool,
    get_twitter_user_tweets_tool,
)
from app.utils.langsmith_manger import LangSmithManager

_langsmith_manager = LangSmithManager()


def get_twitter_agent(
    llm: BaseChatModel,
) -> CompiledGraph:
    """Get a twitter agent.

    Args:
        llm (BaseChatModel): LLM model to use

    Returns:
        CompiledGraph: Generated twitter agent
    """
    return create_react_agent(
        model=llm,
        tools=[
            get_twitter_post_tool(),
            get_twitter_user_tweets_tool(),
            get_twitter_delete_tool(),
        ],
        prompt=_langsmith_manager.get_agent_prompt(
            AGENT_PROMPT_NAME, tweets_max_results=TWEETS_MAX_RESULTS
        ),
        name=AGENT_NAME,
    )


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = get_twitter_agent(llm)

    # Test
    # response = agent.invoke({"messages": [{"role": "user", "content": "트위터에 반가움을 표하는 트윗을 올려줘"}]})
    response = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "트위터에 반가움을 표현했던 트윗을 삭제해줘"},
                {
                    "role": "assistant",
                    "content": """최근 트윗에서 반가움을 표현한 내용은 다음과 같습니다:

> **안녕하세요, 여러분! 여러분과 소통하게 되어 정말 반갑습니다! 😊 #환영합니다 #소통**  
> (트윗 ID: 1935964009423159461)

이 트윗을 삭제하시겠습니까? 확인해 주세요.""",
                },
                {"role": "user", "content": "응 삭제할께"},
            ]
        }
    )
