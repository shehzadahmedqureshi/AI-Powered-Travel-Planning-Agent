import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from graph import compiled_graph

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your Vercel frontend URL only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

app = FastAPI()

class PlanTripRequest(BaseModel):
    query: str

@app.post("/plan_trip")
async def plan_trip(request: PlanTripRequest):
    input_state = {"input_text": request.query}
    result = compiled_graph.invoke(input_state)
    return {"result": result["agent_response"]}