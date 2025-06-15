import pandas as pd
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.preprocessing.remove_noise import apply_kalman_filter

# Bestandsnamen van experimenten
experiment_names = [
    "auto",
    "auto2",
    "fietsen",
    "fietsen2",
    "metro2",
    "rennen",
    "rennen2",
    "trein",
    "trein2",
]

# Sensor-kolommen waarop we Kalman willen toepassen
sensor_columns = [
    'Accelerometer_X (m/s^2)', 'Accelerometer_Y (m/s^2)', 'Accelerometer_Z (m/s^2)',
    'Gyroscope_X (rad/s)', 'Gyroscope_Y (rad/s)', 'Gyroscope_Z (rad/s)',
    'Linear Accelerometer_X (m/s^2)', 'Linear Accelerometer_Y (m/s^2)', 'Linear Accelerometer_Z (m/s^2)',
    'Magnetometer_X (µT)', 'Magnetometer_Y (µT)', 'Magnetometer_Z (µT)',
    'Barometer_X (hPa)'
]

# Paden instellen
aggregated_dir = Path("data/final_datasets")
processed_dir = Path("data/processed_datasets")
processed_dir.mkdir(parents=True, exist_ok=True)

# Loop over de datasets
for name in experiment_names:
    input_path = aggregated_dir / f"{name}.csv"
    output_path = processed_dir / f"{name}_kalman_filtered.csv"

    df = pd.read_csv(input_path)

    print(f"🔄 Verwerken: {name}.csv")

    for col in sensor_columns:
        if col in df.columns:
            df[f"{col}_kalman"] = apply_kalman_filter(df[col])
        else:
            print(f"⚠️ Kolom niet gevonden: {col} in {name}.csv")
    
    # Alleen Kalman-kolommen + Time
    filtered_cols = ["Time (s)"] + [f"{col}_kalman" for col in sensor_columns if f"{col}_kalman" in df.columns]
    df_filtered = df[filtered_cols]

    df_filtered.to_csv(output_path, index=False)
    print(f"✅ Opgeslagen naar: {output_path}")
 