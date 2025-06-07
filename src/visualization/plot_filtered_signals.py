import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

def low_pass_filter(data, cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

def plot_filtered_magnitude(df, granularity_ms):
    df['acc_magnitude'] = (df[['acc_X (m/s^2)', 'acc_Y (m/s^2)', 'acc_Z (m/s^2)']] ** 2).sum(axis=1)**0.5
    fs = 1000 / granularity_ms
    df['acc_magnitude_filtered'] = low_pass_filter(df['acc_magnitude'], cutoff=1.0, fs=fs)

    plt.figure(figsize=(12, 4))
    plt.plot(df.index, df['acc_magnitude'], alpha=0.5, label='Raw')
    plt.plot(df.index, df['acc_magnitude_filtered'], label='Filtered', color='red')
    plt.title("Filtered Acceleration Magnitude")
    plt.xlabel("Time")
    plt.ylabel("Acceleration (m/s²)")
    plt.legend()
    plt.tight_layout()
    plt.show()


