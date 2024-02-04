# GPTs-EasyConfig
![Static Badge](https://img.shields.io/badge/license-MIT-blue)

`GPTs-EasyConfig` is a streamlined open-source tool designed to simplify and automate the setup and configuration of databases for GPT-based applications. Leveraging the user-friendly Streamlit interface, it provides a seamless experience for both beginners and experienced developers to manage and interact with their GPT instances effectively.

Currently, `GPTs-EasyConfig` supports web search, web parsing, and web navigation. Other functions are still under development.

## Prerequisites

Before you begin, ensure you have the following installed:
- `Conda`
- `Google Chrome`
- `ChromeDriver` compatible with your Chrome version

## Environment Setup

1. **Create a Conda Environment:**
   Open your terminal and create a new Conda environment named `gpts-easyconfig` with Python 3.10 by running:

   ```bash
   conda create -n gpts-easyconfig python=3.10
   ```

2. **Activate the Environment:**
   Activate the newly created environment using:

   ```bash
   conda activate gpts-easyconfig
   ```

3. **Install Dependencies:**
   Navigate to the project directory and install the required packages from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables:**
   Copy the `.env_template` file to a new file named `.env` in the same directory.

   ```bash
   cp backend_assistent/.env_template backend_assistent/.env
   ```

   Fill in the `.env` file with your details:
   - `CHROME_DRIVER_PATH`: The file path to your ChromeDriver executable.
   - `CHROME_BINARY_PATH`: The file path to your Google Chrome executable.
   - `SCREENSHOT_PATH`: The directory where screenshots will be saved.
   - `USERNAME`: Your GitHub username.
   - `REPO`: The name of the GitHub repository you're working with.
   - `TOKEN`: Your GitHub personal access token.
   - `CHROME_USER_DATA_DIR`: The path to Chrome's user data directory.
   - `CHROME_PROFILE_DIRECTORY`: The name of the Chrome profile directory.
   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `GOOGLE_API_KEY`: Your Google API key.
   - `GOOGLE_CSE_ID`: Your Google Custom Search Engine ID.

   Ensure the Chrome binary and ChromeDriver are compatible with each other.

## Running the Application

With the environment set up and configured, you can run the application with the following command:

```bash
python -m backend_assistent.main
```

