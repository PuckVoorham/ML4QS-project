import sys
from pathlib import Path

# Setup
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.preprocessing.create_dataset import CreateDataset
# from src.visualization.plot_raw_signals import plot_raw_accelerometer
from src.visualization.plot_filtered_signals import plot_filtered_magnitude
# from src.visualization.plot_pca import plot_pca_projection

# Load dataset
data_path = project_root / 'data' / 'experiment_2_fietsen_puck'
creator = CreateDataset(base_dir=data_path, granularity_ms=100)

creator.add_numerical_dataset(
    file_name='Accelerometer.csv',
    timestamp_col='Time (s)',
    value_cols=['X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)'],
    aggregation='avg',
    prefix='acc_'
)

df = creator.data_table.dropna()

# Visualizations
# plot_raw_accelerometer(df)
plot_filtered_magnitude(df, granularity_ms=300)
# plot_pca_projection(df)
