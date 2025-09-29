"""
Configuration management following LaunchDarkly best practices.
Handles environment variables and validation.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application settings following LaunchDarkly Python SDK best practices.
    
    Rule 2: Environment-Aware Configuration
    - Uses os.environ for environment variables
    - Supports HTTPS_PROXY environment variable
    - Python idiomatic configuration methods
    """
    
    def __init__(self):
        """Initialize settings from environment variables."""
        self.sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')
        self.flag_key = os.getenv('LAUNCHDARKLY_FLAG_KEY', 'sample-feature')
        self.ci_mode = os.getenv('CI')
        
        # Proxy configuration (Rule 2)
        self.https_proxy = os.getenv('HTTPS_PROXY')
        
        # User context settings
        self.user_key = os.getenv('LAUNCHDARKLY_USER_KEY', 'example-user-key')
        self.user_name = os.getenv('LAUNCHDARKLY_USER_NAME', 'Sandy')
        self.user_kind = os.getenv('LAUNCHDARKLY_USER_KIND', 'user')
    
    def validate(self):
        """
        Validate required configuration.
        
        Raises:
            ValueError: If required settings are missing
        """
        if not self.sdk_key:
            raise ValueError(
                "LAUNCHDARKLY_SDK_KEY is required. "
                "Please set it in your .env file or environment variables."
            )
        
        if not self.flag_key:
            raise ValueError(
                "LAUNCHDARKLY_FLAG_KEY is required. "
                "Please set it in your .env file or environment variables."
            )
    
    def get_user_context(self):
        """Get user context configuration."""
        return {
            'key': self.user_key,
            'name': self.user_name,
            'kind': self.user_kind
        }
    
    def is_ci_mode(self):
        """Check if running in CI mode."""
        return self.ci_mode is not None
