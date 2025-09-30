"""
Flag evaluation functions for LaunchDarkly.

Best Practice: Safe evaluation that never blocks or crashes.
Always returns a value, even if LaunchDarkly is unavailable.
"""
from ldclient import Context
import logging

logger = logging.getLogger(__name__)


def safe_variation(flag_key, context, default_value=False):
    """
    Safely evaluate a feature flag.
    
    Best Practice: variation() - Manages types and returns value without
    interrupting events. Never blocks, always returns a value.
    
    Args:
        flag_key: Feature flag key
        context: User context
        default_value: Default value if evaluation fails
        
    Returns:
        Flag value or default
    """
    try:
        from .launchdarkly import get_ld_client, is_ld_ready
        
        if not is_ld_ready():
            logger.debug(f"LD not ready, using default for '{flag_key}'")
            return default_value
        
        client = get_ld_client()
        if not client:
            return default_value
            
        value = client.variation(flag_key, context, default_value)
        logger.debug(f"Flag '{flag_key}' evaluated to: {value}")
        return value
        
    except Exception as e:
        logger.error(f"Flag evaluation failed for '{flag_key}': {e}")
        return default_value


def safe_variation_detail(flag_key, context, default_value=False):
    """
    Safely evaluate a feature flag with detailed information.
    
    Best Practice: Returns detailed evaluation info including reason.
    
    Args:
        flag_key: Feature flag key
        context: User context
        default_value: Default value if evaluation fails
        
    Returns:
        EvaluationDetail object with value, variation_index, and reason
    """
    try:
        from .launchdarkly import get_ld_client, is_ld_ready
        
        if not is_ld_ready():
            logger.debug(f"LD not ready, using default for '{flag_key}'")
            # Return a simple object with default value
            class DefaultDetail:
                def __init__(self, value):
                    self.value = value
                    self.variation_index = None
                    self.reason = {'kind': 'DEFAULT', 'message': 'LaunchDarkly not initialized'}
            return DefaultDetail(default_value)
        
        client = get_ld_client()
        if not client:
            class DefaultDetail:
                def __init__(self, value):
                    self.value = value
                    self.variation_index = None
                    self.reason = {'kind': 'ERROR', 'message': 'Client not available'}
            return DefaultDetail(default_value)
            
        detail = client.variation_detail(flag_key, context, default_value)
        logger.debug(f"Flag '{flag_key}' detail: {detail.value}, reason: {detail.reason}")
        return detail
        
    except Exception as e:
        logger.error(f"Flag detail evaluation failed for '{flag_key}': {e}")
        class ErrorDetail:
            def __init__(self, value):
                self.value = value
                self.variation_index = None
                self.reason = {'kind': 'ERROR', 'message': str(e)}
        return ErrorDetail(default_value)


def add_flag_listener(flag_key, context, callback):
    """
    Add a real-time flag change listener.
    
    Args:
        flag_key: Feature flag key
        context: User context
        callback: Callback function for flag changes
        
    Returns:
        Listener handle or None
    """
    try:
        from .launchdarkly import get_ld_client, is_ld_ready
        
        if not is_ld_ready():
            logger.warning("Cannot add listener - LD not ready")
            return None
        
        client = get_ld_client()
        if not client:
            return None
            
        listener = client.flag_tracker.add_flag_value_change_listener(
            flag_key, context, callback
        )
        logger.info(f"Added listener for flag: {flag_key}")
        return listener
        
    except Exception as e:
        logger.error(f"Failed to add flag listener: {e}")
        return None
