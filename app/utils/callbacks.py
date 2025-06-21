from langchain_core.callbacks import BaseCallbackHandler

from app.utils.logger import get_logger


class LoggingCallback(BaseCallbackHandler):

    def __init__(self, session_id: str):
        self.logger = get_logger(session_id)

    def _on_llm_error(self, error, **kwargs):
        self.logger.error(f"LLM Error: {error}")

    def _on_tool_error(self, error, **kwargs):
        self.logger.error(f"Tool Error: {error}")



