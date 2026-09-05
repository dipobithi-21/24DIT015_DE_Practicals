import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# LOAD EXPERIMENT RESULTS
# ==========================================

batch = pd.read_csv("results/batch_results.csv")
stream = pd.read_csv("results/streaming_results.csv")


# ==========================================
# CALCULATE PERFORMANCE METRICS
# ==========================================

# Batch processing latency
batch_latency = batch["latency_ms"].mean()

# Streaming delivery latency
stream_latency = stream["delivery_latency_ms"].mean()

# Batch processing time
batch_processing = batch["processing_time_ms"].mean()

# Streaming processing time
stream_processing = stream["processing_time_ms"].mean()

# Batch processing throughput
batch_throughput = batch["throughput_events_sec"].mean()

# Streaming processing throughput
stream_processing_time_seconds = (
    stream["processing_time_ms"].sum() / 1000
)

stream_throughput = (
    len(stream) / stream_processing_time_seconds
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("=" * 65)
print("             FINAL PERFORMANCE COMPARISON")
print("=" * 65)

print(f"Total batch events        : {len(batch) * 100}")
print(f"Total streaming events    : {len(stream)}")

print("\n--- LATENCY ---")

print(
    f"Batch average latency     : "
    f"{batch_latency:.4f} ms"
)

print(
    f"Streaming delivery latency: "
    f"{stream_latency:.4f} ms"
)

print("\n--- PROCESSING TIME ---")

print(
    f"Batch processing time     : "
    f"{batch_processing:.4f} ms"
)

print(
    f"Streaming processing time : "
    f"{stream_processing:.4f} ms"
)

print("\n--- THROUGHPUT ---")

print(
    f"Batch throughput          : "
    f"{batch_throughput:.2f} events/sec"
)

print(
    f"Streaming throughput      : "
    f"{stream_throughput:.2f} events/sec"
)

print("=" * 65)


# ==========================================
# LATENCY COMPARISON CHART
# ==========================================

plt.figure(figsize=(8, 5))

plt.bar(
    ["Batch", "Streaming"],
    [batch_latency, stream_latency]
)

plt.ylabel("Latency (ms)")
plt.xlabel("Pipeline")
plt.title("Batch vs Real-Time Streaming Latency")

plt.tight_layout()

plt.savefig(
    "results/latency_comparison.png",
    dpi=300
)

plt.show()


# ==========================================
# THROUGHPUT COMPARISON CHART
# ==========================================

plt.figure(figsize=(8, 5))

plt.bar(
    ["Batch", "Streaming"],
    [batch_throughput, stream_throughput]
)

plt.ylabel("Processing Throughput (events/sec)")
plt.xlabel("Pipeline")
plt.title("Batch vs Real-Time Streaming Throughput")

plt.tight_layout()

plt.savefig(
    "results/throughput_comparison.png",
    dpi=300
)

plt.show()


print("\nComparison charts generated successfully!")

print("\nSaved files:")
print("results/latency_comparison.png")
print("results/throughput_comparison.png")