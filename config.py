"""
Configuration settings for the Financial Conversational Agent.
"""

import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FinancialAgentConfig:
    """Configuration for the Financial Agent."""
    
    # Model settings
    model_name: str = "gpt-4o-mini"
    max_tokens: int = 2000
    temperature: float = 0.1
    
    # API settings
    api_key: Optional[str] = None
    
    # Data settings
    data_directory: str = "Datasets v2/Datasets v2"
    
    # Analysis settings
    max_retries: int = 3
    timeout_seconds: int = 30
    
    # Logging settings
    log_level: str = "INFO"
    
    def __post_init__(self):
        """Post-initialization setup."""
        # Load API key from environment if not provided
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Validate data directory
        data_path = Path(self.data_directory)
        if not data_path.exists():
            raise ValueError(f"Data directory {self.data_directory} does not exist")
    
    @classmethod
    def from_env(cls) -> "FinancialAgentConfig":
        """Create configuration from environment variables."""
        return cls(
            model_name=os.getenv("FINANCIAL_AGENT_MODEL", "gpt-4o-mini"),
            max_tokens=int(os.getenv("FINANCIAL_AGENT_MAX_TOKENS", "2000")),
            temperature=float(os.getenv("FINANCIAL_AGENT_TEMPERATURE", "0.1")),
            api_key=os.getenv("OPENAI_API_KEY"),
            data_directory=os.getenv("FINANCIAL_AGENT_DATA_DIR", "Datasets v2/Datasets v2"),
            max_retries=int(os.getenv("FINANCIAL_AGENT_MAX_RETRIES", "3")),
            timeout_seconds=int(os.getenv("FINANCIAL_AGENT_TIMEOUT", "30")),
            log_level=os.getenv("FINANCIAL_AGENT_LOG_LEVEL", "INFO")
        )


# Default configuration
DEFAULT_CONFIG = FinancialAgentConfig()


def get_config() -> FinancialAgentConfig:
    """Get the current configuration."""
    return DEFAULT_CONFIG


def update_config(**kwargs) -> None:
    """Update the default configuration."""
    for key, value in kwargs.items():
        if hasattr(DEFAULT_CONFIG, key):
            setattr(DEFAULT_CONFIG, key, value)
        else:
            raise ValueError(f"Unknown configuration key: {key}")


def validate_config(config: FinancialAgentConfig) -> bool:
    """Validate configuration settings."""
    errors = []
    
    # Check required settings
    if not config.api_key:
        errors.append("API key is required")
    
    if not config.model_name:
        errors.append("Model name is required")
    
    if config.max_tokens <= 0:
        errors.append("Max tokens must be positive")
    
    if config.temperature < 0 or config.temperature > 2:
        errors.append("Temperature must be between 0 and 2")
    
    # Check data directory
    data_path = Path(config.data_directory)
    if not data_path.exists():
        errors.append(f"Data directory {config.data_directory} does not exist")
    
    if errors:
        raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
    
    return True 