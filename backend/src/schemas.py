from typing import Optional

from pydantic import BaseModel


class CreateMidiRequest(BaseModel):
    tab: str
    tempo: Optional[int] = 100
    lines_per_tab: Optional[int] = 6
    verbose: Optional[bool] = False
