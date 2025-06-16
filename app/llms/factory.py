import streamlit as st
from typing import Any, List

from llms.config import get_model_config, ModelConfig

class LLMFactory:
    
    def __init__(self):
        self._cache = {}
    
    def get_llm(self, provider: str, version: str, **kwargs) -> Any:
        cache_key = f"{provider}_{version}"
        if cache_key  in self._cache:
            return self._cache[cache_key]
        
        config = get_model_config(provider, version)
        llm = self._create_llm(config, **kwargs)
        self._cache[cache_key] = llm 
        return llm
    
    def _create_llm(self, config: ModelConfig, **kwargs) -> Any:
        if config.provider == "openai":
            return self._create_openai_llm(config, **kwargs)
        elif config.provider == "anthropic":
            return self._create_anthropic_llm(config, **kwargs)
        elif config.provider == "google":
            return self._create_google_llm(config, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")
    
    def _create_openai_llm(self, config: ModelConfig, **kwargs):
        from langchain_openai import ChatOpenAI
            
        return ChatOpenAI(
            model=config.model_name,
            temperature=kwargs.get('temperature', config.temperature),
            max_tokens=kwargs.get('max_tokens', config.max_tokens),
            streaming=True,
            **{k: v for k, v in kwargs.items() if k not in ['temperature', 'max_tokens', 'streaming']}
        )
    
    def _create_anthropic_llm(self, config: ModelConfig, **kwargs):
        from langchain_anthropic import ChatAnthropic
            
        return ChatAnthropic(
            model=config.model_name,
            temperature=kwargs.get('temperature', config.temperature),
            max_tokens=kwargs.get('max_tokens', config.max_tokens),
            streaming=True,
            **{k: v for k, v in kwargs.items() if k not in ['temperature', 'max_tokens', 'streaming']}
        )
    
    def _create_google_llm(self, config: ModelConfig, **kwargs):
        from langchain_google_genai import ChatGoogleGenerativeAI
            
        return ChatGoogleGenerativeAI(
            model=config.model_name,
            temperature=kwargs.get('temperature', config.temperature),
            max_tokens=kwargs.get('max_tokens', config.max_tokens),
            streaming=True,
            **{k: v for k, v in kwargs.items() if k not in ['temperature', 'max_tokens', 'streaming']}
        )
    
    def clear_cache(self):
        self._cache.clear()
    
    def get_cache_info(self) -> List[str]:
        return {
            "cached_models": len(self._cache),
            "cache_keys": list(self._cache.keys())
        }

# Global factory instance
_factory = LLMFactory()

@st.cache_resource
def get_llm_factory() -> LLMFactory:
    return _factory

def get_llm_instance(log, provider: str, version: str, **kwargs) -> Any:
    """Get an LLM instance from the factory"""
    try:
        factory = get_llm_factory()
        return factory.get_llm(provider, version, **kwargs)
    except Exception as e:
        log.exception(f"Error loading model: {e}")
        return None

def clear_llm_cache():
    factory = get_llm_factory()
    factory.clear_cache()
    st.cache_resource.clear()

def get_cache_info():
    factory = get_llm_factory()
    return factory.get_cache_info() 