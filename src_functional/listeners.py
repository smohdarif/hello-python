"""
Flag change listener callback functions.
Simple callbacks for real-time flag monitoring.
"""
from .display import show_basic_result, show_detailed_result
from .evaluation import safe_variation_detail
import logging

logger = logging.getLogger(__name__)


def on_basic_flag_change(flag_change):
    """
    Simple callback for flag changes.
    
    Args:
        flag_change: Flag change event object
    """
    logger.info(f"Flag changed: {flag_change.key} -> {flag_change.new_value}")
    show_basic_result(flag_change.key, flag_change.new_value)


def on_detailed_flag_change(flag_change, context):
    """
    Detailed callback for flag changes with evaluation details.
    
    Args:
        flag_change: Flag change event object
        context: User context for evaluation
    """
    logger.info(f"Flag changed: {flag_change.key} -> {flag_change.new_value}")
    
    # Get detailed evaluation
    detail = safe_variation_detail(flag_change.key, context, False)
    show_detailed_result(flag_change.key, detail)
