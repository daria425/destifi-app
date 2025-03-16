from app.core.assistants.travel_image_assistant import TravelImageAnalyzer
from app.core.agents.travel_agent import generate_itenerary_with_tool
def create_itinerary_from_image(travel_image_analyzer:TravelImageAnalyzer, image_data_url:str):
    """Creates an itinerary based on the image."""
    image_analysis=travel_image_analyzer.respond_to_upload(image_data_url)
    itinerary=generate_itenerary_with_tool(image_analysis)
    return itinerary

    