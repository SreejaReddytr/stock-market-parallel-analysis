
import pandas as pd
import time

def analyze_serial(file_path):
    start = time.time()
    df = pd.read_csv(file_path)
    avg_close = df['Close'].mean()
    max_price = df['High'].max()
    min_price = df['Low'].min()
    volatility = df['Close'].std()
    end = time.time()

    print(f"[Serial] Time: {end - start:.4f} s")
    print(f"Avg Close: {avg_close:.2f}, Max: {max_price:.2f}, Min: {min_price:.2f}, Volatility: {volatility:.2f}")

if __name__ == '__main__':
    analyze_serial('large_stock_data.csv')
