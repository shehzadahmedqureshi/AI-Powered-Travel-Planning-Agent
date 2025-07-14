from langchain.tools import BaseTool

class HotelSearchTool(BaseTool):
    name = "HotelSearchTool"
    description = "Finds a hotel with good location and reviews."

    def _run(self, location, check_in, check_out):
        # Example stub — replace with real Google Places API or Booking.com API
        return (
            f"Found a nice hotel in {location} from {check_in} to {check_out}: "
            "The Cozy Central Hotel, 4.5 stars, great location near city center."
        )

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented yet.")