import json
import time
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "user-activity",
    bootstrap_servers="localhost:9092",
    group_id="spike-consumer-group",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda value:
        json.loads(value.decode("utf-8"))
)

count = 0
start = time.time()

print("=" * 60)
print("SPIKE CONSUMER")
print("=" * 60)
print("Waiting for traffic spike events...")

try:
    for message in consumer:
        count += 1

        if count % 500 == 0:
            elapsed = time.time() - start

            print(
                f"Processed: {count} | "
                f"Throughput: {count / elapsed:.2f} events/sec"
            )

        if count >= 3000:
            break

finally:
    consumer.close()

elapsed = time.time() - start

print("\n" + "=" * 60)
print("SPIKE CONSUMER SUMMARY")
print("=" * 60)

print(f"Total events processed : {count}")
print(f"Processing time        : {elapsed:.4f} seconds")
print(
    f"Throughput             : "
    f"{count / elapsed:.2f} events/sec"
)