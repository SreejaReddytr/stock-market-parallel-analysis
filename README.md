
# 🧠 Parallel Analysis of Stock Market Data

**Author:** Mary Sreeja Thirumala Reddy  
**Course:** Parallel Programming  
**Final Project Report Included**

---

## 📘 Overview

This project explores how **parallel programming techniques** can accelerate the analysis of large-scale stock market data using:

- 🐍 Python (Serial & Multiprocessing)
- 💻 C++ (std::thread and OpenMP)
- 📈 Performance Benchmarking + Visualizations

---

## 🧪 Problem Statement

Given 50+ CSV files (or one large file with 100,000 rows), the program calculates:

- Average Closing Price  
- Maximum & Minimum Stock Price  
- Volatility (Standard Deviation of Close)

The goal is to measure **execution time improvements** when using parallel approaches vs. serial.

---

## 📂 Project Structure

```
stock_market_parallel_project/
├── data/                             # Stock data CSVs
├── graphs/                           # Auto-generated charts
├── python/                           # Python implementations
├── cpp/                              # C++ and OpenMP implementations
├── Parallel_Stock_Report.pdf         # Full technical report
├── final_graph_generator.py          # Plots benchmark results
└── README.md
```

---

## 🚀 How to Run

### Python (Serial & Parallel)
```bash
cd python
python3 serial_analyzer.py                         # 50 small files
python3 parallel_analyzer.py                       # multiprocessing (50 files)

python3 serial_large_file_analyzer.py              # 1 large file (serial)
python3 parallel_large_file_analyzer.py            # 1 large file (basic parallel)
python3 parallel_large_file_analyzer_optimized.py  # 1 large file (optimized chunks)

python3 final_graph_generator.py                   # generate benchmark charts
```

### C++ (Serial, Threads, OpenMP)
```bash
cd cpp

# Compile
g++ -std=c++17 -O2 serial_analyzer.cpp -o serial_analyzer
g++ -std=c++17 -O2 -pthread parallel_threads.cpp -o parallel_threads
g++ -std=c++17 -O2 -fopenmp parallel_openmp.cpp -o parallel_openmp  # requires libomp

# Run
./serial_analyzer
./parallel_threads
./parallel_openmp
```

---

## 📊 Sample Benchmark Results

| Implementation                  | Time (s) | Speedup vs C++ Serial |
|---------------------------------|----------|------------------------|
| C++ Serial (50 files)           | 0.095    | 1.00x                  |
| C++ OpenMP (large)              | 0.18     | 4.56x ✅ Best           |
| Python Serial (large)           | 0.125    | 0.73x                  |
| Python Parallel (large)         | 1.04     | 1.86x                  |

---

## 🔬 Key Learnings

- Python multiprocessing has high overhead unless data is very large
- OpenMP is the most efficient and developer-friendly parallel model
- Parallelism helps most when input is **huge and CPU-bound**
- Serial Python is still competitive for small datasets

---

## 📎 Report

See `Parallel_Stock_Report.pdf` for full explanation, tables, charts, and reflections.

---

## 🧠 Future Work

- GPU-based acceleration using CUDA
- Stream-based processing for real-time stock feeds
- Distributed scaling with Dask or MPI
