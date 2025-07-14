from langchain.tools import BaseTool

class FlightSearchTool(BaseTool):
    name = "FlightSearchTool"
    description = "Finds cheapest return flights using Tequila API"

    def _run(self, origin, destination, month):
        # Your Tequila API call here!
        return f"Dummy flight: {origin} to {destination} in {month}"