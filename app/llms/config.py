from typing import Dict, List
from dataclasses import dataclass
from collections import OrderedDict

@dataclass
class ModelConfig:
    """Model configuration"""
    provider: str
    model_name: str
    max_tokens: int
    temperature: float = 0.7

# OpenAI Model Configs
CHATGPT_MODELS = OrderedDict({
    "GPT-4o": ModelConfig(
        provider="openai",
        model_name="gpt-4o",
        max_tokens=8192,
        temperature=0.7,
    ),
    "GPT-4-Turbo": ModelConfig(
        provider="openai",
        model_name="gpt-4-turbo-preview",
        max_tokens=128000,
        temperature=0.7,
    ),
    "GPT-3.5-turbo": ModelConfig(
        provider="openai",
        model_name="gpt-3.5-turbo",
        max_tokens=4096,
        temperature=0.7,
    ),
})

# Anthropic Model Configs
ANTHROPIC_MODELS = OrderedDict({
    "Claude-3-Opus": ModelConfig(
        provider="anthropic",
        model_name="claude-3-opus-20240229",
        max_tokens=200000,
        temperature=0.7,
    ),
    "Claude-3-Sonnet": ModelConfig(
        provider="anthropic",
        model_name="claude-3-sonnet-20240229",
        max_tokens=200000,
        temperature=0.7,
    ),
    "Claude-3-Haiku": ModelConfig(
        provider="anthropic",
        model_name="claude-3-haiku-20240307",
        max_tokens=200000,
        temperature=0.7,
    )
})

# Gemini Model Configs
GEMINI_MODELS = OrderedDict({
    "Gemini 1.5 Pro": ModelConfig(
        provider="google",
        model_name="gemini-1.5-pro-latest",
        max_tokens=32768,
        temperature=0.7,
    ),
    "Gemini 1.5 Flash": ModelConfig(
        provider="google",
        model_name="gemini-1.5-flash-latest",
        max_tokens=32768,
        temperature=0.7,
    ),
    "Gemini 1.0 Pro": ModelConfig(
        provider="google",
        model_name="gemini-1.0-pro-latest",
        max_tokens=32768,
        temperature=0.7,
    ),
})

AVAILABLE_MODELS: Dict[str, Dict[str, ModelConfig]] = {
    "OpenAI - ChatGPT": CHATGPT_MODELS,
    "Anthropic - Claude": ANTHROPIC_MODELS,
    "Google - Gemini": GEMINI_MODELS
}

def get_model_versions(provider: str) -> List[str]:
    """Return all model versions for a given provider"""
    return list(AVAILABLE_MODELS.get(provider, {}).keys())

def get_model_config(provider: str, version: str) -> ModelConfig:
    """Return the configuration for a given model"""
    provider_models = AVAILABLE_MODELS.get(provider, {})
    if version not in provider_models:
        raise ValueError(f"Unsupported model: {provider}/{version}")
    return provider_models[version] 