"""
LaunchDarkly Python Demo - Function-Based Architecture

Demonstrates all LaunchDarkly best practices with simple functions.
"""
import time
from threading import Event
from halo import Halo
import logging

from .config import get_sdk_key, load_app_config, validate_config
from .launchdarkly import init_ld_client, is_ld_ready, setup_graceful_shutdown
from .context import build_demo_context, build_user_context
from .evaluation import safe_variation, safe_variation_detail, add_flag_listener
from .display import (
    show_basic_result, show_detailed_result, show_section_header,
    show_monitoring_info, show_initialization_status
)
from .listeners import on_basic_flag_change

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def run_basic_evaluation(flag_key, context):
    """
    Run basic flag evaluation demo.
    
    Args:
        flag_key: Feature flag key
        context: User context
    """
    show_section_header("BASIC FLAG EVALUATION")
    
    # Safe evaluation - works even if LD not ready
    flag_value = safe_variation(flag_key, context, False)
    show_basic_result(flag_key, flag_value)


def run_detailed_evaluation(flag_key, context):
    """
    Run detailed flag evaluation demo.
    
    Args:
        flag_key: Feature flag key
        context: User context
    """
    show_section_header("DETAILED FLAG EVALUATION")
    
    # Get detailed evaluation with reason
    flag_detail = safe_variation_detail(flag_key, context, False)
    show_detailed_result(flag_key, flag_detail)


def run_real_time_monitoring(flag_key, context):
    """
    Run real-time flag monitoring demo.
    
    Args:
        flag_key: Feature flag key
        context: User context
    """
    show_section_header("REAL-TIME FLAG MONITORING")
    show_monitoring_info()
    
    # Add listener for flag changes
    listener = add_flag_listener(flag_key, context, on_basic_flag_change)
    
    if not listener:
        print("⚠ Could not start monitoring (LD not ready)")
        return
    
    # Wait for changes
    with Halo(text='Waiting for changes', spinner='dots'):
        try:
            Event().wait()
        except KeyboardInterrupt:
            print("\n*** Shutting down gracefully...")


def main():
    """
    Main application entry point.
    
    Demonstrates:
    - Non-blocking initialization
    - Safe flag evaluation
    - Real-time monitoring
    - Graceful shutdown
    """
    print("\n" + "=" * 60)
    print("LaunchDarkly Python Demo - Function-Based Architecture")
    print("=" * 60)
    
    try:
        # Load and validate configuration
        print("\n*** Loading configuration...")
        config = load_app_config()
        validate_config(config)
        sdk_key = get_sdk_key()
        print("✓ Configuration loaded")
        
        # Setup graceful shutdown
        setup_graceful_shutdown()
        
        # Initialize LaunchDarkly (non-blocking)
        print("\n*** Initializing LaunchDarkly...")
        start_time = time.time()
        is_ready = init_ld_client(sdk_key, wait_seconds=5)
        elapsed = time.time() - start_time
        
        # Show initialization status
        show_initialization_status(is_ready, elapsed)
        
        # Build user context (for demo, using simple context)
        # In real app: context = build_user_context(user.id, user.name, email=user.email)
        context = build_demo_context()
        print(f"✓ Using demo context: example-user-key (Sandy)")
        
        # Run demos
        flag_key = config['flag_key']
        
        # Basic evaluation (works even if LD not ready!)
        run_basic_evaluation(flag_key, context)
        
        # Detailed evaluation
        run_detailed_evaluation(flag_key, context)
        
        # Real-time monitoring (unless in CI mode)
        if not config['ci_mode']:
            run_real_time_monitoring(flag_key, context)
        else:
            print("\n*** CI mode detected - skipping real-time monitoring")
            print("*** Demo completed successfully")
            
    except ValueError as e:
        logger.error(f"Configuration Error: {e}")
        print("\nPlease check your .env file or environment variables")
        return 1
    except KeyboardInterrupt:
        print("\n*** Interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
