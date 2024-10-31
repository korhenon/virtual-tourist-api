from typing import Annotated, Optional

from fastapi import Header
from pydantic import BaseModel

TokenHeader = Annotated[Optional[str], Header()]


class MessageResponse(BaseModel):
    message: str
