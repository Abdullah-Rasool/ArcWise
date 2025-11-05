
"""
Agent: Validator 
Team Finstream | ArcWise Project
---------------------------------
Role:
Performs compliance and safety validation for flagged or uncertain transactions.
Runs deeper checks before final decision (approve/reject).
"""
from agents import Agent,Runner,handoff,RunContextWrapper,ModelSettings # type: ignore
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
class ValidationResult(BaseModel):
    amount:float
    recipient:str
    review_data : str
    compliance_status:str
    confidence : float = Field(..., ge=0.0 , le=1.0)
    risk_score: float = Field(..., ge=0.0 , le=1.0)
    recommendation:str
    decision: str = Field(..., description="success|failed")
    transaction_id : str = Field(..., description="Mock or real transaction hash")
    optional_msg:Optional[str] = None
#  --- System Instructions ---
Validator_INSTRUCTIONS = """

You are the Validator Agent, acting as a highly focused Compliance and Risk Officer.

Your single task is to review transactions flagged by the Decision Agent and provide an audited final status.

1.  **Review Input**: Analyze the data provided in the 'review_data' context. Pay special attention to the amount, recipient, and the 'safety_flag' status.

2.  **Risk Assessment:** Based on the transaction details (e.g., large amount, suspicious recipient), assign a high-fidelity **risk_score** between 0.0 (No Risk) and 1.0 (Highest Risk).

3.  **Policy Enforcement (The Threshold):**
    * If the calculated **risk_score is less than 0.4**, the transaction is low-risk.
    * If the calculated **risk_score is 0.4 or higher**, the transaction is high-risk.

4.  **Determine Final Status:**
    * Set `compliance_status` to **'approved'** for low-risk transactions (< 0.4).
    * Set `compliance_status` to **'rejected'** for high-risk transactions (>= 0.4).

5.  **Recommendation:** Based on the final status, set the `recommendation` field:
    * If approved: set to `execute_transaction`.Use the **decision_to_executor_handoff** tool. Pass ALL required data to the tool.
    * If rejected: set to `notify_admin` (to alert them of the block)and ignore transaction _id and do not return in the output.

6.  **Final Output:** You **MUST** return your complete analysis only as a JSON object strictly adhering to the **ValidationResult** schema. DO NOT add any extra text, explanations, or dialogue.
"""

# --- Agent Setup ---
validator_agent = Agent(
    name= "Validator Agent",
    output_type=ValidationResult,
    instructions=Validator_INSTRUCTIONS,
    model_settings=ModelSettings(temperature=0.0),
)

# --- handoff callback ---
async def handle_decision_to_validator(ctx:RunContextWrapper[None],input_data:DecisionHandoffPayload):
    logger.info(f"handoff received from:{input_data.source_agent}. safety status:{input_data.safety_flag}")

    if ctx.context is None:
        ctx.context = {} # type: ignore
        ctx.context["handoff_data"] = input_data.model_dump()   # type: ignore # store as dict, not JSON string
        return
        
   
decision_to_validator_handoff = handoff(
    agent=validator_agent,
    on_handoff=handle_decision_to_validator,
    input_type=DecisionHandoffPayload,
)