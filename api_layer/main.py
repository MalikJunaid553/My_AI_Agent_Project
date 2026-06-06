import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, ".env"))

from api_layer.assistant import assistant_agent

app = FastAPI()

class UserRequest(BaseModel):
    prompt: str

@app.post("/api/v1/chat")
async def chat_with_agent(data: UserRequest):
    agent_response = await assistant_agent.ainvoke(
        {"messages": [("user", data.prompt)]},
        config={"configurable": {"thread_id": "postman_user"}}
    )
    
    final_answer = agent_response["messages"][-1].content
    
    return {
        "status": "success",
        "output": final_answer
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
#uvicorn api_layer.main:app --reload --port 8080