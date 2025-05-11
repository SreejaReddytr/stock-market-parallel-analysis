
import pandas as pd
import numpy as np
import multiprocessing
import time

def analyze_chunk(chunk):
    avg_close = chunk['Close'].mean()
    max_price = chunk['High'].max()
    min_price = chunk['Low'].min()
    volatility = chunk['Close'].std()
    return avg_close, max_price, min_price, volatility

def analyze_parallel_optimized(file_path, num_chunks=4):
    start = time.time()
    df = pd.read_csv(file_path)
    chunks = np.array_split(df, num_chunks)

    with multiprocessing.Pool(processes=num_chunks) as pool:
        results = pool.map(analyze_chunk, chunks)

    avg_close = sum(r[0] for r in results) / num_chunks
    max_price = max(r[1] for r in results)
    min_price = min(r[2] for r in results)
    volatility = sum(r[3] for r in results) / num_chunks

    end = time.time()
    print(f"[Optimized Parallel] Time: {end - start:.4f} s")
    print(f"Avg Close: {avg_close:.2f}, Max: {max_price:.2f}, Min: {min_price:.2f}, Volatility: {volatility:.2f}")

if __name__ == '__main__':
    analyze_parallel_optimized('large_stock_data.csv', num_chunks=multiprocessing.cpu_count())
