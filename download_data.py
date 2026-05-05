"""
Download NYC Yellow Taxi trip data (January 2024).
Source: NYC Taxi & Limousine Commission (TLC).
~48MB parquet file with ~2.96M rows and 19 columns.
"""
import os
import sys
import urllib.request

DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_PATH = os.path.join(DATA_DIR, "yellow_tripdata_2024-01.parquet")


def download():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DATA_PATH):
        size_mb = os.path.getsize(DATA_PATH) / (1024 * 1024)
        print(f"Dataset already exists at {DATA_PATH} ({size_mb:.1f} MB)")
        return DATA_PATH
    print(f"Downloading from {DATA_URL} ...")
    urllib.request.urlretrieve(DATA_URL, DATA_PATH)
    size_mb = os.path.getsize(DATA_PATH) / (1024 * 1024)
    print(f"Downloaded to {DATA_PATH} ({size_mb:.1f} MB)")
    return DATA_PATH


if __name__ == "__main__":
    download()
