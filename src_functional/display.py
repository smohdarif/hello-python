"""
Display and formatting functions for LaunchDarkly demo.
Simple, clean output functions.
"""


def show_basic_result(flag_key, value):
    """
    Display basic flag evaluation result.
    
    Args:
        flag_key: Flag key
        value: Flag value
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"📍 FLOW [5/6]: display.show_basic_result() - Displaying result")
    logger.info(f"   ↳ Flag: '{flag_key}' = {value}")
    
    print()
    print(f"*** The {flag_key} feature flag evaluates to {value}")
    
    if value:
        logger.info("   ↳ Value is True, showing banner...")
        show_banner()
    
    logger.info("✓ Basic result displayed")


def show_detailed_result(flag_key, detail):
    """
    Display detailed flag evaluation result.
    
    Args:
        flag_key: Flag key
        detail: EvaluationDetail object
    """
    print()
    print("=" * 60)
    print(f"*** DETAILED FLAG EVALUATION: {flag_key}")
    print("=" * 60)
    print(f"*** Value: {detail.value}")
    print(f"*** Variation Index: {detail.variation_index}")
    print(f"*** Reason: {detail.reason}")
    
    # Show evaluation type
    if hasattr(detail, 'reason') and detail.reason:
        reason_kind = detail.reason.get('kind', 'UNKNOWN')
        print(f"*** Evaluation Type: {reason_kind}")
        
        if reason_kind == 'TARGET_MATCH':
            print("*** User matched targeting rule")
        elif reason_kind == 'FALLTHROUGH':
            print("*** Using fallthrough variation")
        elif reason_kind == 'OFF':
            print("*** Flag is turned OFF")
        elif reason_kind == 'DEFAULT':
            print("*** Using default value (LD not ready)")
        elif reason_kind == 'ERROR':
            print(f"*** Error: {detail.reason.get('message', 'Unknown')}")
    
    print("=" * 60)
    
    if detail.value:
        show_banner()


def show_banner():
    """Display LaunchDarkly ASCII banner."""
    print()
    print("        ██       ")
    print("          ██     ")
    print("      ████████   ")
    print("         ███████ ")
    print("██ LAUNCHDARKLY █")
    print("         ███████ ")
    print("      ████████   ")
    print("          ██     ")
    print("        ██       ")
    print()


def show_section_header(title):
    """
    Display a section header.
    
    Args:
        title: Section title
    """
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def show_monitoring_info():
    """Display real-time monitoring information."""
    print()
    print("*** Monitoring for flag changes...")
    print("*** Toggle your flag in LaunchDarkly dashboard to see changes")
    print("*** Press Ctrl+C to exit")


def show_initialization_status(is_ready, elapsed_time=None):
    """
    Display initialization status.
    
    Args:
        is_ready: Whether LD is ready
        elapsed_time: Time taken to initialize (optional)
    """
    if is_ready:
        msg = "✓ LaunchDarkly is ready"
        if elapsed_time:
            msg += f" (initialized in {elapsed_time:.2f}s)"
        print(msg)
    else:
        print("⚠ LaunchDarkly not ready - using default flag values")
        print("  (This is OK! Your app continues to work)")
