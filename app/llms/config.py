from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ModelConfig:
    """Model configuration"""
    provider: str
    model_name: str
    temperature: float = 0.5

# OpenAI Model Configs
CHATGPT_MODELS = OrderedDict({
    "GPT-4o-mini": ModelConfig(
        provider="openai",
        model_name="gpt-4o-mini",
        temperature=0.5,
    ),
    "GPT-4.1-mini": ModelConfig(
        provider="openai",
        model_name="gpt-4.1-mini",
        temperature=0.5,
    ),
    "GPT-4o": ModelConfig(
        provider="openai",
        model_name="gpt-4o",
        temperature=0.5,
    ),
})

# Anthropic Model Configs
ANTHROPIC_MODELS = OrderedDict({
    "Claude-3-Opus": ModelConfig(
        provider="anthropic",
        model_name="claude-3-opus-20240229",
        temperature=0.5,
    ),
    "Claude-3-Sonnet": ModelConfig(
        provider="anthropic",
        model_name="claude-3-sonnet-20240229",
        temperature=0.5,
    ),
    "Claude-3-Haiku": ModelConfig(
        provider="anthropic",
        model_name="claude-3-haiku-20240307",
        temperature=0.5,
    )
})

# Gemini Model Configs
GEMINI_MODELS = OrderedDict({
    "Gemini 1.5 Pro": ModelConfig(
        provider="google",
        model_name="gemini-1.5-pro-latest",
        temperature=0.5,
    ),
    "Gemini 2.0 Flash": ModelConfig(
        provider="google",
        model_name="gemini-1.5-flash-latest",
        temperature=0.5,
    ),
    "Gemini 1.5 Flash": ModelConfig(
        provider="google",
        model_name="gemini-1.5-flash-latest",
        temperature=0.5,
    ),
})

AVAILABLE_MODELS: Dict[str, Dict[str, ModelConfig]] = {
    "OpenAI - ChatGPT": CHATGPT_MODELS,
    "Anthropic - Claude": ANTHROPIC_MODELS,
    "Google - Gemini": GEMINI_MODELS
}

def get_model_versions(model_provider: str) -> List[str]:
    """Return all model versions for a given provider"""
    return list(AVAILABLE_MODELS.get(model_provider, {}).keys())

def get_model_config(model_provider: str, model_version: str) -> ModelConfig:
    """Return the configuration for a given model"""
    provider_models = AVAILABLE_MODELS.get(model_provider, {})
    if model_version not in provider_models:
        raise ValueError(f"Unsupported model: {model_provider}/{model_version}")
    return provider_models[model_version] 