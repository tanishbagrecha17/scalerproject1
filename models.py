from pydantic import BaseModel
from typing import List, Optional, Any

class Observation(BaseModel):
    dataset: List[dict]
    step_count: int
    quality_score: float

class Action(BaseModel):
    action_type: str
    column: Optional[str] = None
    value: Optional[Any] = None
    row_id: Optional[int] = None

class Reward(BaseModel):
    score: float
    reason: str