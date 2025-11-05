"""
Agent: Analyzer
Team Finstream | ArcWise Project
---------------------------------
Role:
Analyzes user transactions, detects anomalies,
classifies transaction intents, and outputs clean structured data
for the Decision Agent via handoff.
"""

#  --- Imports ---
import json
from agents import Agent, Runner, ModelSettings
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from dotenv import load_dotenv
import os
import asyncio
from my_agents.agent_decision import analyzer_to_decision_handoff
from utils.logger import logger


#  --- Environment setup ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

if not openai_api_key:
    raise EnvironmentError("❌ OPENAI_API_KEY not found in .env file!")

# Set it globally for downstream libraries
os.environ["OPENAI_API_KEY"] = openai_api_key


#  --- Pydantic Schemas ---
class TransactionDetails(BaseModel):
    """Holds structured transaction details."""
    amount: Optional[float] = None
    asset: Optional[str] = None
    recipient: Optional[str] = None
    memo: Optional[str] = None


class AnalysisResult(BaseModel):
    """Main structured output from the Analyzer Agent."""
    intent: str = Field(..., description="transaction|information|investment|general")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str
    transaction: Optional[TransactionDetails] = None
    safety_flag: bool = Field(False)

    @field_validator("intent")
    def intent_must_be_valid(cls, v):
        allowed = {"transaction", "information", "investment", "general"}
        if v not in allowed:
            raise ValueError(f"intent must be one of {allowed}")
        return v


#  --- LLM System Instructions ---
ANALYZER_INSTRUCTIONS = """
You are the Analyzer Agent.
Your role:
1. Classify the user’s input into one of: transaction, information, investment, or general.
2. If transaction, extract amount, asset (e.g., USDC), recipient (address/handle), and optional memo.
3. If the intent is 'transaction', use the provided handoff tool immediately 
to pass the data to the Decision Agent. Do NOT return JSON yourself.
4. set safety_flag amount > 10000 or recipient appears suspicious.
4. keep responses deterministic and concise.
"""


#  --- Agent Setup ---
analyzer_agent = Agent(
    name="Analyzer Agent",
    instructions=ANALYZER_INSTRUCTIONS,
    output_type=AnalysisResult,
    handoffs=[analyzer_to_decision_handoff],
    model_settings=ModelSettings(
        temperature=0.0,
    ),
)


#  --- Core Execution Function ---
async def analyze_and_run(text: str):
    """
    Run the full multi-agent workflow asynchronously
    """
    try:
        logger.info(f" Analyzing input: {text}")
        res = await Runner.run(analyzer_agent, input=text,)
        logger.info(" Analysis successful.")
        if res.final_output:
             print("\nFinal Agent Output:\n" + json.dumps(res.final_output.model_dump(), indent=2))
    except Exception as e:
        logger.error(f" Error during analysis: {e}")
        return None



#  --- Example Test Run ---
if __name__ == "__main__":
    examples = [
        "Transfer 10 USDC to 0xAbC1234ef5678 for invoice #223",
        "What's my USDC balance?",
        "Send 20000 USDC to suspicious_user",
        "Invest 5000 USDC in Bitcoin",
    ]

    for ex in examples:
        asyncio.run(analyze_and_run(ex))
      
        print("-" * 50)
