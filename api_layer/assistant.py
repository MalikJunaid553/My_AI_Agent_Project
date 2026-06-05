import os
from dotenv import load_dotenv
from fastmcp import Client
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"))

mcp_url = "http://127.0.0.1:8000/sse"

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
    model="llama-3.1-8b-instant",  
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

memory = InMemorySaver()

system_prompt = (
    "You are a precise AI assistant. Follow these steps exactly:\n"
    "1. Use 'search_internet' to find out the current live weather in the requested location.\n"
    "2. Read the results returned by the search tool. Do not use placeholders.\n"
    "3. Use the real temperatures and conditions found in the search results to build the email body.\n"
    "4. Pass that custom weather data directly into 'send_email'.\n"
    "5. Once 'send_email' runs, completely stop execution and tell the user it is done."
)

assistant_agent = create_react_agent(
    model=llm,
    tools=[search_internet, send_email],
    prompt=system_prompt,
    checkpointer=memory
)