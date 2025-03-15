import os, time, json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, RequiredFunctionToolCall, SubmitToolOutputsAction, ToolOutput, BingGroundingTool, ToolSet
from dotenv import load_dotenv
from typing import List
load_dotenv()
ai_foundry_project_key=os.getenv("AZURE_AI_FOUNDRY_PROJECT_KEY")
ai_foundry_connection_string=os.getenv("AZURE_AI_FOUNDRY_PROJECT_CONNECTION_STRING")
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=ai_foundry_connection_string
)

sample_description="""
    **Travel Destination Insights:**

    Analyzing the collage, the terminal theme suggests a journey and exploration, ideal for travel enthusiasts looking for a unique combination of tropical nature and cultural experience. The imagery suggests a tropical destination, likely a rainforest region known for its rich biodiversity and breathtaking landscapes, possibly like the Amazon Rainforest or the Galapagos Islands.

    **Suggested Travel Destinations:**

    1. **Tayuca, Mexico**: Noted for its vibrant tropical flowers and lush greenery, Tayuca offers a picturesque backdrop akin to the orchid and lotus paintings in your image.
    2. **Yunnan, China**: The earthy tones and images of natural and ancient structures suggest Yunnan, a province known for its biodiverse rainforest, ethnic cultures, and historical sites.
    3. **Okinawa, Japan**: The diverse natural elements and serene landscapes presented in the collage align with the region's rich cultural heritage and unique flora, tropical islands, and traditional Ryukyu Islands culture.
    4. **Borneo, Indonesia**: The image's rural charm and natural resources point to Borneo, known for its peatland rice fields, Meheram cowries, and a bamboo forest.

    **Activities and Vibe:**

    The tropical and serene vibe of the collage suggests a travel experience filled with outdoor adventures such as hiking, bird-watching, and nature photography. Activities like visiting local markets, attending cultural festivals, and participating in traditional crafts would reveal the rich local culture, mirroring the door-to-yid and delivery box scenes that imply exploration and discovery.

    **Weather and Season:**

    Given the lush tropical imagery, the travel experience would likely be in the rainy season, offering vibrant colors and lush landscapes. Expect humidity, occasional rain showers, and warm weather during this period, suitable for a rich, immersive experience in nature and local communities.

    **Keywords for Trip Recommendations:**

    - Tropical rainforest
    - Biodiversity
    - Cultural heritage
    - Outdoor adventures
    - Nature photography
    - Traditional crafts
    - Floral landscapes
    - Authentic markets

    This collage-inspired travel plan promises an immersive journey through some of the world's most enchanting tropical destinations, blending cultural richness with natural splendor."""

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

functions = FunctionTool(functions=[extract_travel_details])


def get_structured_travel_details(description: str):
    """
    Get structured travel details from a description using an Azure AI agent.
    
    Args:
        description: A travel destination description
        
    Returns:
        dict: Structured travel data extracted by the agent
    """
    with project_client:
        # Create an agent with appropriate tools
        agent = project_client.agents.create_agent(
            model="gpt-4o",
            name="travel-detail-assistant",
            instructions="You are a helpful travel assistant. Your task is to analyze the provided travel destination description and extract key details for personalized trip planning. Provide insights on the destination, trip vibe, recommended activities, seasonal considerations, ideal trip length, budget category, and user preferences. Use the provided description to generate a structured summary for trip recommendations. Use your knowledge and best recommendations if specific details are not provided within the text",
            tools=functions.definitions,
        )

        thread = project_client.agents.create_thread()
        
        # Add the user message with the description
        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=f"""Help me plan a vacation based on this description:{description}""",
        )
        
        # Start the agent run
        run = project_client.agents.create_run(thread_id=thread.id, assistant_id=agent.id)
        
        # Track the extracted data
        extracted_data = None
        
        # Process the run until completion
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

            if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    project_client.agents.cancel_run(thread_id=thread.id, run_id=run.id)
                    break

                tool_outputs = []
                for tool_call in tool_calls:
                    if isinstance(tool_call, RequiredFunctionToolCall):
                        try:
                            output = functions.execute(tool_call)
                            # Save the extracted data
                            extracted_data = json.loads(output)
                            tool_outputs.append(
                                ToolOutput(
                                    tool_call_id=tool_call.id,
                                    output=output,
                                )
                            )
                        except Exception as e:
                            print(f"Error executing tool_call: {e}")

                # Submit the outputs to continue the run
                project_client.agents.submit_tool_outputs_to_run(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs,
                )

        # Clean up
        project_client.agents.delete_agent(agent.id)
        
        # Return just the extracted data
        return extracted_data

def generate_itenerary_with_tool(description:str):
    with project_client:
        # Create an agent and run user's request with function calls
        agent = project_client.agents.create_agent(
            model="gpt-4o",
            name="my-assistant",
            instructions="You are a helpful travel assistant. Your task is to generate a detailed and personalized itinerary based on the provided text. Make sure that the created itenerary is detailed and breaks down activities day by day. If the text contains multiple destinations only provide an itenerary for one. If any details are missing, infer the most suitable options using your knowledge of travel trends, geographic conditions, and seasonal insights. Ensure recommendations are practical, well-structured, and aligned with the user’s preferences.",
            tools=functions.definitions,
        )
        print(f"Created agent, ID: {agent.id}")

        thread = project_client.agents.create_thread()
        print(f"Created thread, ID: {thread.id}")

        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=f"""Help me plan a vacation based on this description:{description}""",
        )
        print(f"Created message, ID: {message.id}")

        run = project_client.agents.create_run(thread_id=thread.id, assistant_id=agent.id)
        print(f"Created run, ID: {run.id}")

        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

            if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    print("No tool calls provided - cancelling run")
                    project_client.agents.cancel_run(thread_id=thread.id, run_id=run.id)
                    break

                tool_outputs = []
                for tool_call in tool_calls:
                    if isinstance(tool_call, RequiredFunctionToolCall):
                        try:
                            print(f"Executing tool call: {tool_call}")
                            output = functions.execute(tool_call)
                            tool_outputs.append(
                                ToolOutput(
                                    tool_call_id=tool_call.id,
                                    output=output,
                                )
                            )
                        except Exception as e:
                            print(f"Error executing tool_call {tool_call.id}: {e}")

                print(f"Tool outputs: {tool_outputs}")
                if tool_outputs:
                    project_client.agents.submit_tool_outputs_to_run(
                        thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                    )

            print(f"Current run status: {run.status}")

        print(f"Run completed with status: {run.status}")
        messages = project_client.agents.list_messages(thread_id=thread.id)
        last_message = messages.data[0]['content'][0]['text']['value']
        return last_message

# ai_message=generate_itenerary_with_tool(sample_description)
# print(ai_message)