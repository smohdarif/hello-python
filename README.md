# LaunchDarkly Python Demo Application

A comprehensive Python application demonstrating LaunchDarkly's SDK with both single-file and modular architectures. This project showcases feature flag evaluation, real-time monitoring, and follows all LaunchDarkly best practices.

## 🏗️ Project Structure

This project provides **two implementations** of the same LaunchDarkly demo:

### 📁 **Single-File Version** (Original)
```
hello-python/
├── main.py                    # Single-file implementation
├── .env                       # Environment variables
└── requirements.txt           # Dependencies
```

### 📁 **Modular Version** (Refactored)
```
hello-python/
├── main_refactored.py         # Entry point for modular version
├── src/                       # Source package
│   ├── config/               # Configuration management
│   │   └── settings.py       # Environment & settings
│   ├── services/             # LaunchDarkly service
│   │   └── launchdarkly_service.py  # SDK wrapper
│   ├── listeners/            # Event handling
│   │   └── flag_listeners.py # Flag change listeners
│   ├── utils/                # Utilities
│   │   └── display.py        # Display & formatting
│   └── main.py               # Application logic
├── tests/                    # Unit tests
│   └── test_launchdarkly_service.py
├── .env                      # Environment variables
└── requirements.txt          # Dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- LaunchDarkly account and SDK key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/smohdarif/hello-python.git
   cd hello-python
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   # Copy and edit the .env file
   cp .env.example .env  # If available, or create .env manually
   ```

5. **Set up your .env file:**
   ```env
   # LaunchDarkly Configuration
   LAUNCHDARKLY_SDK_KEY=your-sdk-key-here
   LAUNCHDARKLY_FLAG_KEY=sample-feature
   
   # User Context Configuration (Optional)
   LAUNCHDARKLY_USER_KEY=example-user-key
   LAUNCHDARKLY_USER_NAME=Sandy
   LAUNCHDARKLY_USER_KIND=user
   
   # Optional: Set to 'true' to run in CI mode
   # CI=false
   ```

## 🎯 Running the Application

### Option 1: Single-File Version (Original)
```bash
python main.py
```

### Option 2: Modular Version (Refactored)
```bash
python main_refactored.py
```

