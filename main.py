from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Tuple

app = FastAPI(title="Q-Learning CRUD API")

# Data model for Q-value entry
class QValue(BaseModel):
    state: str
    action: str
    value: float

# In-memory Q-table storage: keys are (state, action) tuples
q_table: Dict[Tuple[str, str], float] = {}

@app.get("/")
def root():
    return {"message": "Welcome to the Q-Learning CRUD API"}

@app.post("/qvalue/", status_code=201)
def create_qvalue(qvalue: QValue):
    key = (qvalue.state, qvalue.action)
    if key in q_table:
        raise HTTPException(status_code=400, detail="Q-value for this state-action already exists.")
    q_table[key] = qvalue.value
    return {"message": "Q-value created", "qvalue": qvalue}

@app.get("/qvalue/{state}/{action}")
def read_qvalue(state: str, action: str):
    key = (state, action)
    if key not in q_table:
        raise HTTPException(status_code=404, detail="Q-value not found.")
    return {"state": state, "action": action, "value": q_table[key]}

@app.put("/qvalue/{state}/{action}")
def update_qvalue(state: str, action: str, qvalue: QValue):
    key = (state, action)
    if key not in q_table:
        raise HTTPException(status_code=404, detail="Q-value not found.")
    q_table[key] = qvalue.value
    return {"message": "Q-value updated", "qvalue": qvalue}

@app.delete("/qvalue/{state}/{action}", status_code=204)
def delete_qvalue(state: str, action: str):
    key = (state, action)
    if key not in q_table:
        raise HTTPException(status_code=404, detail="Q-value not found.")
    del q_table[key]
    return
