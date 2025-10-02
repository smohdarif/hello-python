# LaunchDarkly Python SDK - Best Practices

This document outlines the LaunchDarkly best practices implemented in this project.

---

## SDK is initialized once as a singleton early in the application's lifecycle

**Applies to:** All SDKs

Prevent duplicate connections, conserve resources, and ensure consistent caching/telemetry.

### Implementation

- **MUST** Expose exactly one `ldclient` per process/tab via a shared module/DI container (root provider in React).
- **SHOULD** Make init idempotent: reuse the existing client if already created.
- **SHOULD** Close the client cleanly on shutdown; in serverless, create the client **outside** the handler for container reuse.
- **NICE-TO-HAVE** Emit a single startup log summarizing effective LD config (redacted).

### Validation

- **Pass** if metrics/inspector show **one** stream connection per process/tab.
- **Pass** if event volume and resource usage do not scale with repeated imports/renders.

### Our Implementation

✅ Uses `ldclient.set_config()` and `ldclient.get()` singleton pattern  
✅ Graceful shutdown with `atexit` and signal handlers  
✅ Startup logging with redacted SDK key  
✅ One stream connection per process

**Location:** `src_functional/launchdarkly.py`

---

## Application does not block on initialization

**Applies to:** All SDKs

A LaunchDarkly SDK is *initialized* when it connects to the service and is ready to evaluate flags. If `variation` is called before initialization, the SDK returns the **fallback** value you provide. **Do not block** the app while waiting for initialization. The SDK will continue connecting in the background. Calls to `variation` will always return most recent flag value.

### Implementation

- **MUST** Set an initialization timeout
  - Client-side: **100–500 ms**
  - Server-side: **1–5 s**
- **SHOULD** Implement a custom timeout when the SDK lacks a native parameter by racing init against a timer.
- **MAY** Subscribe to change events to proactively **respond** to flag updates.

### Validation

- **Pass** if with endpoints blocked the app renders using fallbacks (or bootstrapped values) within the configured timeout.

### Our Implementation

✅ Server-side timeout: 5 seconds (configurable via `LD_INIT_TIMEOUT`)  
✅ Non-blocking initialization - app continues if LD unavailable  
✅ Real-time flag change listeners implemented  
✅ Tested with invalid SDK key - app still works with defaults

**Location:** `src_functional/launchdarkly.py`, `src_functional/listeners.py`

---

## Environment-Aware Configuration

**Applies to:** All SDKs

Configuration should adapt to the environment (dev, staging, prod).

### Implementation

- **MUST** Use environment variables for SDK key and sensitive configuration
- **SHOULD** Support `HTTPS_PROXY` environment variable for proxy configuration
- **SHOULD** Use different SDK keys for different environments
- **NICE-TO-HAVE** Configuration validation on startup

### Validation

- **Pass** if configuration correctly adapts to different environments
- **Pass** if proxy settings are respected when configured

### Our Implementation

✅ All configuration from environment variables  
✅ `HTTPS_PROXY` support implemented  
✅ Configuration validation with helpful error messages  
✅ `.env` file support for local development

**Location:** `src_functional/config.py`

---

## Safe Flag Evaluation (variation)

**Applies to:** All SDKs

Managing types coming back from LaunchDarkly. Mocking or local overrides in development/testing.

### Implementation

- **MUST** Always provide a default/fallback value
- **MUST** Handle cases where LD client is not initialized
- **SHOULD** Handle type mismatches gracefully
- **SHOULD** Log evaluation failures without crashing
- **MAY** Use `variation_detail()` for debugging and understanding evaluation reasons

### Validation

- **Pass** if evaluation always returns a value (never undefined/null)
- **Pass** if app works correctly when LD is unavailable
- **Pass** if type mismatches are handled gracefully

### Our Implementation

✅ `safe_variation()` always returns a value  
✅ Never blocks or crashes on evaluation  
✅ Returns default when LD not ready  
✅ Comprehensive error handling and logging  
✅ `safe_variation_detail()` for detailed evaluation information

