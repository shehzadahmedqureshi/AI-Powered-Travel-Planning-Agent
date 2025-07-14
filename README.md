# AI-Powered Travel Planning Agent

## 🚀 Overview

This project is an **AI Travel Planner** that uses advanced language models and modular tools to help users plan personalized trips. The agent can:

- Search for the flights based on user preferences
- Find hotels based on user preferences
- Generate daily itineraries with real activities

Users can request any combination: flights only, hotels only, itinerary only, or all together. The workflow is robust, stateful, and supports branching, retries, and future expansion.

---

## 🧩 Key Components

### 1. Large Language Model (LLM)

- **Provider:** Groq
- **Model:** `deepseek-r1-distill-llama-70b`
- **Purpose:** Reason about user input, decide which tools to use, and combine results into final responses.

### 2. Tools

Each functionality is a self-contained tool:

| Tool             | Description                                 |
| ---------------- | ------------------------------------------- |
| FlightSearchTool | Finds flights.                              |
| HotelSearchTool  | Finds hotels.                               |
| ItineraryTool    | Suggests a day-by-day plan with activities. |

- Each tool handles input, makes external API calls, and provides a clear description for the LLM.

### 3. Agent Executor

- Uses LangChain's `AgentExecutor` to wrap the LLM and tools.
- Parses user queries and decides tool usage dynamically (ReAct style).
- Logs intermediate steps for debugging and transparency.

### 4. Workflow Orchestration (LangGraph)

- Nodes for each tool (flight, hotel, itinerary)
- Conditional branching to skip irrelevant steps
- Retry logic for robustness (max 2 attempts per node)
- Simple state class to track intermediate and final results

---

## 🗂️ High-Level Flow

1. **Input:** User query (e.g., “I need hotels and an itinerary for Rome.”)
2. **State:** Stores input and outputs (`flight_result`, `hotel_result`, `itinerary_result`).
3. **Nodes:**
   - `CheckFlight` → `FlightNode`
   - `CheckHotel` → `HotelNode`
   - `CheckItinerary` → `ItineraryNode`
4. **Branching:**
   - Each check decides whether to run the corresponding node.
   - Skips irrelevant steps.
5. **Retries:**
   - If a node fails, retry that node only (max 2 attempts).
6. **Final Output:**
   - Aggregated results are returned to the user.

---

## 🏗️ Architecture

```
User Input → [LangChain AgentExecutor + Groq LLM]
           → [LangGraph Workflow]
               ├─ FlightNode (if needed)
               ├─ HotelNode (if needed)
               └─ ItineraryNode (if needed)
           → Aggregated Results
```

---

## 🛠️ Setup Instructions

### 1. Prerequisites

- Python 3.11+
- [Groq API Key](https://console.groq.com/)

### 2. Clone the Repository

```bash
git clone <your-repo-url>
cd Travel Agent/backend
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `backend/` directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

Or export it in your shell:

```bash
export GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Agent

```bash
python main.py
```

---

## 💡 Example Use Cases

| User Input                                 | Expected Path                          |
| ------------------------------------------ | -------------------------------------- |
| “Find me the cheapest flights to Tokyo”    | FlightNode only                        |
| “I need hotels in Paris and an itinerary”  | HotelNode + ItineraryNode              |
| “Plan a full trip to Rome with everything” | FlightNode → HotelNode → ItineraryNode |

---

## 🧩 Extending the Project

- Add new tools by creating a new file in `tools/` and registering it in `graph.py`.
- Update branching logic in the workflow to include new tools.
- The modular design makes it easy to add features or swap out APIs.

---

## ✅ Success Criteria

- User can run the agent with natural language input.
- Agent only runs relevant tools.
- Each node can retry if it fails.
- Results are stored in state and shown at the end.
- Easy to extend with new tools or flows.

---

## 📄 Folder Structure

```
backend/
├── main.py              # Entry point
├── graph.py             # Workflow and agent logic
├── tools/
│   ├── flight_tool.py
│   ├── hotel_tool.py
│   └── itinerary_tool.py
├── requirements.txt     # Dependencies
├── .env                 # For GROQ_API_KEY
└── README.md            # This file
```

---

## ⚡️ End Result

A robust, modular travel-planning AI agent that:

- Uses LLM reasoning + tools
- Supports flexible workflows
- Handles real-world errors gracefully
- Can grow as you add features!
