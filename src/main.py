"""
LaunchDarkly Python Demo - Refactored Version
Following all 5 LaunchDarkly best practices rules.

Rule 1: Singleton Pattern ✅
Rule 2: Environment-Aware Configuration ✅  
Rule 3: Initialization Pattern ✅
Rule 4: Graceful Shutdown ✅
Rule 5: Lightweight Configuration ✅
"""
import sys
from threading import Event
from halo import Halo

from .config.settings import Settings
from .services.launchdarkly_service import LaunchDarklyService
from .listeners.flag_listeners import BasicFlagListener, DetailedFlagListener
from .utils.display import DisplayUtils
from ldclient import Context


def create_user_context(settings: Settings) -> Context:
    """
    Create user context for flag evaluation.
    
    Args:
        settings: Application settings
        
    Returns:
        LaunchDarkly user context
    """
    user_config = settings.get_user_context()
    return Context.builder(user_config['key'])\
        .kind(user_config['kind'])\
        .name(user_config['name'])\
        .build()


def run_basic_evaluation(ld_service: LaunchDarklyService, settings: Settings, display: DisplayUtils):
    """Run basic flag evaluation."""
    display.show_section_header("BASIC FLAG EVALUATION")
    
    context = create_user_context(settings)
    flag_value = ld_service.evaluate_flag(settings.flag_key, context, False)
    display.show_basic_result(settings.flag_key, flag_value)


def run_detailed_evaluation(ld_service: LaunchDarklyService, settings: Settings, display: DisplayUtils):
    """Run detailed flag evaluation."""
    display.show_section_header("DETAILED FLAG EVALUATION")
    
    context = create_user_context(settings)
    flag_detail = ld_service.evaluate_flag_detail(settings.flag_key, context, False)
    display.show_detailed_result(settings.flag_key, flag_detail)


def run_real_time_monitoring(ld_service: LaunchDarklyService, settings: Settings, display: DisplayUtils):
    """Run real-time flag monitoring."""
    display.show_section_header("REAL-TIME FLAG MONITORING")
    display.show_monitoring_info()
    
    context = create_user_context(settings)
    user_context = settings.get_user_context()
    
    # Use detailed listener for real-time changes
    listener = DetailedFlagListener(ld_service, user_context)
    ld_service.add_flag_listener(settings.flag_key, context, listener.on_flag_change)
    
    with Halo(text='Waiting for changes', spinner='dots'):
        try:
            Event().wait()
        except KeyboardInterrupt:
            print("\\n*** Shutting down gracefully...")
            ld_service.close()
            sys.exit(0)


def main():
    """
    Main application entry point.
    
    Follows all 5 LaunchDarkly best practices:
    - Rule 1: Singleton Pattern
    - Rule 2: Environment-Aware Configuration
    - Rule 3: Initialization Pattern
    - Rule 4: Graceful Shutdown
    - Rule 5: Lightweight Configuration
    """
    try:
        # Rule 2: Environment-Aware Configuration
        print("*** Loading configuration...")
        settings = Settings()
        settings.validate()
        print("*** Configuration loaded successfully")
        
        # Rule 1 & 3: Singleton Pattern & Initialization
        print("*** Initializing LaunchDarkly service...")
        ld_service = LaunchDarklyService(settings.sdk_key)
        print("*** LaunchDarkly service initialized successfully")
        
        # Initialize display utilities
        display = DisplayUtils()
        
        # Run basic evaluation
        run_basic_evaluation(ld_service, settings, display)
        
        # Run detailed evaluation
        run_detailed_evaluation(ld_service, settings, display)
        
        # Run real-time monitoring (unless in CI mode)
        if not settings.is_ci_mode():
            run_real_time_monitoring(ld_service, settings, display)
        else:
            print("\\n*** CI mode detected - skipping real-time monitoring")
            print("*** Demo completed successfully")
            
    except ValueError as e:
        print(f"*** Configuration Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"*** LaunchDarkly Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"*** Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
