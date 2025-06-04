import pandas as pd
import os

def load_sensor_csv(file_path, sensor_name):

    """Load a CSV file and rename columns."""
    df = pd.read_csv(file_path)

    # Strip quotes and whitespace from columns
    df.columns = [col.strip().replace('"', '') for col in df.columns]

    # Rename time column uniformly
    if 'Time (s)' in df.columns:
        df.rename(columns={'Time (s)': 'time'}, inplace=True)

    # Add a sensor column to identify the origin
    df['sensor'] = sensor_name

    return df
