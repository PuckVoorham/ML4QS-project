import sys
from pathlib import Path

# Setup project root
project_root = Path(__file__).resolve().parent.parent 
sys.path.append(str(project_root))

from src.preprocessing.create_dataset import CreateDataset

# Path to experiment folder
data_path = project_root / 'data' / 'experiment_2_fietsen_puck'

# Create dataset object
granularity = 100  # milliseconds
creator = CreateDataset(base_dir=data_path, granularity_ms=granularity)

# Try to load one sensor file
file_name = 'Accelerometer.csv'
timestamp_col = 'Time (s)' 
value_cols = ['X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)']
prefix = 'acc_'

creator.add_numerical_dataset(file_name=file_name,
                               timestamp_col=timestamp_col,
                               value_cols=value_cols,
                               aggregation='avg',
                               prefix=prefix)

# Check the first few rows of the generated dataset
print(creator.data_table.head(10))
