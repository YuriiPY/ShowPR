
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class StoreTimePayload(BaseModel):
    until: Optional[str] = Field(None, description="Time in HH:MM format")
    close_now: Optional[bool] = False
