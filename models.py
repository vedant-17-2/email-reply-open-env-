
from pydantic import BaseModel
from typing import Optional, List


class EmailAction(BaseModel):
    reply: str


class ConversationTurn(BaseModel):
    role: str          # "customer" or "agent"
    message: str
    score: Optional[float] = None


class EmailObservation(BaseModel):
    email_subject: str
    email_body: str
    task_id: str
    instruction: str
    conversation_history: List[ConversationTurn] = []
    current_customer_message: Optional[str] = None
    turn_number: int = 0
    last_reply: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    done: bool = False


class EpisodeState(BaseModel):
    step: int
    episode_id: str
    task_id: str
    done: bool
    turn_number: int = 0
    cumulative_score: float = 0.0
