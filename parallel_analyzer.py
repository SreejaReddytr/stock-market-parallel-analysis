
import os
import pandas as pd
import time
from multiprocessing import Pool, cpu_count

def analyze_file(filepath):
    df = pd.read_csv(filepath)
    avg_close = df['Close'].mean()
    max_price = df['High'].max()
    min_price = df['Low'].min()
    volatility = df['Close'].std()
    return {
        'file': os.path.basename(filepath),
        'avg_close': avg_close,
        'max_price': max_price,
        'min_price': min_price,
        'volatility': volatility
    }

def main():
    input_dir = '../data'
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]

    start = time.time()
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(analyze_file, files)
    end = time.time()

    print(f"[Parallel] Total Execution Time: {end - start:.2f} seconds")
    df = pd.DataFrame(results)
    df.to_csv('parallel_results.csv', index=False)

if __name__ == '__main__':
    main()
