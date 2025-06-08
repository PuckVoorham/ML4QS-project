import numpy as np
import pandas as pd
from scipy.stats import zscore
from sklearn.decomposition import PCA
import numpy as np

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

# Perform PCA on numeric sensor data columns
def perform_pca(df, time_col="Time (s)", n_components=3):
    df = df.dropna().copy()
    time = df[time_col].values
    
    axis_cols = [col for col in df.columns if col != time_col and np.issubdtype(df[col].dtype, np.number)]
    data_matrix = df[axis_cols].values
    
    # Dynamically adjust n_components
    max_components = min(n_components, data_matrix.shape[0], data_matrix.shape[1])
    
    pca = PCA(n_components=max_components)
    principal_components = pca.fit_transform(data_matrix)
    
    return time, principal_components, pca.explained_variance_ratio_, pca