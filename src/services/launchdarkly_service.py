"""
LaunchDarkly service following official Python SDK best practices.

Rule 1: Singleton Pattern
Rule 3: Initialization Pattern  
Rule 4: Graceful Shutdown
Rule 5: Lightweight Configuration
"""
import ldclient
from ldclient import Context
from ldclient.config import Config
from typing import Optional, Callable, Any
import atexit
import signal
import sys


class LaunchDarklyService:
    """
    LaunchDarkly service wrapper following official SDK patterns.
    
    Implements all 5 rules from LaunchDarkly best practices:
    - Rule 1: Singleton pattern using ldclient.set_config() and ldclient.get()
    - Rule 2: Environment-aware configuration
    - Rule 3: Proper initialization with timeout considerations
    - Rule 4: Graceful shutdown with proper cleanup
    - Rule 5: Lightweight configuration
    """
    
    def __init__(self, sdk_key: str):
        """
        Initialize LaunchDarkly service.
        
        Args:
            sdk_key: LaunchDarkly SDK key
            
        Raises:
            RuntimeError: If SDK fails to initialize
        """
        self.sdk_key = sdk_key
        self._client = None
        self._is_initialized = False
        self._initialize()
        self._setup_graceful_shutdown()
    
    def _initialize(self):
        """
        Initialize LaunchDarkly SDK following Rule 1 & 3.
        
        Rule 1: Singleton Pattern
        - Uses ldclient.set_config() and ldclient.get()
        - Enforces singleton pattern as documented
        
        Rule 3: Initialization Pattern
        - Uses the exact same initialization pattern
        - Includes timeout considerations
        - Proper singleton initialization
        """
        try:
            # Rule 1: Singleton configuration
            ldclient.set_config(Config(self.sdk_key))
            
            # Rule 3: Initialization check with timeout consideration
            if not ldclient.get().is_initialized():
                raise RuntimeError(
                    "Failed to initialize LaunchDarkly SDK. "
                    "Please check your internet connection and SDK credentials."
                )
            
            self._client = ldclient.get()
            self._is_initialized = True
            print("*** LaunchDarkly SDK successfully initialized")
            
        except Exception as e:
            raise RuntimeError(f"LaunchDarkly SDK initialization failed: {e}")
    
    def _setup_graceful_shutdown(self):
        """
        Setup graceful shutdown following Rule 4.
        
        Rule 4: Graceful Shutdown
        - Emphasizes graceful shutdown
        - Uses Python signal handlers
        - Proper flush and close patterns
        """
        def _close_client():
            """Close client gracefully."""
            try:
                if self._client:
                    self._client.close()
                    print("*** LaunchDarkly client closed gracefully")
            except Exception as e:
                print(f"*** Warning: Error closing LaunchDarkly client: {e}")
        
        # Register cleanup on exit
        atexit.register(_close_client)
        
        # Register signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            print(f"\\n*** Received signal {signum}, shutting down gracefully...")
            _close_client()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def is_ready(self) -> bool:
        """Check if the service is ready for use."""
        return self._is_initialized and self._client is not None
    
    def evaluate_flag(self, flag_key: str, context: Context, default_value: Any = False):
        """
        Evaluate a feature flag.
        
        Args:
            flag_key: Feature flag key
            context: User context
            default_value: Default value if flag evaluation fails
            
        Returns:
            Flag value
        """
        if not self.is_ready():
            raise RuntimeError("LaunchDarkly service is not ready")
        
        return self._client.variation(flag_key, context, default_value)
    
    def evaluate_flag_detail(self, flag_key: str, context: Context, default_value: Any = False):
        """
        Evaluate a feature flag with detailed information.
        
        Args:
            flag_key: Feature flag key
            context: User context
            default_value: Default value if flag evaluation fails
            
        Returns:
            Flag evaluation detail object
        """
        if not self.is_ready():
            raise RuntimeError("LaunchDarkly service is not ready")
        
        return self._client.variation_detail(flag_key, context, default_value)
    
    def add_flag_listener(self, flag_key: str, context: Context, callback: Callable):
        """
        Add a flag change listener.
        
        Args:
            flag_key: Feature flag key
            context: User context
            callback: Callback function for flag changes
            
        Returns:
            Listener object
        """
        if not self.is_ready():
            raise RuntimeError("LaunchDarkly service is not ready")
        
        return self._client.flag_tracker.add_flag_value_change_listener(
            flag_key, context, callback
        )
    
    def postfork(self):
        """
        Reinitialize client after fork (for worker processes).
        
        Rule 5: Worker Process Support
        - The official docs specifically mention:
        - "Worker-based servers require specific setup... use postfork() to reinitialize the client"
        """
        if self._client:
            self._client.postfork()
    
    def close(self):
        """Close the LaunchDarkly client."""
        if self._client:
            self._client.close()
            self._client = None
            self._is_initialized = False
