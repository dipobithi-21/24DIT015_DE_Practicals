import json
import time
import pandas as pd
import os

INPUT_FILE = "activity_logs.json"
BATCH_SIZE = 100
BATCH_INTERVAL = 1

os.makedirs("results", exist_ok=True)

# Load test data
with open(INPUT_FILE, "r") as file:
    events = json.load(file)

results = []

print("=" * 60)
print("PERIODIC BATCH INGESTION PIPELINE")
print("=" * 60)

total_start = time.time()

for start in range(0, len(events), BATCH_SIZE):

    batch = events[start:start + BATCH_SIZE]

    batch_start = time.time()

    # Convert batch to Pandas DataFrame
    df = pd.DataFrame(batch)

    # Example telemetry processing
    df["high_cpu"] = df["server_cpu"] > 80

    high_cpu_events = int(df["high_cpu"].sum())

    # Processing time
    processing_time = time.time() - batch_start

    # Throughput
    throughput = (
        len(df) / processing_time
        if processing_time > 0
        else 0
    )

    # Processing latency
    latency_ms = processing_time * 1000

    batch_number = len(results) + 1

    results.append({
        "batch_number": batch_number,
        "events": len(df),
        "high_cpu_events": high_cpu_events,
        "processing_time_ms": latency_ms,
        "throughput_events_sec": throughput,
        "latency_ms": latency_ms
    })

    print(
        f"Batch {batch_number:02d} | "
        f"Events: {len(df)} | "
        f"High CPU: {high_cpu_events} | "
        f"Latency: {latency_ms:.4f} ms | "
        f"Throughput: {throughput:.2f} events/sec"
    )

    # Simulate periodic batch trigger
    time.sleep(BATCH_INTERVAL)

total_time = time.time() - total_start

result_df = pd.DataFrame(results)

result_df.to_csv(
    "results/batch_results.csv",
    index=False
)

print("\n" + "=" * 60)
print("BATCH PIPELINE SUMMARY")
print("=" * 60)

print(
    f"Total events       : {len(events)}"
)

print(
    f"Number of batches  : {len(result_df)}"
)

print(
    f"Average latency    : "
    f"{result_df['latency_ms'].mean():.4f} ms"
)

print(
    f"Average throughput  : "
    f"{result_df['throughput_events_sec'].mean():.2f} events/sec"
)

print(
    f"Total execution time: "
    f"{total_time:.2f} seconds"
)

print("\nResults saved to:")
print("results/batch_results.csv")