
import os
import pandas as pd
import time

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
    results = [analyze_file(f) for f in files]
    end = time.time()

    print(f"[Serial] Total Execution Time: {end - start:.2f} seconds")
    df = pd.DataFrame(results)
    df.to_csv('serial_results.csv', index=False)

if __name__ == '__main__':
    main()
