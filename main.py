import os
import logging
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServerSse
from typing import AsyncGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8008/sse")


class ChatRequest(BaseModel):
    user_input: str


class ChatResponse(BaseModel):
    response: str


async def get_mcp_server() -> AsyncGenerator[MCPServerSse, None]:
    logger.info("Creating new MCP server instance...")
    server = MCPServerSse(
        name="MongoDB Demo MCP Server",
        params={"url": MCP_SERVER_URL},
        cache_tools_list=True,
    )
    await server.__aenter__()
    logger.info("MCP server instance created successfully")
    try:
        yield server
    finally:
        logger.info("Cleaning up MCP server instance...")
        await server.__aexit__(None, None, None)


app = FastAPI()


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat: ChatRequest, mcp_server: MCPServerSse = Depends(get_mcp_server)
):
    logger.info(f"Received chat request: {chat.user_input}")

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant and you can use some tools provided via model context protocol",
        model=MODEL,
        mcp_servers=[mcp_server],
    )

    try:
        trace_id = gen_trace_id()
        logger.info(f"Starting chat processing with trace_id: {trace_id}")
        with trace(workflow_name="Chat API Request", trace_id=trace_id):
            result = await Runner.run(starting_agent=agent, input=chat.user_input)
            logger.info("Chat processing completed successfully")
            return {"response": result.final_output}
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return {"response": f"Error: {str(e)}"}
