import os, time, json
from azure.ai.projects.models import FunctionTool, RequiredFunctionToolCall, SubmitToolOutputsAction, ToolOutput, BingGroundingTool, ToolSet
from dotenv import load_dotenv
from app.core.agents.agent_functions import extract_travel_details
from app.config.ai_project_client import project_client
load_dotenv()
websearch_agent_id=os.getenv("WEBSEARCH_AGENT_ID")