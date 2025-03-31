import asyncio
import pathlib

from pydantic_ai import Agent
from openai import AsyncOpenAI, OpenAI 
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

import mcp_client

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()

CONFIG_FILE = SCRIPT_DIR / "mcp_config.json"

fetch_server = MCPServerStdio('python', ["-m", "mcp_server_fetch"])

def get_model():
    return OpenAIModel(
        model_name="gpt-4o-mini",
    )

async def get_pydantic_ai_agent():
    client = mcp_client.MCPClient()
    client.load_servers(str(CONFIG_FILE))
    tools = await client.start()
    return client, Agent(model=get_model(), tools=tools)

async def main():
    client, agent = await get_pydantic_ai_agent()
    while True:
        user_input=input("\n[You]: ")

        if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
            print('Goodbye!')
            break
            
        result = await agent.run(user_input)
        print('[Assistent]: ', result.data)

if __name__ == "__main__":
    asyncio.run(main())
