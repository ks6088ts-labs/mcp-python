import asyncio
import logging
from os import getenv

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

logging.basicConfig(level=logging.DEBUG)
load_dotenv(override=True)


async def run_agent(message: str):
    async with MultiServerMCPClient(
        {
            "math": {
                # Make sure to update to the full absolute path to your environment
                "command": "/Users/ks6088ts/.local/bin/uv",
                "args": [
                    "--directory",
                    "/Users/ks6088ts/src/github.com/ks6088ts-labs/mcp-python/scripts",
                    "run",
                    "math_server.py",
                ],
                "transport": "stdio",
            },
            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    ) as client:
        model = AzureChatOpenAI(
            api_key=getenv("AZURE_OPENAI_API_KEY"),
            api_version=getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
            model=getenv("AZURE_OPENAI_MODEL_GPT"),
        )

        agent = create_react_agent(model, client.get_tools())
        return await agent.ainvoke(
            {
                "messages": message,
            }
        )


if __name__ == "__main__":
    for message in [
        "what is 1 + 1?",
        "what is the weather in nyc?",
        "tell me a joke",
    ]:
        result = asyncio.run(run_agent(message=message))
        print(f"Result: {result}")

        last_message: BaseMessage = result["messages"][-1]
        print(f"Question: {message}")
        print(f"Answer: {last_message.content}")
        # print(f"Last message: {last_message.model_dump_json(indent=2)}")
