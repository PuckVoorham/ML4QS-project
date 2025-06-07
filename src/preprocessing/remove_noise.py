import numpy as np
import pandas as pd
from scipy.stats import zscore

# apply 1d kalman filter
def apply_kalman_filter(series, process_variance=1e-5, measurement_variance=0.1**2):
    n = len(series)
    xhat = np.zeros(n)
    P = np.zeros(n)
    xhatminus = np.zeros(n)
    Pminus = np.zeros(n)
    K = np.zeros(n)

    xhat[0] = series.iloc[0]
    P[0] = 1.0

    for k in range(1, n):
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + process_variance

        K[k] = Pminus[k] / (Pminus[k] + measurement_variance)
        xhat[k] = xhatminus[k] + K[k] * (series.iloc[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]

    return pd.Series(xhat, index=series.index)

# Z-score based outlier detection
def detect_outliers(series, threshold=3.0):
    z_scores = zscore(series.dropna())
    outliers = np.abs(z_scores) > threshold
    return pd.Series(outliers, index=series.dropna().index).reindex(series.index, fill_value=False)

from scipy.signal import butter, filtfilt

# Butterworth low-pass filter
def apply_lowpass_filter(data, cutoff=2.0, fs=50.0, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)
