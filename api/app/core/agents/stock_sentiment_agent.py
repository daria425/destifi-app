import os, time, json, sys, re, random

current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, api_dir)
from azure.ai.projects.models import FunctionTool, RequiredFunctionToolCall, SubmitToolOutputsAction, ToolOutput, BingGroundingTool
from dotenv import load_dotenv
from app.config.ai_project_config import project_client, bing_connection
from app.core.agents.agent_functions import extract_stock_sentiment
from app.core.agents.agent_instructions import search_instructions, extract_instructions
load_dotenv()

class RateLimitException(Exception):
    """Custom exception for rate limit handling"""
    def __init__(self, message, wait_time=None):
        self.message = message
        self.wait_time = wait_time
        super().__init__(self.message)

class StockSentimentAgent:
    def __init__(self):
        self.project_client = project_client
        self.search_agent_id = os.getenv("WEB_SEARCH_AGENT_ID")  # Dedicated for Bing searches
        self.extract_agent_id = os.getenv("EXTRACT_AGENT_ID")  # Dedicated for extractions
        self.bing_tool = BingGroundingTool(connection_id=bing_connection.id)
        self.functions = FunctionTool(functions=[extract_stock_sentiment])
        self.search_instructions = search_instructions
        self.extract_instructions = extract_instructions
        
    def setup_agents(self):
        """Initialize both agents with their respective configurations"""
        try:
            self.project_client.agents.update_agent(
                assistant_id=self.search_agent_id,
                tools=[self.bing_tool.definitions[0]],
                instructions=self.search_instructions
            )
        except Exception as e:
            print(f"Error setting up search agent: {e}")
        try:
            self.project_client.agents.update_agent(
                assistant_id=self.extract_agent_id,
                tools=[self.functions.definitions[0]],
                instructions=self.extract_instructions
            )
        except Exception as e:
            print(f"Error setting up extraction agent: {e}")
    
    def _extract_wait_time(self, error_msg):
        """Extract wait time from error message"""
        wait_time_match = re.search(r'Try again in (\d+) seconds', str(error_msg))
        if wait_time_match:
            return int(wait_time_match.group(1)) + random.randint(5, 15)  # Add jitter
        return 60  # Default wait time
        
    def _handle_run_with_rate_limit(self, create_run_func, get_run_func, max_retries=3):
        """Generic method to handle runs with rate limit retry logic"""
        run = None
        
        for attempt in range(max_retries):
            try:
                # If no run exists yet or we need to create a new one after rate limit
                if run is None:
                    run = create_run_func()
                    print(f"Created run, ID: {run.id}")
                
                # Monitor run progress with rate limit handling
                while run.status in ["queued", "in_progress", "requires_action"]:
                    time.sleep(1)
                    try:
                        run = get_run_func(run.id)
                    except Exception as e:
                        if "rate_limit" in str(e).lower():
                            wait_time = self._extract_wait_time(e)
                            print(f"Rate limit during monitoring. Waiting {wait_time}s...")
                            time.sleep(wait_time)
                            continue
                        raise 
                    yield run
                break
                
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    if attempt < max_retries - 1:
                        wait_time = self._extract_wait_time(e)
                        print(f"Rate limit hit, attempt {attempt+1}/{max_retries}. Waiting {wait_time}s...")
                        time.sleep(wait_time)
                        run = None  # Reset run so we create a new one
                    else:
                        raise Exception(f"Max retries exceeded due to rate limits")
                else:
                    print(f"Unexpected error: {e}")
                    raise
        
        return run
    
    def get_stock_sentiment(self, stock: str):
        """Use search agent with Bing tool to get sentiment analysis"""
        thread = self.project_client.agents.create_thread()
        thread_id = thread.id
        message = self.project_client.agents.create_message(
            thread_id=thread_id,
            role="user",
            content=f"""Stock Data:{stock}""",
        )
        print(f"Created message, ID: {message.id}")

        # Define create and get run functions for this context
        def create_run():
            try:
                return self.project_client.agents.create_run(thread_id=thread_id, assistant_id=self.search_agent_id)
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    wait_time = self._extract_wait_time(e)
                    print(f"Rate limit when creating run. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    raise  # Re-raise to trigger retry
                raise
                
        def get_run(run_id):
            return self.project_client.agents.get_run(thread_id=thread_id, run_id=run_id)

        # Use the generic handler
        run = None
        for current_run in self._handle_run_with_rate_limit(create_run, get_run):
            run = current_run
            # No special handling needed here, just let it run
            print(f"Current run status: {run.status}")
            
        if not run:
            raise Exception("Failed to create or complete the run")
            
        print(f"Run completed with status: {run.status}")
        
        # Get messages with rate limit handling
        try:
            messages = self.project_client.agents.list_messages(thread_id=thread_id)
        except Exception as e:
            if "rate_limit" in str(e).lower():
                wait_time = self._extract_wait_time(e)
                print(f"Rate limit when listing messages. Waiting {wait_time}s...")
                time.sleep(wait_time)
                messages = self.project_client.agents.list_messages(thread_id=thread_id)
            else:
                raise
                
        last_message = messages.data[0]['content'][0]['text']['value']
        return {
            "message": last_message, 
            "thread_id": thread_id,
            "timestamp": run.created_at
        }
        
    def extract_structured_data(self, sentiment_analysis: str):
        """Use extraction agent with function tool to extract structured data"""
        thread = self.project_client.agents.create_thread()
        thread_id = thread.id
        message = self.project_client.agents.create_message(
            thread_id=thread_id,
            role="user",
            content=f"""Sentiment Analysis:{sentiment_analysis}""",
        )
        print(f"Created message, ID: {message.id}")

        tool_outputs_results = []  # Store all tool outputs

        # Define create and get run functions for this context
        def create_run():
            try:
                return self.project_client.agents.create_run(thread_id=thread_id, assistant_id=self.extract_agent_id)
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    wait_time = self._extract_wait_time(e)
                    print(f"Rate limit when creating extraction run. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    raise  # Re-raise to trigger retry
                raise
                
        def get_run(run_id):
            return self.project_client.agents.get_run(thread_id=thread_id, run_id=run_id)

        # Use the generic handler with tool processing
        run = None
        for current_run in self._handle_run_with_rate_limit(create_run, get_run):
            run = current_run
            
            if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    print("No tool calls provided - cancelling run")
                    self.project_client.agents.cancel_run(thread_id=thread_id, run_id=run.id)
                    break

                for tool_call in tool_calls:
                    if isinstance(tool_call, RequiredFunctionToolCall):
                        try:
                            print(f"Executing tool call: {tool_call}")
                            output = self.functions.execute(tool_call)
                            
                            # Store the output directly
                            tool_outputs_results.append({
                                "tool_call_id": tool_call.id,
                                "function_name": tool_call.function.name,
                                "output": output
                            })
                        except Exception as e:
                            print(f"Error executing tool_call {tool_call.id}: {e}")
                
                # Once we've collected outputs, cancel the run instead of submitting them
                if tool_outputs_results:
                    print("Tool outputs collected, cancelling run")
                    try:
                        self.project_client.agents.cancel_run(thread_id=thread_id, run_id=run.id)
                        break
                    except Exception as e:
                        if "rate_limit" in str(e).lower():
                            wait_time = self._extract_wait_time(e)
                            print(f"Rate limit when cancelling run. Waiting {wait_time}s...")
                            time.sleep(wait_time)
                            # Still break as we have the tool outputs
                            break
                        raise
                        
            print(f"Current run status: {run.status}")

        print(f"Run completed with status: {run.status if run else 'Unknown'}")
        
        # Return tool outputs if available
        if tool_outputs_results:
            return tool_outputs_results[0]["output"]
        
        # Otherwise, get the message response
        try:
            messages = self.project_client.agents.list_messages(thread_id=thread_id)
        except Exception as e:
            if "rate_limit" in str(e).lower():
                wait_time = self._extract_wait_time(e)
                print(f"Rate limit when listing messages. Waiting {wait_time}s...")
                time.sleep(wait_time)
                messages = self.project_client.agents.list_messages(thread_id=thread_id)
            else:
                raise
                
        last_message = messages.data[0]['content'][0]['text']['value']
        return {
            "message": last_message, 
            "thread_id": thread_id,
            "timestamp": run.created_at if run else time.time()
        }

    def analyze_stock(self, stock_data):
        """Complete workflow with retry and error handling"""
        max_retries = 3
        retry_delay = 60  # seconds
        self.setup_agents()
        
        for attempt in range(max_retries):
            try:
                analysis = self.get_stock_sentiment(stock_data)
                # Wait between calls to avoid rate limits
                wait_time = random.randint(10, 20)  # Random wait time
                print(f"Analysis received. Waiting {wait_time}s before extraction...")
                time.sleep(wait_time)
                structured_data = self.extract_structured_data(analysis['message'])
                return structured_data
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    wait_time = self._extract_wait_time(e) + retry_delay * attempt
                    print(f"Rate limit in workflow. Waiting {wait_time}s before retry {attempt+1}/{max_retries}")
                    time.sleep(wait_time)
                else:
                    print(f"Unexpected error in workflow: {e}")
                    if attempt == max_retries - 1:
                        raise
        
        raise Exception("Max retries exceeded")
    

# agent=StockSentimentAgent()
# stock_data="TSLA"
# structured_data=agent.analyze_stock(stock_data)
# print(structured_data)