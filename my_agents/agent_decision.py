"""
Agent: Decision 
Team Finstream | ArcWise Project
---------------------------------
Role: The Decision Agent takes the handoff payload from the Analyzer Agent 
and decides what action to perform based on the intent and context.
"""

#   --- imports ---
from agents import Agent,Runner,ModelSettings,RunContextWrapper,handoff
from pydantic import BaseModel,Field,field_validator
from typing import Optional
import os
from dotenv import load_dotenv
from my_agents.handoff_shared_schema import DecisionHandoffPayload, HandoffPayload
from my_agents.agent_executor import decision_to_executor_handoff
from utils.logger import logger


#  --- Environment setup ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME","gpt-4o-mini")

if not openai_api_key:
    raise EnvironmentError("❌ OPENAI_API_KEY not found in .env file!")

os.environ["OPENAI_API_KEY"] = openai_api_key

#  --- Pydantic Schemas ---
class DecisionResult(BaseModel):
    """ Structured output from Descision Agent """
    decision : str = Field(..., description="review|approve|reject")
    confidence : float = Field(..., ge=0.0 , le=1.0)
    reason:str
    next_action: Optional[str] = Field(None, description="follow_up|notify_admin|execute_transaction")
    
    @field_validator("decision")
    def decision_must_be_valid(cls,v):
     allowed = {"approve","review","reject"}
     if v not in allowed:
        raise ValueError(f"Decision must be one of {allowed}")
     return v
    
    

#  --- LLM System Instructions ---
DECISION_INSTRUCTIONS = """
You are the Decision Agent in a financial workflow.
Your job:
1. Review Analyzer Agent’s structured 'handoff_data' provided in your context. 
2. Make a decision for each transaction: approve, review, or reject.
   - approve: safe, normal transaction
   - review: uncertain, large, or flagged by safety_flag
   - reject: confirmed suspicious, fraudulent, or invalid
3. **If the decision is 'approve'**: 
   Use the **decision_to_executor_handoff** tool. Pass ALL required data to the tool.

4. **If the decision is 'review'**: 
   Use the **decision_to_validator_handoff** tool. Pass ALL required data to the tool. 
   **CRITICAL:** DO NOT return a JSON object (DecisionResult) in this case.

5. **If the decision is 'reject'**:
   Return a JSON object that strictly adheres to the DecisionResult schema.
6. Always explain reasoning clearly in the "reason" field.
7. Set confidence between 0.0 and 1.0.
8. Suggest next_action, e.g., 'execute_transaction', 'notify_admin', 'follow_up'.
"""

# --- Agent Setup ---
decision_agent = Agent(
    name= "Decision Agent",
    instructions=DECISION_INSTRUCTIONS,
    output_type=DecisionResult,
    handoffs=[
        decision_to_executor_handoff,
    ],
    model_settings= ModelSettings(
        temperature = 0.0,
    ),
    
)

#   --- Handoff Callback Function ---
async def handle_handoff_payload(ctx:RunContextWrapper[None],input_data : HandoffPayload):
    logger.info(f"handoff received from:{input_data.source_agent}. safety status:{input_data.safety_flag}")
    if ctx.context is None:
        ctx.context = {}
        ctx.context["handoff_data"] = input_data.model_dump()   # store as dict, not JSON string
    
   
#  --- handoff config object ---
analyzer_to_decision_handoff = handoff(
    agent=decision_agent,
    on_handoff=handle_handoff_payload,
    input_type=HandoffPayload
)






