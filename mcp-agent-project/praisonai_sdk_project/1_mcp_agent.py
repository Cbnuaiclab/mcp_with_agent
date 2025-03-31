from praisonaiagents import Agent, MCP
from dotenv import load_dotenv

import os 

load_dotenv()

def search_airbnb(query):
    agent=Agent(
        instructions="You help book apartments on Airbnb.",
        llm="gpt-4o-mini", 
        tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
    )
    result = agent.start(query)
    return f"## Airbnb Search Results\n\n{result}"



def search_files(query):
    agent=Agent(
        instructions="Use the tools to read the filesystem and answer questions based on those files. Use those files to answer the user's questions.",
        llm="gpt-4o-mini", 
        tools=MCP("npx -y @modelcontextprotocol/server-filesystem ~/Research")
    )
    result = agent.start(query)
    return f"## File Search Results\n\n{result}"

brave_api_key = os.getenv("BRAVE_API_KEY")
def brave_search(query):
    search_agent = Agent(
        instructions="""You are a helpful assistant that can search the web for information.
        Use the available tools when relevant to answer user questions.""",
        llm="gpt-4o-mini",
        tools=MCP("npx -y @modelcontextprotocol/server-brave-search", env={"BRAVE_API_KEY": brave_api_key})
    )
    result=search_agent.start(query)
    return f"## File Search Results\n\n{result}"

brave_search("Search more information about AI News")
# search_airbnb("I want to book an apartment in Paris for 2 nights. 03/28 - 03/30 for 2 adults")
# search_files("What can you do?")