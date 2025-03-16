import os, time, json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, RequiredFunctionToolCall, SubmitToolOutputsAction, ToolOutput, BingGroundingTool, ToolSet
from dotenv import load_dotenv
from app.core.agents.agent_functions import extract_travel_details
load_dotenv()
ai_foundry_project_key=os.getenv("AZURE_AI_FOUNDRY_PROJECT_KEY")
ai_foundry_connection_string=os.getenv("AZURE_AI_FOUNDRY_PROJECT_CONNECTION_STRING")
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=ai_foundry_connection_string
)


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