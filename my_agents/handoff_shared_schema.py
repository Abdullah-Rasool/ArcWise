
from typing import Optional
from pydantic import BaseModel,Field

class TransactionDetailsHandoff(BaseModel):
    """
    Holds structured Transaction details that handoff to Decision Agent
    """
    amount: Optional[float] = None
    asset: Optional[str] = None
    recipient: Optional[str] = None
    memo: Optional[str] = None
    
class HandoffPayload(BaseModel):
    """The structured data to be passed during the handoff."""
    source_agent: str = "Analyzer Agent"
    intent: str
    confidence: float
    reason: str
    transaction: Optional[TransactionDetailsHandoff] = None
    safety_flag: bool = Field(False)

class DecisionHandoffPayload(HandoffPayload):
     """Used for passing Decision Agent’s output to the Executor Agent."""
     source_agent: str = "Decision Agent"
     decision: str
     next_action: Optional[str]
    
