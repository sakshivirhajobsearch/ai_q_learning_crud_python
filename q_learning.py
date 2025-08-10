import random
from database import get_connection

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q(self, state, action):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM q_values WHERE state=? AND action=?", (state, action))
        row = cursor.fetchone()
        conn.close()
        return row["value"] if row else 0.0

    def set_q(self, state, action, value):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO q_values (state, action, value)
            VALUES (?, ?, ?)
        """, (state, action, value))
        conn.commit()
        conn.close()

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        q_values = [(action, self.get_q(state, action)) for action in self.actions]
        max_q = max(q_values, key=lambda x: x[1])[1]
        best_actions = [a for a, q in q_values if q == max_q]
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        old_q = self.get_q(state, action)
        future_q = max([self.get_q(next_state, a) for a in self.actions], default=0.0)
        new_q = old_q + self.alpha * (reward + self.gamma * future_q - old_q)
        self.set_q(state, action, new_q)
