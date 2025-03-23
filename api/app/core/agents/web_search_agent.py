import os, time, json
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))

api_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

sys.path.insert(0, api_dir)
from azure.ai.projects.models import FunctionTool, RequiredFunctionToolCall, SubmitToolOutputsAction, ToolOutput, BingGroundingTool
from dotenv import load_dotenv
from app.config.ai_project_config import project_client, bing_connection
from app.core.agents.agent_functions import extract_stock_sentiment
load_dotenv()
web_search_agent_id=os.getenv("WEB_SEARCH_AGENT_ID")

class WebSearchAgent:
    def __init__(self):
        self.functions = FunctionTool(functions=[extract_stock_sentiment])
        self.bing_tool=BingGroundingTool(connection_id=bing_connection.id)
        self.project_client = project_client
        self.thread_id=None
        self.agent_id=web_search_agent_id

    def see_tools(self):
        agent=self.project_client.agents.get_agent(assistant_id=self.agent_id)
        print(agent.tools)
    def update_agent_config(self, agent_updates):
            self.project_client.agents.update_agent(
                assistant_id=self.agent_id,
                **agent_updates
            )
         
    def get_stock_sentiment(self, stock: str):
        generation_instructions="""Given the following stock, use the bing tool to provide a summary of the latest sentiment analysis, key financial news, and potential market-moving events. 
- Ensure insights are clear, concise, and useful for investors. 
- Use the bing tool to ensure information is up to date.
- Provide as much detail as possible on sentiment and reasons for the sentiment,
- include a sentiment score of -1 to 1 and sentiment category (Bullish, Neutral, Bearish), 
 -include key financial news topics, and news volume (specific number of mentions in articles or social media)."""
        agent=self.project_client.agents.get_agent(assistant_id=self.agent_id)
        if self.bing_tool.definitions[0] not in agent.tools:
            print("Adding Bing tool")
            self.update_agent_config(agent_updates={"tools":[self.bing_tool.definitions[0]]})
        if agent.instructions!=generation_instructions:
                print("Updating instructions")
                self.update_agent_config(agent_updates={"instructions":generation_instructions})
        thread = self.project_client.agents.create_thread()
        print(f"Created thread, ID: {thread.id}")
        self.thread_id = thread.id

        message = self.project_client.agents.create_message(
            thread_id=self.thread_id,
            role="user",
            content=f"""Stock Data:{stock}""",
        )
        print(f"Created message, ID: {message.id}")

        run = self.project_client.agents.create_run(thread_id=self.thread_id, assistant_id=self.agent_id)
        print(f"Created run, ID: {run.id}")

        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = self.project_client.agents.get_run(thread_id=self.thread_id, run_id=run.id)

            if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    print("No tool calls provided - cancelling run")
                    self.project_client.agents.cancel_run(thread_id=self.thread_id, run_id=run.id)
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
                        thread_id=self.thread_id, run_id=run.id, tool_outputs=tool_outputs
                    )
            print(f"Current run status: {run.status}")
        print(f"Run completed with status: {run.status}")
        messages = self.project_client.agents.list_messages(thread_id=self.thread_id)
        last_message = messages.data[0]['content'][0]['text']['value']
        return {
            "message": last_message, 
            "thread_id": self.thread_id,
            "timestamp":run.created_at
        }
    
    def extract_structured_data(self, sentiment_analysis:str):
        agent = self.project_client.agents.get_agent(assistant_id=self.agent_id)
        generation_instructions = """Analyze the following stock sentiment paragraph and extract structured information, 
        including the stock symbol, overall sentiment score (-1 to 1), sentiment category (Bullish, Neutral, Bearish), key financial news topics, news volume (number of mentions in articles or social media). 
        Ensure the extracted data is well-structured and suitable for quantitative analysis."""
        if self.functions.definitions[0] not in agent.tools:
            print("Replacing Bing tool with function tool")
            self.update_agent_config(agent_updates={"tools":[self.functions.definitions[0]]})   
        if agent.instructions != generation_instructions:
            print("Updating instructions")
            self.update_agent_config(agent_updates={"instructions":generation_instructions})
        message = self.project_client.agents.create_message(
            thread_id=self.thread_id,
            role="user",
            content=f"""Stock Sentiment:{sentiment_analysis}""",
        )
        print(f"Created message, ID: {message.id}")

        run = self.project_client.agents.create_run(thread_id=self.thread_id, assistant_id=self.agent_id)
        print(f"Created run, ID: {run.id}")

        tool_outputs_results = []  # Store all tool outputs

        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = self.project_client.agents.get_run(thread_id=self.thread_id, run_id=run.id)

            if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    print("No tool calls provided - cancelling run")
                    self.project_client.agents.cancel_run(thread_id=self.thread_id, run_id=run.id)
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
                    self.project_client.agents.cancel_run(thread_id=self.thread_id, run_id=run.id)
                    break
            
            print(f"Current run status: {run.status}")
        print(run)
        print(f"Run completed with status: {run.status}")
        
        # If we collected tool outputs, return them directly
        if tool_outputs_results:
            return tool_outputs_results[0]["output"]  # Return just the first tool output content
        
        # Otherwise, fall back to the message response
        messages = self.project_client.agents.list_messages(thread_id=self.thread_id)
        last_message = messages.data[0]['content'][0]['text']['value']
        return {
            "message": last_message, 
            "thread_id": self.thread_id,
            "timestamp": run.created_at
        }
        

    
agent=WebSearchAgent()
stock_data={
    "symbol": "TSLA",
    "name": "Tesla, Inc.",
    "summary": "Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems in the United States, China, and internationally. The company operates in two segments, Automotive, and Energy Generation and Storage. The Automotive segment offers electric vehicles, as well as sells automotive regulatory credits. It provides sedans and sport utility vehicles through direct and used vehicle sales, a network of Tesla Superchargers, and in-app upgrades; and purchase financing and leasing services. This segment is also involved in the provision of non-warranty after-sales vehicle services, sale of used vehicles, retail merchandise, and vehicle insurance, as well as sale of products through its subsidiaries to third party customers; services for electric vehicles through its company-owned service locations, and Tesla mobile service technicians; and vehicle limited warranties and extended service plans. The Energy Generation and Storage segment engages in the design, manufacture, installation, sale, and leasing of solar energy generation and energy storage products, and related services to residential, commercial, and industrial customers and utilities through its website, stores, and galleries, as well as through a network of channel partners. This segment also offers service and repairs to its energy product customers, including under warranty; and various financing options to its solar customers. The company was formerly known as Tesla Motors, Inc. and changed its name to Tesla, Inc. in February 2017. Tesla, Inc. was founded in 2003 and is headquartered in Palo Alto, California.",
    "currency": "USD",
    "sector": "Consumer Discretionary",
    "industry_group": "Automobiles & Components",
    "industry": "Automobiles",
    "exchange": "NMS",
    "market": "NASDAQ Global Select",
    "country": "United States",
    "state": "CA",
    "city": "Palo Alto",
    "zipcode": "94304",
    "website": "http://www.tesla.com",
    "market_cap": "Mega Cap",
    "isin": "US88160R1014",
    "cusip": "88160R101",
    "figi": 0,
    "composite_figi": 0,
    "shareclass_figi": 0,
    "label": "TSLA",
    "description": "Tesla, Inc.",
    "additionalInfo": "Consumer Discretionary"
}

stock_data=json.dumps(stock_data)
analysis=agent.get_stock_sentiment(stock_data)
print(analysis)
time.sleep(5)  # Pause execution for 5 seconds
structured_data=agent.extract_structured_data(analysis['message'])
print(structured_data)
