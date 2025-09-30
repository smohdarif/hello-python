"""
Configuration management for LaunchDarkly Python Demo.

Best Practice: Environment-aware configuration with validation.
Follows LaunchDarkly recommended patterns for getSDKKey() and getLDConfig().
"""
import os
from dotenv import load_dotenv
from ldclient.config import Config
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


def get_sdk_key():
    """
    Get LaunchDarkly SDK key from environment.
    
    Best Practice: getSDKKey() - Retrieving SDK key for execution environment.
    Returns the correct key for the environment that the application is being run.
    
    Returns:
        str: SDK key from environment
        
    Raises:
        ValueError: If SDK key is not set
    """
    sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')
    
    if not sdk_key:
        raise ValueError(
            "LAUNCHDARKLY_SDK_KEY environment variable is required. "
            "Please set it in your .env file or environment."
        )
    
    return sdk_key


def load_app_config():
    """
    Load application configuration from environment.
    
    Note: User context details are NOT loaded here - they should be passed
    dynamically when building contexts using context.py functions.
    
    Returns:
        dict: Configuration dictionary with app settings
    """
    config = {
        # LaunchDarkly settings
        'sdk_key': os.getenv('LAUNCHDARKLY_SDK_KEY'),
        'flag_key': os.getenv('LAUNCHDARKLY_FLAG_KEY', 'sample-feature'),
        
        # Application settings
        'ci_mode': os.getenv('CI') is not None,
        
        # Network settings
        'https_proxy': os.getenv('HTTPS_PROXY'),
        'init_timeout': float(os.getenv('LD_INIT_TIMEOUT', '5.0')),
        'connect_timeout': float(os.getenv('LD_CONNECT_TIMEOUT', '10.0')),
        'read_timeout': float(os.getenv('LD_READ_TIMEOUT', '15.0')),
    }
    
    return config


def get_ld_config(sdk_key, connect_timeout=10.0, read_timeout=15.0):
    """
    Create LaunchDarkly Config object with proper settings.
    
    Best Practice: getLDConfig() - Create wrapper around configuration settings
    that may need to be managed by environment.
    
    Args:
        sdk_key: LaunchDarkly SDK key
        connect_timeout: Connection timeout in seconds
        read_timeout: Read timeout in seconds
        
    Returns:
        Config: LaunchDarkly configuration object
    """
    https_proxy = os.getenv('HTTPS_PROXY')
    
    config_args = {
        'sdk_key': sdk_key,
        'connect_timeout': connect_timeout,
        'read_timeout': read_timeout,
    }
    
    # Add proxy if configured
    if https_proxy:
        config_args['http_proxy'] = https_proxy
        logger.info(f"Using HTTPS proxy: {https_proxy}")
    
    return Config(**config_args)


def validate_config(config):
    """
    Validate required configuration values.
    
    Args:
        config: Configuration dictionary
        
    Raises:
        ValueError: If required configuration is missing or invalid
    """
    required_fields = ['sdk_key', 'flag_key']
    
    for field in required_fields:
        if not config.get(field):
            raise ValueError(f"Required configuration '{field}' is missing")
    
    # Validate timeout values
    if config.get('init_timeout', 0) <= 0:
        raise ValueError("init_timeout must be greater than 0")
    
    logger.info("Configuration validated successfully")
