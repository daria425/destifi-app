from typing import List
import json
def extract_travel_details(
    destination: str,
    vibe: str,
    recommended_activities: List[str],
    seasonal_insights: str,
    trip_length: str,
    budget: str,
    preferred_activities: List[str]
) -> str:
    """
    Extracts structured travel details from the provided text.

    :param destination: The travel destination mentioned in the text, e.g., 'Santorini, Greece'.
    :param vibe: Overall theme or mood of the trip, e.g., 'Romantic, scenic, luxurious'.
    :param recommended_activities: List of suggested activities based on the destination.
    :param seasonal_insights: Best seasons to visit and any relevant seasonal considerations.
    :param trip_length: Ideal duration of the trip, e.g., '5 days'.
    :param budget: Estimated budget category for the trip, e.g., 'Mid-range'.
    :param preferred_activities: List of user-specified preferences for activities.
    
    :return: A JSON string containing structured travel details.
    """
    travel_data = {
        "destination": destination,
        "vibe": vibe,
        "recommended_activities": recommended_activities,
        "seasonal_insights": seasonal_insights,
        "trip_length": trip_length,
        "budget": budget,
        "preferred_activities": preferred_activities,
    }
    
    return json.dumps(travel_data, indent=4)


def extract_activity_details(
    itinerary_text: str
) -> str:
    """
    Extracts specific activities from the provided itinerary text.

    :param itinerary_text: Raw text containing the travel itinerary details.
    
    :return: A JSON string containing a list of structured activity details.
    """
    activities = []
    day_sections = itinerary_text.split("Day ")
    
    for section in day_sections[1:]:
        try:
            day_number = section.split(":")[0].strip()
            details = section.split("\n")[1:]  # Skip the day heading
            
            for detail in details:
                if ":" in detail:
                    time_of_day, activity = detail.split(":", 1)
                    activities.append({
                        "day": int(day_number),
                        "time_of_day": time_of_day.strip(),
                        "activity": activity.strip()
                    })
        except Exception as e:
            print(f"Error parsing section: {section} - {e}")

    return json.dumps(activities, indent=4)


