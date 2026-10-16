"""Total revenue per region from a sales CSV. Usage: uv run report.py sales.csv --top 2"""
import argparse
import polars as pl


def main() -> None:
    parser = argparse.ArgumentParser(description="Revenue per region from a sales CSV.")
    parser.add_argument("csv_file", help="path to the CSV (columns: region, product, units, unit_price)")
    parser.add_argument("--top", type=int, default=3, help="how many regions to show (default: 3)")
    parser.add_argument("--product", help="keep only this product (default: all)")
    args = parser.parse_args()

    df = pl.read_csv(args.csv_file)
    if args.product:
        df = df.filter(pl.col("product") == args.product)
    result = (
        df.with_columns((pl.col("units") * pl.col("unit_price")).alias("revenue"))
        .group_by("region")
        .agg(pl.col("revenue").sum())
        .sort("revenue", descending=True)
        .head(args.top)
    )
    print(result)


if __name__ == "__main__":
    main()
