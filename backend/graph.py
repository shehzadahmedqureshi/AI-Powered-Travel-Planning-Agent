import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, Tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import RunnableRetry

from tools.flight_tool import FlightSearchTool
from tools.hotel_tool import HotelSearchTool
from tools.itinerary_tool import ItineraryTool


# ✅ Setup Groq LLM
llm = ChatGroq(
    model_name="deepseek-r1-distill-llama-70b",
    api_key=os.getenv("GROQ_API_KEY"),
)

# ✅ Wrap your tools
tools = [
    Tool.from_function(
        func=FlightSearchTool()._run,
        name="FlightSearch",
        description="Finds cheapest return flights"
    ),
    Tool.from_function(
        func=HotelSearchTool()._run,
        name="HotelSearch",
        description="Finds good hotels with good location"
    ),
    Tool.from_function(
        func=ItineraryTool()._run,
        name="Itinerary",
        description="Suggests day-by-day plan with real activities"
    ),
]

# ✅ Shared agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=llm,
    tools=tools,
    verbose=True,
)

# ✅ State
class TravelPlannerState:
    def __init__(self, input_text):
        self.input_text = input_text
        self.flight_result = None
        self.hotel_result = None
        self.itinerary_result = None


# ✅ Nodes — each with retry wrapper

@RunnableRetry(max_attempts=2)  # retry this node if it fails
def flight_node(state: TravelPlannerState):
    output = agent_executor.run(f"Only find flights: {state.input_text}")
    state.flight_result = output
    return state

@RunnableRetry(max_attempts=2)
def hotel_node(state: TravelPlannerState):
    output = agent_executor.run(f"Only find hotels: {state.input_text}")
    state.hotel_result = output
    return state

@RunnableRetry(max_attempts=2)
def itinerary_node(state: TravelPlannerState):
    output = agent_executor.run(f"Only build itinerary: {state.input_text}")
    state.itinerary_result = output
    return state


# ✅ Branch logic: decide which nodes to run

def decide_flight(state: TravelPlannerState):
    if "flight" in state.input_text.lower():
        return "FlightNode"
    return "CheckHotel"

def decide_hotel(state: TravelPlannerState):
    if "hotel" in state.input_text.lower():
        return "HotelNode"
    return "CheckItinerary"

def decide_itinerary(state: TravelPlannerState):
    if "itinerary" in state.input_text.lower():
        return "ItineraryNode"
    return END


# ✅ Build graph

graph = StateGraph(TravelPlannerState)

graph.add_node("FlightNode", flight_node)
graph.add_node("HotelNode", hotel_node)
graph.add_node("ItineraryNode", itinerary_node)

# Conditional branches
graph.add_conditional_edges("CheckFlight", decide_flight)
graph.add_conditional_edges("CheckHotel", decide_hotel)
graph.add_conditional_edges("CheckItinerary", decide_itinerary)

# After each node, go to next check
graph.add_edge("FlightNode", "CheckHotel")
graph.add_edge("HotelNode", "CheckItinerary")
graph.add_edge("ItineraryNode", END)

graph.set_entry_point("CheckFlight")

compiled_graph = graph.compile()