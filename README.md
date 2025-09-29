# LaunchDarkly sample Python application

We've built a simple console application that demonstrates how LaunchDarkly's SDK works.

Below, you'll find the build procedure. For more comprehensive instructions, you can visit your [Quickstart page](https://app.launchdarkly.com/quickstart#/) or the [Python reference guide](https://docs.launchdarkly.com/sdk/server-side/python).

This demo requires Python 3.9 or higher.

## LaunchDarkly Flag Configuration

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

Once you've created the flag, you can test it by running:

```bash
# Activate virtual environment
source venv/bin/activate

# Set your SDK key (replace with your actual key)
export LAUNCHDARKLY_SDK_KEY="your-actual-sdk-key-here"

# Optionally set a custom flag key (or leave it to use 'sample-feature')
export LAUNCHDARKLY_FLAG_KEY="sample-feature"

# Run the program
python main.py
```

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
