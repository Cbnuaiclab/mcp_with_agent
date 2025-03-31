import asyncio
import os
import shutil
from typing import List

from dotenv import load_dotenv
from agents import Agent, Runner, gen_trace_id, trace, set_default_openai_key, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.mcp import MCPServer, MCPServerStdio, MCPServerSse

model = OpenAIChatCompletionsModel(
    model="llama3.3:latest",
    openai_client=AsyncOpenAI(
        base_url="http://10.255.78.58:9001/v1", 
        api_key="ollama"
    )
)

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY",""))
github_token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")

async def run(mcp_server: MCPServer, message:str):
    agent = Agent(
        name="Assistant",
        instructions=f"Answer questions about the git repository.",
        mcp_servers=[mcp_server],
        # model="gpt-4o-mini"
        model=model
    )
    print("\n"+"-"*40)
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

async def main():
    async with MCPServerStdio(
        cache_tools_list=True,
        params={"command": "npx", "args":["@modelcontextprotocol/server-github"], "env":{"GITHUB_PERSONAL_ACCESS_TOKEN":github_token}},
    ) as server: 
        with trace(workflow_name="MCP Git Example"):
            await run(server,input("[User] "))

if __name__=="__main__":
    asyncio.run(main())