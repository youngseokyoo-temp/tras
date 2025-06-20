from langchain_core.language_models import BaseChatModel
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

from app.agents.calendar_agent.constants import AGENT_NAME, AGENT_PROMPT_NAME
from app.agents.calendar_agent.tools import (
    get_calendar_create_event_tool,
    get_calendar_delete_event_tool,
    get_calendar_search_events_tool,
    get_calendar_update_event_tool,
    get_calendars_info_tool,
    get_current_datetime_tool,
)
from app.utils.langsmith_manger import LangSmithManager

_langsmith_manager = LangSmithManager()

def get_calendar_agent(
    llm: BaseChatModel,
) -> CompiledGraph:
    """Get a calendar agent.

    Args:
        llm (BaseChatModel): LLM model to use

    Returns:
        CompiledGraph: Generated calendar agent
        """
    return create_react_agent(
        model=llm,
        tools=[
            get_calendar_create_event_tool(),
            get_calendar_delete_event_tool(),
            get_calendar_update_event_tool(),
            get_current_datetime_tool(),
            get_calendar_search_events_tool(),
            get_calendars_info_tool(),
        ],
        prompt=_langsmith_manager.get_agent_prompt(AGENT_PROMPT_NAME),
        name=AGENT_NAME,
    )


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = get_calendar_agent(llm)

    # Test
    response = agent.invoke({"messages": [{"role": "user", "content": "2026년의 1/13일부터 1/15일까지 일정 등록해줘"}, {"role": "assistant", "content": """

일정이 등록되었습니다. 

- **제목**: 여행
- **시작 시간**: 2026년 1월 13일 00:00
- **종료 시간**: 2026년 1월 15일 23:59
- [이벤트 링크](https://www.google.com/calendar/event?eid=bHMwNjk3c2drb2ppb2hjMzA0aDNhMGxpYzAgcmljaHBpbkBnLnNra3UuZWR1)

이벤트를 수정할 필요가 있나요?"""}, {"role": "user", "content": "수정할 필요가 없어. 이벤트 삭제해줘"}]})
    print(response)