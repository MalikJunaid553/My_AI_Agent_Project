import os
from dotenv import load_dotenv
from fastmcp import Client
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"))

mcp_url = os.getenv("MCP_URL", "http://127.0.0.1:8000/sse")

async def search_internet(query: str) -> str:
    """Searches the live internet using SerpApi on Google."""
    async with Client(mcp_url) as client:
        result = await client.call_tool("search_internet", {"query": query})
        if hasattr(result, 'content') and len(result.content) > 0:
            text_data = getattr(result.content[0], 'text', '')
            if text_data.strip():
                return str(text_data)
        return str(result)

async def send_email(to_email: str, subject: str, body: str) -> str:
    """Sends an email to a recipient using yagmail."""
    async with Client(mcp_url) as client:
        result = await client.call_tool("send_email", {"to_email": to_email, "subject": subject, "body": body})
        return "SUCCESS: Email has been completely sent. Stop and inform the user."

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

memory = InMemorySaver()

system_prompt = (
    "You are a precise and reliable AI assistant that can search the live internet "
    "and send information by email.\n"
    "Follow these rules:\n"
    "1. Carefully understand what information the user is requesting.\n"
    "2. When the user asks for current, live, recent, or online information, use the "
    "'search_internet' tool to find the requested information.\n"
    "3. Search for the user's exact request and do not assume or invent information.\n"
    "4. Read and use the actual information returned by the 'search_internet' tool. "
    "Do not use placeholders or make up search results.\n"
    "5. If the user asks you to send the information by email, create a clear and "
    "accurate email containing the relevant information found from the search.\n"
    "6. Pass the actual information from the search results directly into "
    "'send_email'.\n"
    "7. Only send an email when the user explicitly asks you to send one.\n"
    "8. If the user provides an email address, use that address as the recipient. "
    "If no recipient email address is provided and one is required, ask the user "
    "for the email address before sending.\n"
    "9. Never invent facts, search results, prices, dates, names, or other information.\n"
    "10. After 'send_email' successfully runs, completely stop execution and tell "
    "the user that the email has been sent.\n"
    "11. If the user only asks for information and does not request an email, "
    "return the information directly to the user."
)

assistant_agent = create_react_agent(
    model=llm,
    tools=[search_internet, send_email],
    prompt=system_prompt,
    checkpointer=memory
)