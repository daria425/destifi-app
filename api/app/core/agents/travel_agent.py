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
class Travel_Agent:
    def __init__(self):
        self.functions = FunctionTool(functions=[extract_travel_details])
        self.project_client = project_client
        self.thread_id=None
        self.agent_id=None
        self.started_chat=False
    
    def start_chat(self):
        update={
            "tools": None, 
            "instructions":"You are a travel AI assistant that helps users plan vacations. Your goal is to provide detailed and personalized itineraries based on user requests. You should use your knowledge of travel trends, geographic conditions, and seasonal insights to create practical and well-structured recommendations. Ensure that the itineraries are aligned with the user's preferences and break down activities day by day. Make sure to ask clarifying questions if any details are missing and ensure that activities are specific."
        }
        self.tools=None
        self.update_agent_config(self.agent_id, self.thread_id, update)
        self.started_chat=True


    def update_agent_config(self, agent_id:str, agent_updates: dict):
        with self.project_client:
            if self.agent_id:
                try:
                    self.project_client.agents.update_agent(assistant_id=agent_id, **agent_updates)
                except Exception as e:
                    print(f"Error updating agent: {e}")


    def generate_itenerary_with_tool(self, description: str):
        with self.project_client:
            # Create an agent and run user's request with function calls
            if not self.agent_id:
                agent = self.project_client.agents.create_agent(
                    model="gpt-4o",
                    name="my-assistant",
                    instructions="You are a helpful travel assistant. Your task is to generate a detailed and personalized itinerary based on the provided text. Make sure that the created itenerary is detailed and breaks down activities day by day. If the text contains multiple destinations only provide an itenerary for one. If any details are missing, infer the most suitable options using your knowledge of travel trends, geographic conditions, and seasonal insights. Ensure recommendations are practical, well-structured, and aligned with the user's preferences.",
                    tools=self.functions.definitions,
                )
                print(f"Created agent, ID: {agent.id}")
                self.agent_id = agent.id
            if not self.thread_id:
                thread = self.project_client.agents.create_thread()
                print(f"Created thread, ID: {thread.id}")
                self.thread_id = thread.id

            message = self.project_client.agents.create_message(
                thread_id=self.thread_id,
                role="user",
                content=f"""Help me plan a vacation based on this description:{description}""",
            )
            print(f"Created message, ID: {message.id}")

            run = self.project_client.agents.create_run(thread_id=self.thread_id, assistant_id=self.agent_id)
            print(f"Created run, ID: {run.id}")

            while run.status in ["queued", "in_progress", "requires_action"]:
                time.sleep(1)
                run = self.project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

                if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    if not tool_calls:
                        print("No tool calls provided - cancelling run")
                        self.project_client.agents.cancel_run(thread_id=thread.id, run_id=run.id)
                        break

                    tool_outputs = []
                    for tool_call in tool_calls:
                        if isinstance(tool_call, RequiredFunctionToolCall):
                            try:
                                print(f"Executing tool call: {tool_call}")
                                output = self.functions.execute(tool_call)
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
                        self.project_client.agents.submit_tool_outputs_to_run(
                            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                        )
                print(f"Current run status: {run.status}")
            print(f"Run completed with status: {run.status}")
            messages = self.project_client.agents.list_messages(thread_id=thread.id)
            last_message = messages.data[0]['content'][0]['text']['value']
            return {
                "message": last_message, 
                "thread_id": self.thread_id,
                "timestamp":run.created_at
            }
    def respond_to_user(self, user_message:str):
            if not self.thread_id or not self.agent_id: 
                raise ValueError("No active thread or agent found, please start a new conversation.")
            with self.project_client:
                message = self.project_client.agents.create_message(
                    thread_id=self.thread_id,
                    role="user",
                    content=user_message,
                )
                print(f"Created message, ID: {message.id}")
                if not self.started_chat:
                    self.start_chat()
                run = self.project_client.agents.create_run(thread_id=self.thread_id, assistant_id=self.agent_id)
                print(f"Created run, ID: {run.id}")
                
                while run.status in ["queued", "in_progress", "requires_action"]:
                    time.sleep(1)
                    run = self.project_client.agents.get_run(thread_id=self.thread_id, run_id=run.id)
                    print(f"Current run status: {run.status}")
                print(f"Run completed with status: {run.status}")
                messages = self.project_client.agents.list_messages(thread_id=self.thread_id)
                last_message = messages.data[0]['content'][0]['text']['value']
                return last_message
        
        
