from functools import lru_cache
from typing import Optional

from langchain_core.messages import SystemMessage
from langsmith import Client

from app.utils.env_constants import LANGSMITH_API_KEY


class LangSmithManager:
    """Singleton class to manage LangSmith client."""

    _instance: Optional["LangSmithManager"] = None
    _client: Optional[Client] = None

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def client(self) -> Client:
        """Return LangSmith client instance (lazy initialization)"""
        if self._client is None:
            if not LANGSMITH_API_KEY:
                raise ValueError("LANGSMITH_API_KEY가 설정되지 않았습니다.")
            self._client = Client(api_key=LANGSMITH_API_KEY)
        return self._client

    @lru_cache(maxsize=100)
    def get_agent_prompt(self, name: str, **kwargs) -> SystemMessage:
        """Get a prompt from LangSmith."""
        try:
            chat_prompt = self.client.pull_prompt(name, include_model=False)
            return chat_prompt.messages[0].format(**kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to get prompt '{name}': {str(e)}")

    def reset_client(self):
        """Reset client (for testing)"""
        self._client = None
