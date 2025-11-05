
"""
Agent: Executor 
Team Finstream | ArcWise Project
---------------------------------
Role:
Handles approved transactions and performs blockchain/USDC execution
on Arc network (mocked for now).
"""

# --- Imports ---
from agents import Agent,Runner,handoff,RunContextWrapper,ModelSettings
import json,os
from pydantic import BaseModel,Field,field_validator
from typing import Optional
import asyncio
from dotenv import load_dotenv
from my_agents.handoff_shared_schema import DecisionHandoffPayload
from utils.logger import logger


# --- Environment Setup ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME","gpt-4o-mini")

if not openai_api_key:
    raise EnvironmentError("❌ OPENAI_API_KEY not found!")

os.environ["OPENAI_API_KEY"] = openai_api_key

# --- Pydantic Output Schema ---
class ExecutionResult(BaseModel):
    transaction_id : str = Field(..., description="Mock or real transaction hash")
    decision: str = Field(..., description="success|failed")
    reason:str
    amount:float
    recipient:str
    optional_msg:Optional[str] = None
    
#  --- System Instructions ---
EXECUTOR_INSTRUCTIONS = """
You are the Executor Agent.
You receive a validated and approved transaction payload.
1. Simulate sending the transaction to Arc/USDC (mock API call for now).
2. Return structured ExecutionResult JSON.
3. Set status = 'success' unless simulated conditions fail.
4. Include confirmation_msg with human-readable summary.
"""

# --- Agent Setup ---
executor_agent = Agent(
    name= "Executor Agent",
    output_type=ExecutionResult,
    instructions=EXECUTOR_INSTRUCTIONS,
    model_settings=ModelSettings(temperature=0.0),
)

# --- handoff callback ---
async def handle_decision_to_executor(ctx:RunContextWrapper[None],input_data:DecisionHandoffPayload):
    logger.info(f"💼 Received approved handoff from {input_data.source_agent}")

    if ctx.context is None:
        ctx.context = {}
        ctx.context["handoff_data"] = input_data.model_dump()   # store as dict, not JSON string
        return
        
   
decision_to_executor_handoff = handoff(
    agent=executor_agent,
    on_handoff=handle_decision_to_executor,
    input_type=DecisionHandoffPayload,
)




