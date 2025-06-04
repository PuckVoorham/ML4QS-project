import pandas as pd
import numpy as np
import re
import copy
from datetime import datetime, timedelta
from pathlib import Path

####################### first try out #######################
# def load_sensor_csv(file_path, sensor_name):

#     """Load a CSV file and rename columns."""
#     df = pd.read_csv(file_path)

#     # Strip quotes and whitespace from columns
#     df.columns = [col.strip().replace('"', '') for col in df.columns]

#     # Rename time column uniformly
#     if 'Time (s)' in df.columns:
#         df.rename(columns={'Time (s)': 'time'}, inplace=True)

#     # Add a sensor column to identify the origin
#     df['sensor'] = sensor_name

#     return df
################################################################

class CreateDataset:
    def __init__(self, base_dir, granularity_ms=250):
        self.base_dir = Path(base_dir)
        self.granularity = granularity_ms
        self.data_table = None

    def create_timestamps(self, start_time, end_time):
        return pd.date_range(start=start_time, end=end_time, freq=f'{self.granularity}ms')

    def create_dataset(self, start_time, end_time, columns, prefix):
        prefixed_cols = [f"{prefix}{col}" for col in columns]
        timestamps = self.create_timestamps(start_time, end_time)
        self.data_table = pd.DataFrame(index=timestamps, columns=prefixed_cols, dtype=float)

    def add_numerical_dataset(self, file_name, timestamp_col, value_cols, aggregation='avg', prefix=''):
        file_path = self.base_dir / file_name
        print(f"Reading: {file_path}")
        df = pd.read_csv(file_path, skipinitialspace=True)

        df.columns = [col.strip().replace('"', '') for col in df.columns]
        df[timestamp_col] = pd.to_datetime(df[timestamp_col], unit='s')

        start_time, end_time = df[timestamp_col].min(), df[timestamp_col].max()

        if self.data_table is None:
            self.create_dataset(start_time, end_time, value_cols, prefix)
        else:
            for col in value_cols:
                full_col = f"{prefix}{col}"
                if full_col not in self.data_table.columns:
                    self.data_table[full_col] = np.nan

        for timestamp in self.data_table.index:
            time_window = df[(df[timestamp_col] >= timestamp) &
                             (df[timestamp_col] < timestamp + timedelta(milliseconds=self.granularity))]
            for col in value_cols:
                new_col = f"{prefix}{col}"
                if not time_window.empty:
                    self.data_table.at[timestamp, new_col] = time_window[col].mean() if aggregation == 'avg' else np.nan

    def clean_name(self, name):
        return re.sub('[^0-9a-zA-Z]+', '', name)

    def add_event_dataset(self, file_name, start_col, end_col, value_col, aggregation='sum'):
        file_path = self.base_dir / file_name
        print(f"Reading: {file_path}")
        df = pd.read_csv(file_path)
        df[start_col] = pd.to_datetime(df[start_col])
        df[end_col] = pd.to_datetime(df[end_col])
        df[value_col] = df[value_col].apply(self.clean_name)
        event_types = df[value_col].unique()

        if self.data_table is None:
            self.create_dataset(df[start_col].min(), df[end_col].max(), event_types, value_col)
        for event in event_types:
            col_name = f"{value_col}{event}"
            if col_name not in self.data_table:
                self.data_table[col_name] = 0

        for _, row in df.iterrows():
            relevant_rows = self.data_table[(row[start_col] <= (self.data_table.index + timedelta(milliseconds=self.granularity))) &
                                            (row[end_col] > self.data_table.index)]
            if aggregation == 'sum':
                self.data_table.loc[relevant_rows.index, f"{value_col}{row[value_col]}"] += 1
            elif aggregation == 'binary':
                self.data_table.loc[relevant_rows.index, f"{value_col}{row[value_col]}"] = 1

    def get_relevant_columns(self, patterns):
        return [col for pattern in patterns for col in self.data_table.columns if pattern in col]

