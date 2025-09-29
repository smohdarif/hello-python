"""
Display utilities for LaunchDarkly demo.
Handles all output formatting and banner display.
"""
from typing import Any


class DisplayUtils:
    """Utility class for displaying LaunchDarkly evaluation results."""
    
    def show_basic_result(self, key: str, value: Any):
        """
        Show basic flag evaluation result.
        
        Args:
            key: Flag key
            value: Flag value
        """
        print()
        print(f"*** The {key} feature flag evaluates to {value}")
        
        if value:
            self.show_banner()
    
    def show_detailed_result(self, key: str, detail: Any):
        """
        Show detailed flag evaluation result with variation details.
        
        Args:
            key: Flag key
            detail: Flag evaluation detail object
        """
        print()
        print("=" * 60)
        print(f"*** DETAILED FLAG EVALUATION: {key}")
        print("=" * 60)
        print(f"*** Value: {detail.value}")
        print(f"*** Variation Index: {detail.variation_index}")
        print(f"*** Reason: {detail.reason}")
        
        # Show additional details based on reason
        if hasattr(detail, 'reason') and detail.reason:
            reason_kind = detail.reason.get('kind', 'UNKNOWN')
            print(f"*** Evaluation Type: {reason_kind}")
            
            if reason_kind == 'RULE_MATCH':
                print(f"*** Matched Rule Index: {detail.reason.get('ruleIndex', 'N/A')}")
            elif reason_kind == 'PREREQUISITE_FAILED':
                print(f"*** Prerequisite Failed: {detail.reason.get('prerequisiteKey', 'N/A')}")
            elif reason_kind == 'FALLTHROUGH':
                print("*** Using fallthrough variation")
            elif reason_kind == 'OFF':
                print("*** Flag is turned OFF")
            elif reason_kind == 'TARGET_MATCH':
                print("*** User matched targeting rule")
            elif reason_kind == 'CLIENT_NOT_READY':
                print("*** Client not ready, using default value")
            elif reason_kind == 'ERROR':
                print(f"*** Error: {detail.reason.get('errorKind', 'Unknown error')}")
            elif reason_kind == 'DEFAULT':
                print("*** Using default value")
        
        print("=" * 60)
        
        if detail.value:
            self.show_banner()
    
    def show_banner(self):
        """Display the LaunchDarkly banner."""
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
    
    def show_section_header(self, title: str):
        """Show a section header."""
        print()
        print("=" * 60)
        print(title)
        print("=" * 60)
    
    def show_monitoring_info(self):
        """Show real-time monitoring information."""
        print()
        print("*** Monitoring for flag changes...")
        print("*** Toggle your flag in LaunchDarkly dashboard to see changes")
        print("*** Press Ctrl+C to exit")
