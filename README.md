# LaunchDarkly sample Python application

We've built a simple console application that demonstrates how LaunchDarkly's SDK works.

Below, you'll find the build procedure. For more comprehensive instructions, you can visit your [Quickstart page](https://app.launchdarkly.com/quickstart#/) or the [Python reference guide](https://docs.launchdarkly.com/sdk/server-side/python).

This demo requires Python 3.9 or higher.

## Setup Instructions

### Option 1: Using Environment File (Recommended)

1. **Create a `.env` file** in the project root with your LaunchDarkly credentials:
   ```bash
   # Create .env file
   touch .env
   ```

2. **Add your environment variables** to the `.env` file:
   ```env
   # LaunchDarkly Configuration
   LAUNCHDARKLY_SDK_KEY=your-sdk-key-here
   LAUNCHDARKLY_FLAG_KEY=sample-feature
   
   # Optional: Set to 'true' to run in CI mode (single evaluation)
   # CI=false
   ```

3. **Install dependencies**:
   ```bash
   # Using pip (recommended)
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Or using Poetry
   poetry install
   ```

4. **Run the application**:
   ```bash
   # Using pip
   source venv/bin/activate
   python main.py
   
   # Or using Poetry
   poetry run python main.py
   ```

### Option 2: Using Environment Variables

1. Set the environment variable `LAUNCHDARKLY_SDK_KEY` to your LaunchDarkly SDK key. If there is an existing boolean feature flag in your LaunchDarkly project that you want to evaluate, set `LAUNCHDARKLY_FLAG_KEY` to the flag key; otherwise, a boolean flag of `sample-feature` will be assumed.

    ```bash
    export LAUNCHDARKLY_SDK_KEY="1234567890abcdef"
    export LAUNCHDARKLY_FLAG_KEY="my-boolean-flag"
    ```

2. Ensure you have [Poetry](https://python-poetry.org/) installed.
3. Install the required dependencies with `poetry install`.
4. On the command line, run `poetry run python main.py`

## Expected Output

You should receive the message "The <flagKey> feature flag evaluates to <flagValue>.". The application will run continuously and react to the flag changes in LaunchDarkly.

## Security Note

The `.env` file is included in `.gitignore` to prevent accidentally committing sensitive credentials to version control. Always keep your LaunchDarkly SDK keys secure and never commit them to public repositories.
