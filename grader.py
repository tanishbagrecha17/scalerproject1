import pandas as pd


def grade_dataset(df: pd.DataFrame):
    score = 0.0

    # Check duplicates
    if not df.duplicated().any():
        score += 0.2

    # Check missing customers
    if not df["customer"].isnull().any():
        score += 0.2

    # Check negative amounts
    if not (df["amount"] < 0).any():
        score += 0.2

    # Check valid dates
    try:
        pd.to_datetime(df["date"], errors="raise")
        score += 0.2
    except:
        pass

    # Check reasonable amount (simple anomaly detection)
    if (df["amount"] < 100000).all():
        score += 0.2

    return round(score, 2)