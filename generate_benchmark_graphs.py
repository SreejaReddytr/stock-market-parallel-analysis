import pandas as pd
import matplotlib.pyplot as plt

# Updated execution times from actual tests
execution_times = {
    "Serial (C++, 50 files)": 0.095,
    "Parallel Threads (C++, 50 files)": 0.047,
    "OpenMP (C++, 50 files)": 0.026,
    "Serial (Python, 50 files)": 0.100,
    "Parallel (Python, 50 files)": 0.950,
    "Serial (Python, large file)": 0.125,
    "Parallel (Python, large file)": 1.0428,
    "Optimized Parallel (Python, large file)": 1.2622
}

# Create DataFrame
df = pd.DataFrame(list(execution_times.items()), columns=["Implementation", "Time (s)"])

# Plot 1: Execution Time Comparison
plt.figure(figsize=(12, 6))
plt.bar(df["Implementation"], df["Time (s)"], color='royalblue')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time Comparison: Serial vs. Parallel (Python & C++)")
plt.tight_layout()
plt.savefig("execution_time_comparison_final.png")
plt.close()

# Plot 2: Speedup vs. C++ Serial (Large File)
baseline = 0.82  # Time of C++ Serial (large file)
df["Speedup vs C++ Serial (Large File)"] = df["Time (s)"].apply(lambda x: round(baseline / x, 2))
plt.figure(figsize=(12, 6))
plt.bar(df["Implementation"], df["Speedup vs C++ Serial (Large File)"], color='seagreen')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Speedup (x)")
plt.title("Speedup vs. C++ Serial (Large File)")
plt.tight_layout()
plt.savefig("speedup_vs_cpp_serial_final.png")
plt.close()
