from typing import Optional

from pydantic import BaseModel


class CreateMidiRequest(BaseModel):
    tab: str
    tempo: Optional[int] = 100
    verbose: Optional[bool] = False
