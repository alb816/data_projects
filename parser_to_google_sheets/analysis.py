import pandas as pd


def analyze_data(input_file="tables/data.csv", output_file="tables/metrics.csv"):
    df = pd.read_csv(input_file)
    
    metrics = {
        "count": len(df),
        "mean_price": df["price in £"].mean(),
        "median_price": df["price in £"].median(),
        "min_price": df["price in £"].min(),
        "max_price": df["price in £"].max()
    }

    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(output_file, index=False)
    