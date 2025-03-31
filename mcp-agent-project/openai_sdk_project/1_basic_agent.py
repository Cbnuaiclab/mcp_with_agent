from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

model = OpenAIChatCompletionsModel(
    model="deepseek-r1:8b",
    openai_client=AsyncOpenAI(
        base_url="http://10.255.78.58:9001/v1", 
        api_key="ollama"
    )
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model
)

result = Runner.run_sync(agent, "Create a meal plan for a week.")
print(result.final_output)