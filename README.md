# MCP Project

## Setup Instructions

Follow these steps to set up your development environment:

### 1. Clone the repository

```bash
git clone <repository-url>
cd mcp
```

### 2. Set up environment variables

Copy the example environment file and configure it with your API keys:

```bash
cp .env-example .env
```

Open the `.env` file and add your API keys:
- OPENAI_API_KEY: Your OpenAI API key
- GITHUB_PERSONAL_ACCESS_TOKEN: Your GitHub personal access token
- BRAVE_API_KEY: Your Brave Search API key

### 3. Create a Python virtual environment

```bash
python -m venv env
```

### 4. Activate the virtual environment

On Linux/Mac:
```bash
source env/bin/activate
```

On Windows:
```bash
env\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

The project contains several example agents in the following directories:
- `mcp-agent-project/openai_sdk_project/`: OpenAI SDK examples
- `mcp-agent-project/praisonai_sdk_project/`: PraisonAI SDK examples
- `mcp-agent-project/pydantic_ai_sdk_project/`: Pydantic AI SDK examples

## License

[Add license information here]