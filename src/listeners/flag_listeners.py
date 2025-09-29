"""
Flag change listeners for LaunchDarkly demo.
Handles real-time flag change events.
"""
from typing import Any
from ..utils.display import DisplayUtils
from ..services.launchdarkly_service import LaunchDarklyService
from ldclient import Context


class BasicFlagListener:
    """Basic flag change listener for simple evaluations."""
    
    def __init__(self):
        self.display = DisplayUtils()
    
    def on_flag_change(self, flag_change: Any):
        """
        Handle flag change event with basic display.
        
        Args:
            flag_change: Flag change event object
        """
        self.display.show_basic_result(flag_change.key, flag_change.new_value)


class DetailedFlagListener:
    """Detailed flag change listener with full evaluation details."""
    
    def __init__(self, ld_service: LaunchDarklyService, user_context: dict):
        """
        Initialize detailed flag listener.
        
        Args:
            ld_service: LaunchDarkly service instance
            user_context: User context configuration
        """
        self.ld_service = ld_service
        self.user_context = user_context
        self.display = DisplayUtils()
    
    def on_flag_change(self, flag_change: Any):
        """
        Handle flag change event with detailed evaluation.
        
        Args:
            flag_change: Flag change event object
        """
        try:
            # Create context for evaluation
            context = self._create_context()
            
            # Get detailed evaluation
            detail = self.ld_service.evaluate_flag_detail(
                flag_change.key, context, False
            )
            
            # Display detailed result
            self.display.show_detailed_result(flag_change.key, detail)
            
        except Exception as e:
            print(f"*** Error in flag change listener: {e}")
            # Fallback to basic display
            self.display.show_basic_result(flag_change.key, flag_change.new_value)
    
    def _create_context(self) -> Context:
        """Create user context for flag evaluation."""
        return Context.builder(self.user_context['key'])\
            .kind(self.user_context['kind'])\
            .name(self.user_context['name'])\
            .build()