**Location:** `src_functional/evaluation.py`

---

## Dynamic Context Building (getContext)

**Applies to:** Server-Side Implementations

Extending functionality such as additional logging or metrics. Manage and create contexts dynamically as the server is referenced.

### Implementation

- **MUST** Build contexts from actual user/request data, not static configuration
- **SHOULD** Support building contexts from various data sources (DB, API, JWT, session)
- **SHOULD** Include relevant user attributes for targeting
- **MAY** Support multi-kind contexts (user + organization)

### Validation

- **Pass** if contexts are created dynamically per request/user
- **Pass** if context attributes match actual user data
- **Pass** if contexts support custom attributes

### Our Implementation

✅ `build_user_context()` creates contexts dynamically  
✅ Supports arbitrary custom attributes  
✅ `build_context_from_dict()` for flexible data sources  
✅ Designed for database, API, JWT, or session data  
✅ Demo context provided for testing only

**Location:** `src_functional/context.py`

---

## Graceful Shutdown

**Applies to:** All SDKs

Proper cleanup when application terminates.

### Implementation

- **MUST** Close LD client before application exit
- **SHOULD** Register cleanup handlers for SIGINT/SIGTERM
- **SHOULD** Flush pending events before closing
- **NICE-TO-HAVE** Log shutdown status

### Validation

- **Pass** if client closes cleanly on shutdown
- **Pass** if pending events are flushed

### Our Implementation

✅ `close_ld_client()` for clean shutdown  
✅ Signal handlers for SIGINT/SIGTERM  
✅ `atexit` registration for automatic cleanup  
✅ Shutdown logging

**Location:** `src_functional/launchdarkly.py`

---

## Comprehensive Logging & Flow Tracking

**NICE-TO-HAVE** Emit logs showing execution flow for debugging and learning.

### Implementation

- **SHOULD** Log initialization status
- **SHOULD** Log evaluation details for debugging
- **MAY** Use structured logging with log levels
- **MAY** Include flow markers for tracing execution

### Our Implementation

✅ Flow markers: `📍 FLOW [1/6]`, `📍 FLOW [2/6]`, etc.  
✅ Step-by-step execution logging  
✅ Structured logs with INFO, WARNING, ERROR levels  
✅ Redacted sensitive information in logs

**Location:** All modules in `src_functional/`

---

## Summary: Best Practices Coverage

| Best Practice | Status | Location |
|--------------|--------|----------|
| Singleton Pattern | ✅ IMPLEMENTED | `launchdarkly.py` |
| Non-Blocking Initialization | ✅ IMPLEMENTED | `launchdarkly.py` |
| Environment Configuration | ✅ IMPLEMENTED | `config.py` |
| Safe Evaluation | ✅ IMPLEMENTED | `evaluation.py` |
| Dynamic Context Building | ✅ IMPLEMENTED | `context.py` |
| Graceful Shutdown | ✅ IMPLEMENTED | `launchdarkly.py` |
| Proxy Support | ✅ IMPLEMENTED | `config.py` |
| Real-Time Updates | ✅ IMPLEMENTED | `listeners.py` |
| Comprehensive Logging | ✅ IMPLEMENTED | All modules |

---

## Testing Best Practices

### Test Non-Blocking Initialization
Set an invalid SDK key - application should still start and work with default values.

### Test Singleton Pattern
Check logs to verify only ONE stream connection is established per process.

### Test Environment Configuration
Verify application uses environment-specific configuration correctly.

### Test Graceful Shutdown
Test signal handling (Ctrl+C) to ensure clean shutdown.

---

## Quick Reference

**CICE Flow:** Config → Init → Context → Evaluate

1. **Config** - Get SDK key and settings
2. **Init** - Connect to LaunchDarkly (non-blocking)
3. **Context** - Build user information
4. **Evaluate** - Get flag value (always safe)
5. **Display** - Show result
6. **Listen** - Monitor changes (optional)

**See:** `FLOW_GUIDE.md` for detailed flow diagrams

---

**Run the demo:** `python main_functional.py` 