Both versions provide the same functionality but with different architectures.

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_launchdarkly_service.py
```

## 🏛️ Architecture Comparison

### Single-File Version
- ✅ **Simple**: All code in one file
- ✅ **Easy to understand**: Linear flow
- ✅ **Quick setup**: Minimal structure
- ❌ **Hard to maintain**: Everything mixed together
- ❌ **Not scalable**: Difficult to extend

### Modular Version
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Testable**: Individual components can be tested
- ✅ **Scalable**: Easy to add new features
- ✅ **Professional**: Production-ready structure
- ✅ **Follows best practices**: All 5 LaunchDarkly rules implemented

## 📋 LaunchDarkly Flag Configuration

Before running the application, you need to set up a feature flag in your LaunchDarkly dashboard.

### 1. Flag Type and Key
- **Flag Type**: Boolean flag
- **Flag Key**: `sample-feature` (default) or any custom key you set in `LAUNCHDARKLY_FLAG_KEY`
- **Flag Name**: You can name it anything descriptive like "Sample Feature" or "Demo Feature"

### 2. Flag Variations
Since this is a **boolean flag**, you need two variations:
- **Variation 1**: `true` (Boolean)
- **Variation 2**: `false` (Boolean)

### 3. User Context
The program creates a specific user context that will appear in your LaunchDarkly dashboard:
- **User Key**: `example-user-key`
- **User Kind**: `user`
- **User Name**: `Sandy`

### 4. Step-by-Step Setup in LaunchDarkly

1. **Go to your LaunchDarkly dashboard** and navigate to your project

2. **Create a new flag**:
   - Click "Create Flag"
   - Choose "Boolean" as the flag type
   - Set the flag key to `sample-feature` (or your custom key)
   - Set the flag name to something like "Sample Feature"

3. **Configure the flag variations**:
   - **Variation 1**: `true` (Boolean)
   - **Variation 2**: `false` (Boolean)
   - Set the default variation to `false`

4. **Set up targeting rules**:
   - **For the user "Sandy" (key: example-user-key)**:
     - Add a targeting rule that serves `true` to this specific user
   - **For all other users**:
     - Serve `false` (or whatever you want as the default)

5. **Save and turn on the flag**

### 5. Testing the Setup

Once you've created the flag, you can test it by running either version of the application.

### 6. Expected Behavior

- **If the flag evaluates to `true`**: You'll see the LaunchDarkly banner displayed
- **If the flag evaluates to `false`**: You'll see the evaluation result but no banner
- **The program will wait for real-time changes**: You can toggle the flag in LaunchDarkly and see the changes immediately

### 7. Real-time Testing

While the program is running:
1. Go to your LaunchDarkly dashboard
2. Find the flag you created
3. Toggle it between `true` and `false`
4. Watch the program output change in real-time

## 🏆 LaunchDarkly Best Practices

The modular version implements all 5 official LaunchDarkly Python SDK best practices:

### ✅ Rule 1: Singleton Pattern
- Uses `ldclient.set_config()` and `ldclient.get()`
- Enforces singleton pattern as documented
- No custom singleton implementation needed

### ✅ Rule 2: Environment-Aware Configuration
- Uses `os.environ` for environment variables
- Supports `HTTPS_PROXY` environment variable
- Python idiomatic configuration methods

### ✅ Rule 3: Initialization Pattern
- Uses the exact same initialization pattern
- Includes timeout considerations
- Proper singleton initialization

### ✅ Rule 4: Graceful Shutdown
- Emphasizes graceful shutdown
- Uses Python signal handlers
- Proper flush and close patterns

### ✅ Rule 5: Lightweight Configuration
- Environment variable configuration
- Relay proxy support
- Logging configuration via environment variables

## 🔧 Development

### Adding New Features

The modular structure makes it easy to add new features:

1. **Add new services** in `src/services/`
2. **Add new utilities** in `src/utils/`
3. **Add new listeners** in `src/listeners/`
4. **Update configuration** in `src/config/`

### Code Organization

- **Configuration**: `src/config/settings.py`
- **LaunchDarkly Logic**: `src/services/launchdarkly_service.py`
- **Display Logic**: `src/utils/display.py`
- **Event Handling**: `src/listeners/flag_listeners.py`
- **Main Application**: `src/main.py`

## 📊 Features

### Single-File Version
- ✅ Basic flag evaluation
- ✅ Real-time flag monitoring
- ✅ Simple banner display
- ✅ Environment variable support

### Modular Version
- ✅ All single-file features
- ✅ Detailed flag evaluation with variation details
- ✅ Enhanced error handling
- ✅ Graceful shutdown with signal handling
- ✅ Comprehensive logging
- ✅ Unit tests
- ✅ Professional architecture
- ✅ Easy to extend and maintain

## 🛠️ Troubleshooting

### Common Issues

1. **SDK Key Error**: Make sure `LAUNCHDARKLY_SDK_KEY` is set in your `.env` file
2. **Flag Not Found**: Ensure the flag key matches what you created in LaunchDarkly
3. **Connection Issues**: Check your internet connection and proxy settings
4. **Import Errors**: Make sure you're in the correct directory and virtual environment is activated

### Debug Mode

Set `CI=true` in your `.env` file to run in CI mode (single evaluation without real-time monitoring).

## 📝 License

This project is licensed under the Apache-2.0 License - see the [LICENSE.txt](LICENSE.txt) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Additional Resources

- [LaunchDarkly Quickstart](https://app.launchdarkly.com/quickstart#/)
- [Python SDK Reference](https://docs.launchdarkly.com/sdk/server-side/python)
- [Feature Flag Best Practices](https://docs.launchdarkly.com/guides/flags/testing-flags)
