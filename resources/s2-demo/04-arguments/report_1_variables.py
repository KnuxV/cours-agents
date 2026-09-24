# report_1_variables.py — étape 0 : les valeurs sont écrites dans le fichier
import pandas as pd

CSV_FILE = "sales.csv"      # on modifie ici…
TOP = 3                     # …et ici, puis on relance

df = pd.read_csv(CSV_FILE)
df["revenue"] = df["units"] * df["unit_price"]
result = df.groupby("region")["revenue"].sum().sort_values(ascending=False).head(TOP)
print(result)
