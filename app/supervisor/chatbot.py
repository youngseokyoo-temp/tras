from typing import Annotated

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.checkpoint.base import Checkpoint
from langgraph.graph import END, START
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.message import MessagesState, StateGraph
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langmem.short_term import SummarizationNode

from app.agents.calendar_agent.agent import get_calendar_agent
from app.agents.calendar_agent.constants import AGENT_NAME as CALENDAR_AGENT_NAME
from app.agents.planner_agent.agent import get_planner_agent
from app.agents.planner_agent.constants import AGENT_NAME as PLANNER_AGENT_NAME
from app.agents.research_agent.agent import get_research_agent
from app.agents.research_agent.constants import AGENT_NAME as RESEARCH_AGENT_NAME
from app.agents.twitter_agent.agent import get_twitter_agent
from app.agents.twitter_agent.constants import AGENT_NAME as TWITTER_AGENT_NAME
from app.supervisor.constants import MAX_SUMMARY_TOKENS, SUPERVISOR_NAME, SUPERVISOR_PROMPT_NAME
from app.utils.create_react_agent import create_react_agent
from app.utils.langsmith_manger import LangSmithManager
from app.supervisor.hooks import guard_using_llamaguard

_langsmith_manager = LangSmithManager()


def create_handoff_tool(*, agent_name: str, description: str | None = None):
    name = f"transfer_to_{agent_name}"
    description = description or f"Ask {agent_name} for help."

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": name,
            "tool_call_id": tool_call_id,
        }

        return Command(
            goto=agent_name,
            update={**state, "messages": state["messages"] + [tool_message]},
            graph=Command.PARENT,
        )

    return handoff_tool


def get_supervisor_chatbot(
    llm: BaseChatModel,
    checkpointer: Checkpoint,
) -> CompiledGraph:
    """Get a supervisor agent.

    Args:
        llm (BaseChatModel): LLM model to use

    Returns:
        CompiledGraph: Generated supervisor agent
    """
    # Agents
    research_agent = get_research_agent(llm)
    planner_agent = get_planner_agent(llm)
    calendar_agent = get_calendar_agent(llm)
    twitter_agent = get_twitter_agent(llm)

    # Handoffs
    assign_to_research_agent = create_handoff_tool(agent_name=RESEARCH_AGENT_NAME)
    assign_to_planner_agent = create_handoff_tool(agent_name=PLANNER_AGENT_NAME)
    assign_to_calendar_agent = create_handoff_tool(agent_name=CALENDAR_AGENT_NAME)
    assign_to_twitter_agent = create_handoff_tool(agent_name=TWITTER_AGENT_NAME)

    # History Summarization
    summarization_node = SummarizationNode(
        model=llm,
        max_tokens=MAX_SUMMARY_TOKENS,
        token_counter=llm.get_num_tokens_from_messages,
    )

    supervisor_agent = create_react_agent(
        model=llm,
        tools=[
            assign_to_planner_agent,
            assign_to_research_agent,
            assign_to_calendar_agent,
            assign_to_twitter_agent,
        ],
        prompt=_langsmith_manager.get_agent_prompt(SUPERVISOR_PROMPT_NAME),
        name=SUPERVISOR_NAME,
        pre_model_hook=summarization_node,
        post_model_hook=guard_using_llamaguard,
    )

    return (
        StateGraph(MessagesState)
        .add_node(
            SUPERVISOR_NAME,
            supervisor_agent,
            destinations=(
                RESEARCH_AGENT_NAME,
                PLANNER_AGENT_NAME,
                CALENDAR_AGENT_NAME,
                TWITTER_AGENT_NAME,
            )
            + (END,),
        )
        .add_node(RESEARCH_AGENT_NAME, research_agent)
        .add_node(PLANNER_AGENT_NAME, planner_agent)
        .add_node(CALENDAR_AGENT_NAME, calendar_agent)
        .add_node(TWITTER_AGENT_NAME, twitter_agent)
        .add_edge(START, SUPERVISOR_NAME)
        .add_edge(RESEARCH_AGENT_NAME, SUPERVISOR_NAME)
        .add_edge(PLANNER_AGENT_NAME, SUPERVISOR_NAME)
        .add_edge(CALENDAR_AGENT_NAME, SUPERVISOR_NAME)
        .add_edge(TWITTER_AGENT_NAME, SUPERVISOR_NAME)
        .compile(checkpointer=checkpointer)
    )


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI
    from IPython.display import display, Image
    chatbot = get_supervisor_chatbot(llm=ChatOpenAI(model="gpt-4o-mini"), checkpointer=None)
    display(Image(chatbot.get_graph().draw_mermaid_png(output_file_path="supervisor.png")))
