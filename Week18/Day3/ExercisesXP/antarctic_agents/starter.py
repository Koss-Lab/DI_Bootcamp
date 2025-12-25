import os
import json
import random
from typing import Dict, Any

from dotenv import load_dotenv
from smolagents import ToolCallingAgent, tool

load_dotenv()

print("🚀 Starting Antarctic Agents simulation...")

# -------------------------------
# Model loader (robust to versions)
# -------------------------------

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "HuggingFaceH4/zephyr-7b-beta")

def build_model():
    try:
        from smolagents import HfApiModel
        print("✅ Using smolagents.HfApiModel")
        return HfApiModel(
            model_id=HF_MODEL_ID,
            token=HF_TOKEN,
            provider="hf-inference",
        )
    except Exception:
        from smolagents import InferenceClientModel
        print("✅ Using smolagents.InferenceClientModel")
        return InferenceClientModel(
            model_id=HF_MODEL_ID,
            token=HF_TOKEN,
            provider="hf-inference",
        )

model = build_model()

# -------------------------------
# Global state
# -------------------------------
DISTRIBUTION_HISTORY: Dict[str, list] = {}

# -------------------------------
# Tools (strict docstrings)
# -------------------------------

@tool
def check_history(penguin_name: str) -> Dict[str, Any]:
    """
    Check the recent resource distribution history for a penguin.

    Args:
        penguin_name (str): The unique identifier of the penguin.

    Returns:
        Dict[str, Any]: Contains recent_food (int) and has_tool (bool).
    """
    history = DISTRIBUTION_HISTORY.get(penguin_name, [])
    recent_food = sum(h["food"] for h in history[-3:]) if history else 0
    has_tool = any(h["has_tool"] for h in history) if history else False
    return {"recent_food": recent_food, "has_tool": has_tool}

@tool
def record_distribution(penguin_name: str, food: int, has_tool: bool) -> str:
    """
    Record a resource distribution event.

    Args:
        penguin_name (str): Penguin identifier.
        food (int): Amount of food given.
        has_tool (bool): Whether a tool was given.

    Returns:
        str: Confirmation message.
    """
    if penguin_name not in DISTRIBUTION_HISTORY:
        DISTRIBUTION_HISTORY[penguin_name] = []
    DISTRIBUTION_HISTORY[penguin_name].append(
        {"food": food, "has_tool": has_tool}
    )
    return f"Recorded: {penguin_name} got {food} food and {'a' if has_tool else 'no'} tool"

@tool
def find_food(penguin_name: str, method: str) -> int:
    """
    Simulate independent food gathering by a penguin.

    Args:
        penguin_name (str): Penguin identifier.
        method (str): 'fishing' or 'foraging'.

    Returns:
        int: Amount of food found.
    """
    if method == "fishing":
        amount = random.randint(2, 7)
    else:
        amount = random.randint(0, 3)
    print(f"🐧 {penguin_name} found {amount} food using {method}")
    return amount

# -------------------------------
# Scientist Agent
# -------------------------------

class ScientistAgent(ToolCallingAgent):
    def __init__(self, initial_food_supply: int = 20, refresh_interval: int = 5):
        super().__init__(
            tools=[check_history, record_distribution],
            model=model,
            name="scientist",
            description="A scientist responding to penguin actions",
        )
        self.initial_food_supply = initial_food_supply
        self.food_supply = initial_food_supply
        self.tool_available = True
        self.refresh_interval = refresh_interval
        self.turn_counter = 0

    def refresh_resources(self):
        self.food_supply = self.initial_food_supply
        self.tool_available = True
        print("\n🔄 Scientist resources refreshed")

    def respond_to_action(self, penguin, penguin_action: Dict[str, Any]) -> None:
        self.turn_counter += 1
        if self.turn_counter % self.refresh_interval == 0:
            self.refresh_resources()

        print(f"\n🔬 Scientist reacts to {penguin.name}")
        print("Penguin action:", penguin_action)

        give_food = min(2, self.food_supply)
        give_tool = self.tool_available and random.random() < 0.3

        if give_food > 0:
            self.food_supply -= give_food
            penguin.food += give_food
        if give_tool:
            penguin.has_tool = True
            self.tool_available = False

        record_distribution(penguin.name, give_food, give_tool)

# -------------------------------
# Penguin Agent
# -------------------------------

class PenguinAgent(ToolCallingAgent):
    def __init__(self, name: str):
        super().__init__(tools=[find_food], model=model, name=name)
        self.name = name
        self.food = 0
        self.has_tool = False

    def take_action(self) -> Dict[str, Any]:
        if self.food < 2:
            action = {"action": "request_food"}
        elif self.has_tool:
            action = {"action": "find_food", "method": "fishing"}
        else:
            action = {"action": "find_food", "method": "foraging"}

        print(f"🐧 {self.name} decides:", action)
        return action

# -------------------------------
# Simulation
# -------------------------------

def run_simulation():
    scientist = ScientistAgent()
    penguins = [PenguinAgent(f"penguin_{i}") for i in range(4)]

    print("\n❄️ Simulation start ❄️")

    for round_idx in range(3):
        print(f"\n====== ROUND {round_idx + 1} ======")

        actions = {}

        for p in penguins:
            act = p.take_action()
            actions[p.name] = act

        for p in penguins:
            if actions[p.name]["action"] == "find_food":
                food = find_food(
                    p.name,
                    actions[p.name].get("method", "foraging"),
                )
                p.food += food

        for p in penguins:
            scientist.respond_to_action(p, actions[p.name])

    print("\n🏁 FINAL STATE")
    for p in penguins:
        hist = check_history(p.name)
        print(f"{p.name} → food={p.food}, had_tool={hist['has_tool']}")

if __name__ == "__main__":
    run_simulation()
