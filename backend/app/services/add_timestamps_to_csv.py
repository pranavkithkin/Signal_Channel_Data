import pandas as pd
from datetime import datetime, timezone

def add_timestamps_to_csv(input_csv, output_csv, timestamp_col='timestamp'):
    """
    Reads a CSV, ensures a proper ISO timestamp column, and writes to a new CSV.
    If the timestamp column exists but is not in ISO format, it will be converted.
    If the timestamp column is missing, it will add the current UTC time.
    """
    df = pd.read_csv(input_csv)

    # If timestamp column exists, try to parse and standardize it
    if timestamp_col in df.columns:
        df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce', utc=True)
        # Fill missing timestamps with current UTC time
        now = datetime.now(timezone.utc)
        df[timestamp_col] = df[timestamp_col].fillna(now)
        # Format as ISO string
        df[timestamp_col] = df[timestamp_col].dt.strftime('%Y-%m-%d %H:%M:%S%z')
    else:
        # If missing, add current UTC time for all rows
        now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
        df[timestamp_col] = now_str

    # Save to new CSV
    df.to_csv(output_csv, index=False)
    print(f"Saved with timestamps: {output_csv}")

if __name__ == "__main__":
    # Example usage:
    # python add_timestamps_to_csv.py input.csv output.csv
    import sys
    if len(sys.argv) != 3:
        print("Usage: python add_timestamps_to_csv.py input.csv output.csv")
    else:
        add_timestamps_to_csv(sys.argv[1], sys.argv[2])