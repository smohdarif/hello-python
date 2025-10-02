"""
LaunchDarkly client management functions.

Best Practices:
- Singleton pattern (getLDClient)
- Non-blocking initialization
- Graceful shutdown
"""
import ldclient
from ldclient.config import Config
import atexit
import signal
import sys
import logging

logger = logging.getLogger(__name__)


def init_ld_client(sdk_key, wait_seconds=5):
    """
    Initialize LaunchDarkly client with non-blocking pattern.
    
    Best Practice: Non-blocking initialization - App continues even if LD unavailable.
    
    Args:
        sdk_key: LaunchDarkly SDK key
        wait_seconds: Max seconds to wait for initialization
        
    Returns:
        bool: True if initialized, False otherwise
    """
    logger.info("📍 FLOW [2/6]: launchdarkly.init_ld_client() - Initializing LaunchDarkly client")
    logger.info(f"   ↳ Using SDK key: {sdk_key[:10]}...{sdk_key[-4:]}")
    logger.info(f"   ↳ Wait timeout: {wait_seconds}s (NON-BLOCKING)")
    
    try:
        # Create config and set it
        logger.debug("   ↳ Creating Config object...")
        config = Config(sdk_key)
        logger.debug("   ↳ Calling ldclient.set_config()...")
        ldclient.set_config(config)
        
        # Get client instance
        logger.debug("   ↳ Getting client instance with ldclient.get()...")
        client = ldclient.get()
        
        # Wait briefly, but don't block forever
        if client.is_initialized():
            logger.info("✓ LaunchDarkly SDK initialized successfully")
            return True
        else:
            logger.warning(
                f"⚠ LaunchDarkly not ready after {wait_seconds}s, "
                "using default values"
            )
            return False
            
    except Exception as e:
        logger.error(f"✗ LaunchDarkly initialization failed: {e}")
        return False


def get_ld_client():
    """
    Get LaunchDarkly client singleton instance.
    
    Best Practice: getLDClient() - Overarching call to manage client.
    
    Returns:
        Client: LaunchDarkly client instance or None
    """
    try:
        return ldclient.get()
    except Exception as e:
        logger.error(f"Error getting LD client: {e}")
        return None


def is_ld_ready():
    """
    Check if LaunchDarkly client is initialized and ready.
    
    Returns:
        bool: True if ready, False otherwise
    """
    try:
        client = ldclient.get()
        return client.is_initialized() if client else False
    except:
        return False


def close_ld_client():
    """
    Close LaunchDarkly client gracefully.
    
    Best Practice: Graceful shutdown with proper cleanup.
    """
    try:
        client = ldclient.get()
        if client:
            client.close()
            logger.info("LaunchDarkly client closed gracefully")
    except Exception as e:
        logger.error(f"Error closing LD client: {e}")


def setup_graceful_shutdown():
    """
    Setup graceful shutdown handlers.
    
    Best Practice: Ensures cleanup on application exit.
    """
    # Register cleanup on exit
    atexit.register(close_ld_client)
    
    # Register signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f"\nReceived signal {signum}, shutting down gracefully...")
        close_ld_client()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.debug("Graceful shutdown handlers registered")
