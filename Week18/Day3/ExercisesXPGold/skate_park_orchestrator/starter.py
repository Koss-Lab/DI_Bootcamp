import os
import re
from datetime import datetime, timedelta
from typing import Dict

from dotenv import load_dotenv
from smolagents import ToolCallingAgent, tool

load_dotenv()

print("🚀 Starting Skate Park Orchestrator (XP GOLD)...")

# -------------------------------------------------
# Model loader (robust with recent smolagents)
# -------------------------------------------------
def build_model():
    try:
        from smolagents import HfApiModel
        print("✅ Using smolagents.HfApiModel")
        return HfApiModel(
            model_id=os.getenv("HF_MODEL_ID", "HuggingFaceH4/zephyr-7b-beta"),
            token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            provider="hf-inference",
        )
    except Exception:
        from smolagents import InferenceClientModel
        print("✅ Using smolagents.InferenceClientModel")
        return InferenceClientModel(
            model_id=os.getenv("HF_MODEL_ID", "HuggingFaceH4/zephyr-7b-beta"),
            token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            provider="hf-inference",
        )

model = build_model()

# ---------------------- Domain Models ----------------------

class BookingSystem:
    def __init__(self):
        self.bookings: Dict[str, Dict[str, str]] = {}

    def check_availability(self, date: str, time: str) -> bool:
        return time not in self.bookings.get(date, {})

    def add_booking(self, date: str, time: str, customer: str) -> None:
        self.bookings.setdefault(date, {})
        self.bookings[date][time] = customer

    def get_bookings(self, date: str) -> Dict[str, str]:
        return self.bookings.get(date, {})

booking_system = BookingSystem()

# ---------------------- Park Tools ----------------------

@tool
def check_booking_availability(date: str, time: str) -> str:
    """
    Check whether a park booking slot is available.

    Args:
        date (str): Booking date in YYYY-MM-DD format.
        time (str): Booking time in HH:MM format.

    Returns:
        str: "available" if the slot is free, otherwise "unavailable".
    """
    return "available" if booking_system.check_availability(date, time) else "unavailable"

@tool
def add_new_booking(date: str, time: str, customer: str) -> str:
    """
    Add a new park booking.

    Args:
        date (str): Booking date in YYYY-MM-DD format.
        time (str): Booking time in HH:MM format.
        customer (str): Name of the customer.

    Returns:
        str: Confirmation message.
    """
    booking_system.add_booking(date, time, customer)
    return f"Booking confirmed for {customer} on {date} at {time}."

@tool
def get_all_bookings(date: str) -> Dict[str, str]:
    """
    Retrieve all bookings for a given date.

    Args:
        date (str): Booking date in YYYY-MM-DD format.

    Returns:
        Dict[str, str]: Mapping of time slots to customer names.
    """
    return booking_system.get_bookings(date)

# ---------------------- Inventory ----------------------

class Inventory:
    def __init__(self):
        self.stock = {
            "skateboard": 20,
            "helmet": 30,
            "wheels": 50,
        }

    def check_stock(self, item: str) -> int:
        return self.stock.get(item, 0)

    def sell_item(self, item: str, quantity: int) -> bool:
        if self.stock.get(item, 0) >= quantity:
            self.stock[item] -= quantity
            return True
        return False

inventory = Inventory()

@tool
def get_inventory_level(item: str) -> str:
    """
    Get current stock level for an item.

    Args:
        item (str): Inventory item name.

    Returns:
        str: Item name and remaining quantity.
    """
    return f"{item}:{inventory.check_stock(item)}"

@tool
def sell_inventory_item(item: str, quantity: int) -> str:
    """
    Sell an item from inventory.

    Args:
        item (str): Inventory item name.
        quantity (int): Quantity to sell.

    Returns:
        str: "sold" if successful, otherwise "failed".
    """
    return "sold" if inventory.sell_item(item, quantity) else "failed"

# ---------------------- Agents ----------------------

class CustomerSupportAgent(ToolCallingAgent):
    def __init__(self):
        super().__init__(
            tools=[],
            model=model,
            name="customer_support_agent",
            description="Diagnose customer intent and provide initial guidance.",
        )

    def diagnose_issue(self, request: str) -> str:
        r = request.lower()
        if any(k in r for k in ["buy", "stock", "skateboard", "helmet", "wheels"]):
            return "Shop"
        if any(k in r for k in ["book", "park", "session", "rent"]):
            return "Park"
        if any(k in r for k in ["broken", "repair"]):
            return "Repair"
        return "Unknown"

class InventoryAgent(ToolCallingAgent):
    def __init__(self):
        super().__init__(
            tools=[get_inventory_level, sell_inventory_item],
            model=model,
            name="inventory_agent",
            description="Manage inventory stock and sales.",
        )

class ParkManagementAgent(ToolCallingAgent):
    def __init__(self):
        super().__init__(
            tools=[check_booking_availability, add_new_booking, get_all_bookings],
            model=model,
            name="park_management_agent",
            description="Manage park bookings and schedules.",
        )

# ---------------------- Orchestrator ----------------------

class Orchestrator(ToolCallingAgent):
    def __init__(self):
        super().__init__(
            tools=[],
            model=model,
            name="orchestrator",
            description="Coordinate agents to handle customer requests end-to-end.",
        )
        self.support = CustomerSupportAgent()
        self.inventory = InventoryAgent()
        self.park = ParkManagementAgent()

    def handle_request(self, user_request: str, customer_name: str = "Guest") -> str:
        diagnosis = self.support.diagnose_issue(user_request)

        date_match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", user_request)
        time_match = re.search(r"\b\d{2}:\d{2}\b", user_request)
        buy_match = re.search(r"buy\s+(\d+)\s+(\w+)", user_request.lower())

        # -------- Park flow --------
        if diagnosis == "Park" and date_match and time_match:
            date = date_match.group()
            time = time_match.group()
            status = check_booking_availability(date, time)
            if status == "available":
                return add_new_booking(date, time, customer_name)

            alt_time = (
                datetime.strptime(time, "%H:%M") + timedelta(hours=1)
            ).strftime("%H:%M")
            return f"Slot unavailable. How about {date} at {alt_time}?"

        # -------- Shop flow --------
        if diagnosis == "Shop":
            if buy_match:
                qty = int(buy_match.group(1))
                item = buy_match.group(2)
                result = sell_inventory_item(item, qty)
                if result == "sold":
                    return f"✅ Sold {qty} {item}(s)."
                return f"❌ Not enough stock for {item}."
            return get_inventory_level("skateboard")

        if diagnosis == "Repair":
            return "Thanks — our Nairobi repair team will contact you shortly."

        return "Could you clarify your request?"

# ---------------------- Demo ----------------------

if __name__ == "__main__":
    orch = Orchestrator()

    print("\n--- Demo in Action (XP GOLD) ---\n")

    req1 = "I want to book a skate session for 2025-09-12 at 10:00."
    print("Response:", orch.handle_request(req1, "Aisha"))

    req2 = "Do you have skateboards? Can I buy 2 skateboards?"
    print("Response:", orch.handle_request(req2, "Brian"))

    req3 = "My helmet is broken!"
    print("Response:", orch.handle_request(req3, "Cynthia"))
