
import pandas as pd
import multiprocessing
import time

def analyze_chunk(chunk):
    avg_close = chunk['Close'].mean()
    max_price = chunk['High'].max()
    min_price = chunk['Low'].min()
    volatility = chunk['Close'].std()
    return avg_close, max_price, min_price, volatility

def serial_analysis(file_path):
    start = time.time()
    df = pd.read_csv(file_path)
    avg_close, max_price, min_price, volatility = analyze_chunk(df)
    end = time.time()
    print(f"[Serial] Time: {end - start:.4f} s")
    print(f"Avg Close: {avg_close:.2f}, Max: {max_price:.2f}, Min: {min_price:.2f}, Volatility: {volatility:.2f}")

def parallel_analysis(file_path, num_chunks=4):
    start = time.time()
    df = pd.read_csv(file_path)
    chunks = [df.iloc[i::num_chunks].copy() for i in range(num_chunks)]

    with multiprocessing.Pool(processes=num_chunks) as pool:
        results = pool.map(analyze_chunk, chunks)

    # Average results
    avg_close = sum(r[0] for r in results) / num_chunks
    max_price = max(r[1] for r in results)
    min_price = min(r[2] for r in results)
    volatility = sum(r[3] for r in results) / num_chunks

    end = time.time()
    print(f"[Parallel] Time: {end - start:.4f} s")
    print(f"Avg Close: {avg_close:.2f}, Max: {max_price:.2f}, Min: {min_price:.2f}, Volatility: {volatility:.2f}")

if __name__ == '__main__':
    file = 'large_stock_data.csv'
    print("\n--- Serial Analysis ---")
    serial_analysis(file)

    print("\n--- Parallel Analysis ---")
    parallel_analysis(file, num_chunks=multiprocessing.cpu_count())
