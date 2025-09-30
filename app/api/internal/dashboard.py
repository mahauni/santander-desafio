import pandas as pd


def get_data():
    return pd.read_csv("data.csv", comment="#", sep=", ", header=0, engine="python")


def get_transactions_json():
    df = get_data()

    return df.to_json(orient="records", indent=4)


def get_value_per_types():
    df = get_data()

    df["value_numeric"] = (
        df["value"].str.replace("R$ ", "").str.replace(",", "").astype(float)
    )

    return df.groupby("type")["value_numeric"].sum().to_json()
