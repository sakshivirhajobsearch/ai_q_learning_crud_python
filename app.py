from fastapi import FastAPI, HTTPException
from models import QValue
from database import init_db, get_connection
from q_learning import QLearningAgent

app = FastAPI(title="Q-Learning CRUD API")

# Initialize DB
init_db()

# Q-learning agent
agent = QLearningAgent(actions=["up", "down", "left", "right"])

@app.get("/")
def root():
    return {"message": "Q-Learning CRUD API is running"}

# CREATE
@app.post("/q_values")
def create_qvalue(qvalue: QValue):
    agent.set_q(qvalue.state, qvalue.action, qvalue.value)
    return {"message": "Q-value added successfully"}

# READ
@app.get("/q_values")
def read_qvalues():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM q_values")
    data = cursor.fetchall()
    conn.close()
    return [dict(row) for row in data]

# READ by state & action
@app.get("/q_values/{state}/{action}")
def read_qvalue(state: str, action: str):
    value = agent.get_q(state, action)
    return {"state": state, "action": action, "value": value}

# UPDATE
@app.put("/q_values")
def update_qvalue(qvalue: QValue):
    agent.set_q(qvalue.state, qvalue.action, qvalue.value)
    return {"message": "Q-value updated successfully"}

# DELETE
@app.delete("/q_values/{state}/{action}")
def delete_qvalue(state: str, action: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM q_values WHERE state=? AND action=?", (state, action))
    conn.commit()
    conn.close()
    return {"message": "Q-value deleted successfully"}

# TRAIN endpoint
@app.post("/train")
def train_agent(state: str, action: str, reward: float, next_state: str):
    agent.learn(state, action, reward, next_state)
    return {"message": "Agent trained on given experience"}
