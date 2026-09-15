import os
import yagmail
from fastmcp import FastMCP
from serpapi import GoogleSearch
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"))

mcp = FastMCP("My-Tools-Server")

@mcp.tool()
def search_internet(query: str) -> str:
    """Searches the live internet using SerpApi on Google."""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY is missing from the environment variables."
        
    params = {"q": query, "api_key": api_key}
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            return f"SerpApi Error Message: {results['error']}"
            
        if "organic_results" in results:
            snippets = [r.get("snippet", "") for r in results["organic_results"][:3]]
            return "\n---\n".join(snippets)
            
        return "Google search returned successfully, but no results found."
    except Exception as e:
        return f"Exception occurred during search execution: {str(e)}"

@mcp.tool()
def send_email(to_email: str, subject: str, body: str) -> str:
    """Sends an email to a recipient using yagmail."""
    try:
        yag = yagmail.SMTP(os.getenv("YAGMAIL_USER"), os.getenv("YAGMAIL_APP_PASSWORD"))
        yag.send(to=to_email, subject=subject, contents=body)
        return f"Successfully sent email to {to_email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    mcp.run(transport="sse", port=port)

    #python mcp_server.py