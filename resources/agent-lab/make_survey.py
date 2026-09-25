"""Generate survey.csv — a fake labour-force survey, 1000 rows, standard library only.

The data-generating process is written down here on purpose: it is the ground
truth you check the agent's analysis against.

    log(income) = 9.6
                + 0.11 * years_of_schooling_above_12
                + 0.020 * years_experience
                + region_effect
                + noise (sd 0.25)

    region_effect: north +0.08, south -0.06, east -0.02, west 0.00
    education:     "high school" (0 extra years), "bachelor" (3),
                   "master" (5), "phd" (8)

Run it with:   python3 make_survey.py
"""

import csv
import math
import random

REGIONS = {"north": 0.08, "south": -0.06, "east": -0.02, "west": 0.00}
EDUCATION = {"high school": 0, "bachelor": 3, "master": 5, "phd": 8}

random.seed(20260925)

rows = []
for i in range(1, 1001):
    region = random.choice(list(REGIONS))
    education = random.choices(
        list(EDUCATION), weights=[0.35, 0.35, 0.22, 0.08]
    )[0]
    experience = min(random.randint(0, 40), 65 - 18 - EDUCATION[education])
    hours = round(random.gauss(37, 6), 1)
    log_income = (
        9.6
        + 0.11 * EDUCATION[education]
        + 0.020 * experience
        + REGIONS[region]
        + random.gauss(0, 0.25)
    )
    rows.append(
        {
            "id": i,
            "region": region,
            "education": education,
            "years_experience": experience,
            "hours_worked": hours,
            "income": round(math.exp(log_income), 2),
        }
    )

with open("survey.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

print(f"survey.csv written — {len(rows)} rows, columns: {', '.join(rows[0])}")
