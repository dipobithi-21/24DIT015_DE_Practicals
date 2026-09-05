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
print("TRAFFIC SPIKE PRODUCER")
print("=" * 60)

print("Sending events at high speed...")

start = time.time()

for i in range(3000):

    event = events[i % len(events)]

    event["spike_event_id"] = i + 1
    event["spike_timestamp"] = time.time()

    producer.send(
        "user-activity",
        value=event
    )

producer.flush()

elapsed = time.time() - start

print("\nTraffic spike completed.")

print(f"Events sent       : 3000")
print(f"Time taken        : {elapsed:.4f} seconds")
print(
    f"Spike throughput  : "
    f"{3000 / elapsed:.2f} events/sec"
)

producer.close()