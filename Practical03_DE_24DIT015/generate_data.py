import json
import random
from datetime import datetime

events = []

users = [f"U{i:03d}" for i in range(1, 21)]

actions = [
    "login",
    "logout",
    "page_view",
    "search",
    "add_to_cart",
    "checkout"
]

for i in range(1000):

    event = {
        "event_id": i + 1,
        "user_id": random.choice(users),
        "action": random.choice(actions),
        "server_cpu": round(random.uniform(20, 95), 2),
        "server_memory": round(random.uniform(30, 90), 2),
        "timestamp": datetime.now().isoformat()
    }

    events.append(event)

with open("activity_logs.json", "w") as file:
    json.dump(events, file, indent=2)

print("1000 events generated successfully.")