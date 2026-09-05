import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value:
        json.dumps(value).encode("utf-8")
)

with open("activity_logs.json", "r") as file:
    events = json.load(file)

print("=" * 60)
print("REAL-TIME STREAMING PRODUCER")
print("=" * 60)

for event in events:

    # Record the exact time the event is sent
    event["send_timestamp"] = time.time()

    producer.send(
        "user-activity",
        value=event
    )

    print(
        f"Sent event: {event['event_id']}"
    )

    # Simulate continuous event arrival
    time.sleep(0.01)

producer.flush()
producer.close()

print("\nProducer completed successfully.")