import json
import time
import os
import pandas as pd

from kafka import KafkaConsumer

os.makedirs("results", exist_ok=True)

consumer = KafkaConsumer(
    "user-activity",
    bootstrap_servers="localhost:9092",
    group_id="activity-consumer-group",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda value:
        json.loads(value.decode("utf-8"))
)

results = []

print("=" * 60)
print("REAL-TIME STREAMING CONSUMER")
print("=" * 60)

start_time = time.time()

for message in consumer:

    receive_time = time.time()

    event = message.value

    send_time = event["send_timestamp"]

    # End-to-end broker delivery latency
    delivery_latency = (
        receive_time - send_time
    ) * 1000

    process_start = time.time()

    # Process individual event using Pandas
    df = pd.DataFrame([event])

    high_cpu = (
        df["server_cpu"].iloc[0] > 80
    )

    processing_time = (
        time.time() - process_start
    ) * 1000

    results.append({
        "event_id": event["event_id"],
        "delivery_latency_ms": delivery_latency,
        "processing_time_ms": processing_time,
        "high_cpu": high_cpu
    })

    if len(results) % 100 == 0:

        print(
            f"Processed {len(results)} events | "
            f"Latest latency: "
            f"{delivery_latency:.4f} ms"
        )

    if len(results) >= 1000:
        break

consumer.close()

total_time = time.time() - start_time

result_df = pd.DataFrame(results)

result_df.to_csv(
    "results/streaming_results.csv",
    index=False
)

print("\n" + "=" * 60)
print("STREAMING PIPELINE SUMMARY")
print("=" * 60)

print(
    f"Total events        : {len(result_df)}"
)

print(
    f"Average delivery latency: "
    f"{result_df['delivery_latency_ms'].mean():.4f} ms"
)

print(
    f"Average processing time: "
    f"{result_df['processing_time_ms'].mean():.4f} ms"
)

print(
    f"Total execution time: "
    f"{total_time:.4f} seconds"
)

print(
    f"Overall throughput: "
    f"{len(result_df) / total_time:.2f} events/sec"
)

print("\nResults saved to:")
print("results/streaming_results.csv")