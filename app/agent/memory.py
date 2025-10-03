import json
import os
from typing import Dict

MEMORY_FILE = "memory.json"


def load_memory(user_id: str) -> Dict:
    """Load user data from a JSON file."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
        return data.get(user_id, {})
    except (json.JSONDecodeError, IOError):
        return {}


def save_memory(user_id: str, data: Dict) -> None:
    """Save user data to a JSON file."""
    try:
        all_data = {}
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                all_data = json.load(f)
        all_data[user_id] = data
        with open(MEMORY_FILE, "w") as f:
            json.dump(all_data, f, indent=2)
    except (json.JSONDecodeError, IOError) as e:
        raise ValueError(f"Failed to save memory: {e}")
