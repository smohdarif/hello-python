# LaunchDarkly Flow - Easy to Remember Guide

## 🎯 The Golden Rule: "Config → Init → Context → Evaluate"

**Remember: CICE** (pronounced "Nice" with a C)
- **C**onfig - Get your keys
- **I**nit - Connect to LaunchDarkly  
- **C**ontext - Build user info
- **E**valuate - Get flag value

---

## 📊 Visual Flow

```
1. CONFIG      →  2. INIT       →  3. CONTEXT    →  4. EVALUATE
   🔑               🚀                👤               🎲
   
get_sdk_key()      init_ld_client    build_user_      safe_variation
                   (NON-BLOCKING!)    context()        (ALWAYS SAFE!)
```

---

## 🔄 Step-by-Step Sequence

### **1. CONFIG** 🔑 (config.py)
```python
sdk_key = get_sdk_key()        # "Where's my key?"
config = load_app_config()     # "What are my settings?"
validate_config(config)        # "Is everything OK?"
```
**Think**: Getting your ID card before entering a building

---

### **2. INIT** 🚀 (launchdarkly.py)
```python
init_ld_client(sdk_key)        # "Connect to LaunchDarkly"
setup_graceful_shutdown()      # "Prepare for exit"
is_ready = is_ld_ready()       # "Are we connected?"
```
**Think**: Starting your car (might take a second, but you can still go!)
**KEY**: Non-blocking! App works even if LD not ready

---

### **3. CONTEXT** 👤 (context.py)
```python
context = build_user_context(
    user_id='user-123',
    name='John',
    email='john@example.com'
)
```
**Think**: Showing your ticket at a movie theater (WHO are you?)

---

### **4. EVALUATE** 🎲 (evaluation.py)
```python
value = safe_variation(
    flag_key='my-feature',
    context=context,
    default_value=False
)
```
**Think**: Asking "Can I enter?" and getting Yes/No
**KEY**: ALWAYS returns a value (default if LD not ready)

---

### **5. DISPLAY** 📺 (display.py)
```python
show_basic_result(flag_key, value)
```
**Think**: Showing the result on screen

---

### **6. LISTEN** 👂 (Optional - listeners.py)
```python
add_flag_listener(flag_key, context, callback)
```
**Think**: Subscribing to notifications for changes

---

## 💡 Memory Trick: "The Restaurant Story"

1. **Config** = Check the menu (What's available?)
2. **Init** = Sit down (Get ready, might wait for table)
3. **Context** = Tell server your name (Who are you?)
4. **Evaluate** = Order food (What do you want?)
5. **Display** = See your plate (Here's your food!)
6. **Listen** = Wait for refills (Server brings updates)

---

## ⚡ Quick Cheat Sheet

| Step | Function | Remember |
|------|----------|----------|
| 1️⃣ | `get_sdk_key()` | 🔑 Get keys first! |
| 2️⃣ | `init_ld_client()` | 🚀 Connect (non-blocking!) |
| 3️⃣ | `build_user_context()` | 👤 WHO is asking? |
| 4️⃣ | `safe_variation()` | 🎲 Get value (always safe!) |
| 5️⃣ | `show_result()` | 📺 Display it |
| 6️⃣ | `add_listener()` | 👂 Watch for changes (optional) |

---

## ❌ DON'T Do This:
```python
# WRONG - No config!
init_ld_client("hardcoded-key")  

# WRONG - Init after evaluation!
value = safe_variation(...)
init_ld_client(sdk_key)

# WRONG - No context!
value = safe_variation(flag_key, None, False)
```

## ✅ DO This:
```python
# CORRECT sequence
sdk_key = get_sdk_key()              # 1. Config
init_ld_client(sdk_key)              # 2. Init
context = build_user_context(...)    # 3. Context  
value = safe_variation(...)          # 4. Evaluate
show_basic_result(...)               # 5. Display
```

---

## 🎯 One-Liner to Remember

**"Key → Init → Who → Value"**

That's the LaunchDarkly flow! 🚀 