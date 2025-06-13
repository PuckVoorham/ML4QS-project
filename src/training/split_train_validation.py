from sklearn.model_selection import train_test_split
import pandas as pd


def split_train_validation(df, label_col, val_size=0.2, random_state=42, stratify_col=None):
    """
    Splits training data into train and validation sets.

    df (pd.DataFrame): DataFrame met features en label
    label_col (str): Naam van de kolom met de target
    val_size (float): proportie voor validatie
    random_state (int): Seed
    stratify_col (str/None): Kolom om op te stratificeren (meestal label)
 
    """
    X = df.drop(columns=[label_col])
    y = df[label_col]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y,
        test_size=val_size,
        random_state=random_state,
        stratify=df[stratify_col] if stratify_col else None
    )

    return X_train, X_val, y_train, y_val



df = pd.read_csv("data/processed_datasets/aggregated_fietsen_kalman_filtered.csv")
print(df)
X_train, X_val, y_train, y_val = split_train_validation(df, label_col="label", stratify_col="label")
print(X_train, X_val, y_train, y_val)
