from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents import handoff
from agents.mcp import MCPServerStdio, MCPServer
from agents import Agent, Runner, gen_trace_id, trace
from contextlib import AsyncExitStack
from dotenv import load_dotenv
from typing import List

import os
import asyncio

model = OpenAIChatCompletionsModel(
    model="openchat",
    openai_client=AsyncOpenAI(
        base_url="http://10.255.78.58:9001/v1", 
        api_key="ollama"
    )
)

load_dotenv()
brave_api_key = os.getenv("BRAVE_API_KEY")

current_dir = os.path.dirname(os.path.abspath(__file__))
samples_dir = os.path.join(current_dir, "mcp_sample_files")

async def run(filesystem_server: MCPServer, websearch_server: MCPServer):
    filesystem_agent = Agent(
        name="Filesystem Assistant",
        instructions="Use the tools to read the filesystem and answer questions based on those files.",
        mcp_servers=[filesystem_server],
        # model="gpt-4o",
        model=model,
    )
    web_search_agent=Agent(
        name="Web Search Assistant",
        instructions="Use the tools search the browser and answer questions.",
        # model="gpt-4o",
        model=model,
        mcp_servers=[websearch_server],
    )

    triage_agent = Agent(name="Triage agent", 
                         instructions="Route to FileAgent or SearchAgent based on the task.",
                        #  model="gpt-4o",
                        model=model,
                         handoffs=[filesystem_agent, web_search_agent])
    
    message = input("[User]: ")
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=triage_agent, input=message)
    print(result.final_output)

async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "mcp_sample_files")

    async with AsyncExitStack() as stack:
        # Start filesystem MCP server
        fs_server = await stack.enter_async_context(
            MCPServerStdio(
                name="Filesystem Server",
                params={
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
                },
            )
        )

        # Start web search MCP server
        search_server = await stack.enter_async_context(
            MCPServerStdio(
                name="Search Server",
                params={
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                    "env":{"BRAVE_API_KEY": brave_api_key}
                },
            )
        )

        # Show available tools
        fs_tools = await fs_server.list_tools()
        search_tools = await search_server.list_tools()
        print("🗂 Filesystem tools:", [t.name for t in fs_tools])
        print("🔍 Search tools:", [t.name for t in search_tools])

        await run(fs_server, search_server)

if __name__=="__main__":
    asyncio.run(main())