from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.base import Checkpoint
from langgraph.graph.graph import CompiledGraph
from langgraph_supervisor import create_supervisor

from app.agents.calendar_agent.agent import get_calendar_agent
from app.agents.planner_agent.agent import get_planner_agent
from app.agents.research_agent.agent import get_research_agent
from app.agents.twitter_agent.agent import get_twitter_agent
from app.supervisor.constants import SUPERVISOR_NAME
from app.supervisor.prompts import SUPERVISOR_PROMPT


def get_supervisor_chatbot(
    llm: BaseChatModel,
    llm_worker: BaseChatModel,
    checkpointer: Checkpoint,
) -> CompiledGraph:
    """Get a supervisor agent.

    Args:
        llm (BaseChatModel): LLM model to use

    Returns:
        CompiledGraph: Generated supervisor agent
    """
    return create_supervisor(
        model=llm,
        agents=[
            get_planner_agent(llm_worker),
            get_research_agent(llm_worker),
            get_calendar_agent(llm_worker),
            get_twitter_agent(llm_worker),
        ],
        prompt=SUPERVISOR_PROMPT,
        add_handoff_back_messages=False,
        supervisor_name=SUPERVISOR_NAME,
        output_mode="last_message",
    ).compile(checkpointer=checkpointer)
