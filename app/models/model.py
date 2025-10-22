from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class Strings(BaseModel):
    id: Optional[str] = None
    value: str

class Analyze_string(Strings):
    properties: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)