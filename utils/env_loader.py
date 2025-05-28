"""
Environment loader utility for managing configuration and environment variables.
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional


class EnvLoader:
    """Utility class for loading and managing environment variables."""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize the environment loader."""
        self.env_file = env_file
        self.load_environment()
    
    def load_environment(self):
        """Load environment variables from .env file."""
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
    
    def get_api_config(self, environment: str = "uat") -> Dict[str, str]:
        """Get API configuration for specified environment."""
        if environment.lower() == "prod":
            return {
                "api_key": os.getenv("ACUMIDATA_PROD_KEY", ""),
                "base_url": "https://api.acumidata.com"
            }
        else:
            return {
                "api_key": os.getenv("ACUMIDATA_UAT_KEY", ""),
                "base_url": "https://uat.api.acumidata.com"
            }
    
    def get_database_config(self) -> Dict[str, str]:
        """Get database configuration from environment variables."""
        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", "datanest"),
            "username": os.getenv("DB_USER", ""),
            "password": os.getenv("DB_PASSWORD", "")
        }
    
    def get_app_config(self) -> Dict[str, Any]:
        """Get general application configuration."""
        return {
            "debug": os.getenv("DEBUG", "False").lower() == "true",
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "secret_key": os.getenv("SECRET_KEY", "default-secret-key"),
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    
    @staticmethod
    def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a specific environment variable with optional default."""
        return os.getenv(key, default)
    
    @staticmethod
    def set_env_var(key: str, value: str):
        """Set an environment variable."""
        os.environ[key] = value
    
    def validate_required_vars(self, required_vars: list) -> Dict[str, bool]:
        """Validate that required environment variables are set."""
        validation_results = {}
        
        for var in required_vars:
            validation_results[var] = bool(os.getenv(var))
        
        return validation_results 