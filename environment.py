import random
from typing import Dict, Any, Tuple

class BudgetTrackerEnv:
    def __init__(self):
        self.total_budget = 1000.0
        self.day = 1
        self.max_days = 30
        self.reset()

    def reset(self) -> Dict[str, Any]:
        self.remaining_budget = self.total_budget
        self.food_spent = 0.0
        self.transport_spent = 0.0
        self.savings = 0.0
        self.entertainment_spent = 0.0
        self.day = 1
        self.done = False
        return self.state()

    def state(self) -> Dict[str, Any]:
        return {
            "remaining_budget": round(self.remaining_budget, 2),
            "food_spent": round(self.food_spent, 2),
            "transport_spent": round(self.transport_spent, 2),
            "savings": round(self.savings, 2),
            "entertainment_spent": round(self.entertainment_spent, 2),
            "day": self.day,
            "month_target_savings": self.total_budget * 0.2
        }

    def step(self, action: str) -> Tuple[Dict, float, bool, Dict]:
        if self.done:
            return self.state(), 0.0, True, {"error": "Episode done, call reset()"}

        cost = round(random.uniform(10, 50), 2)
        cost = min(cost, self.remaining_budget)

        if action == "allocate_food":
            self.food_spent += cost
            self.remaining_budget -= cost
        elif action == "allocate_transport":
            self.transport_spent += cost
            self.remaining_budget -= cost
        elif action == "allocate_savings":
            self.savings += cost
            self.remaining_budget -= cost
        elif action == "allocate_entertainment":
            self.entertainment_spent += cost
            self.remaining_budget -= cost
        elif action == "skip":
            pass

        self.day += 1
        if self.day > self.max_days or self.remaining_budget <= 0:
            self.done = True

        reward = self._compute_reward()
        return self.state(), reward, self.done, {}

    def _compute_reward(self) -> float:
        savings_ratio = self.savings / self.total_budget
        food_ratio = self.food_spent / self.total_budget
        entertainment_ratio = self.entertainment_spent / self.total_budget

        reward = 0.0
        # Base reward for saving
        reward += min(savings_ratio / 0.3, 1.0) * 0.5
        # Penalty for overspending on food
        if food_ratio > 0.30:
            reward -= (food_ratio - 0.30) * 0.5
        # Penalty for entertainment overspend
        if entertainment_ratio > 0.10:
            reward -= (entertainment_ratio - 0.10) * 0.3
        # Bonus for having budget remaining
        reward += (self.remaining_budget / self.total_budget) * 0.2

        return round(max(0.0, min(1.0, reward)), 4)