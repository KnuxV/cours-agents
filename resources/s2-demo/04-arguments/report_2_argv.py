# report_2_argv.py — les valeurs viennent du terminal, mais tout est à notre charge
import sys

import pandas as pd

if len(sys.argv) < 2:
    print("Usage: report_2_argv.py <fichier.csv> [top]")
    sys.exit(1)

csv_file = sys.argv[1]
top = int(sys.argv[2]) if len(sys.argv) > 2 else 3   # conversion à la main

df = pd.read_csv(csv_file)
df["revenue"] = df["units"] * df["unit_price"]
result = df.groupby("region")["revenue"].sum().sort_values(ascending=False).head(top)
print(result)
