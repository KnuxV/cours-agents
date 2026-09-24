# report.py — chiffre d'affaires par région. Usage: uv run report.py sales.csv --top 2
import argparse
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Revenue per region from a sales CSV.")
    parser.add_argument("csv_file", help="path to the CSV (columns: region, product, units, unit_price)")
    parser.add_argument("--top", type=int, default=3, help="how many regions to show (default: 3)")
    parser.add_argument("--product", help="keep only this product (default: all)")
    args = parser.parse_args()

    df = pd.read_csv(args.csv_file)
    if args.product:
        df = df[df["product"] == args.product]
    df["revenue"] = df["units"] * df["unit_price"]
    result = (
        df.groupby("region")["revenue"].sum().sort_values(ascending=False).head(args.top)
    )
    print(result)


if __name__ == "__main__":
    main()
