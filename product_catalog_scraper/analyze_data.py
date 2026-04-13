import pandas as pd
from db import engine


def calculate_avg_price_by_category() -> pd.DataFrame:
    query = """
        SELECT category, price
        FROM books
    """
    df = pd.read_sql(query, engine)

    avg_price_by_category = (
        df
        .groupby("category", as_index=False)["price"]
        .mean()
    )

    return avg_price_by_category


def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    result_df = calculate_avg_price_by_category()
    save_to_csv(result_df, "data_processing/product_catalog_scraper/avg_price_by_category.csv")





