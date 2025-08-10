from pydantic import BaseModel

class QValue(BaseModel):
    state: str
    action: str
    value: float
