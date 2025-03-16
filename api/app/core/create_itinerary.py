from app.core.assistants.travel_image_assistant import TravelImageAnalyzer
from app.core.agents.travel_agent import Travel_Agent
def create_itinerary_from_image(travel_image_analyzer:TravelImageAnalyzer, travel_agent:Travel_Agent,image_data_url:str):
    """Creates an itinerary based on the image."""
    image_analysis=travel_image_analyzer.respond_to_upload(image_data_url)
    itinerary_data=travel_agent.generate_itenerary_with_tool(image_analysis)
    return itinerary_data

    