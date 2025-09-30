# LaunchDarkly Python Demo - Multiple Implementations

This repository contains **three** different implementations of the same LaunchDarkly demo, each showcasing different architectural patterns:

## 🎯 Three Implementations

### 1. **Original Single-File Version** (`main.py`)
- **Architecture**: Single file, procedural
- **Best For**: Quick start, learning basics
- **Run**: `python main.py`
- **Pros**: Simple, easy to understand
- **Cons**: Not scalable, harder to maintain

### 2. **Class-Based Modular Version** (`main_refactored.py`)
- **Architecture**: Object-oriented with classes
- **Structure**: `src/` directory with separated concerns
  - `src/config/` - Settings class
  - `src/services/` - LaunchDarklyService class
  - `src/listeners/` - Listener classes
  - `src/utils/` - DisplayUtils class
- **Best For**: Enterprise applications, complex requirements
- **Run**: `python main_refactored.py`
- **Pros**: Full OOP, easy to extend, professional
- **Cons**: More complex, more boilerplate

### 3. **Function-Based Modular Version** (`main_functional.py`) ✨ NEW!
- **Architecture**: Functional programming with pure functions
- **Structure**: `src_functional/` directory with separated concerns
  - `src_functional/config.py` - Configuration functions
  - `src_functional/launchdarkly.py` - Client management functions
  - `src_functional/context.py` - Context building functions
  - `src_functional/evaluation.py` - Flag evaluation functions
  - `src_functional/display.py` - Display functions
  - `src_functional/listeners.py` - Callback functions
- **Best For**: Modern Python, demos, medium-sized apps
- **Run**: `python main_functional.py`
- **Pros**: Simple, testable, Pythonic, no classes
- **Cons**: Less "enterprise-y" feel

## ✅ All Implementations Follow LaunchDarkly Best Practices

All three versions implement the **5 LaunchDarkly rules**:
1. ✅ Singleton Pattern
2. ✅ Environment-Aware Configuration
3. ✅ Proper Initialization
4. ✅ Graceful Shutdown  
5. ✅ Lightweight Configuration

**Plus**: Function-based version adds **non-blocking initialization**!

## 🚀 Quick Comparison

| Feature | Single-File | Class-Based | Function-Based |
|---------|-------------|-------------|----------------|
| Lines of Code | ~97 | ~600+ | ~300 |
| Number of Files | 1 | 13 | 7 |
| Complexity | Low | High | Medium |
| Testability | Low | High | High |
| Maintainability | Low | High | High |
| Learning Curve | Easy | Steep | Medium |
| Non-Blocking Init | ❌ | ❌ | ✅ |
| Dynamic Context | ❌ | ❌ | ✅ |

## 📊 Which One Should You Use?

- **Learning LaunchDarkly?** → Start with `main.py`
- **Building an enterprise app?** → Use `main_refactored.py`
- **Building a modern Python app?** → Use `main_functional.py` ✨
- **Just need a quick demo?** → Use `main.py`

## 🧪 Testing All Versions

```bash
# Test original
python main.py

# Test class-based
python main_refactored.py

# Test function-based
python main_functional.py
```

All three should produce similar output and demonstrate the same LaunchDarkly features!

## 📁 Repository Structure

```
hello-python/
├── main.py                    # Original single-file
├── main_refactored.py        # Class-based entry point
├── main_functional.py        # Function-based entry point
├── src/                      # Class-based modules
│   ├── config/
│   ├── services/
│   ├── listeners/
│   └── utils/
└── src_functional/           # Function-based modules
    ├── config.py
    ├── launchdarkly.py
    ├── context.py
    ├── evaluation.py
    ├── display.py
    └── listeners.py
```

## 🎯 Recommendation

For most users, we recommend the **Function-Based version** (`main_functional.py`) because it:
- Shows modern Python patterns
- Is easier to understand than classes
- Includes non-blocking initialization
- Supports dynamic context building
- Is production-ready but not over-engineered

---

Choose the implementation that best fits your needs and learning style! 🚀
