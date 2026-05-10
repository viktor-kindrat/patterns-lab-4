import csv
import random
from datetime import datetime, timedelta


CRIME_TYPES = [
    "THEFT", "BURGLARY", "ASSAULT", "VANDALISM", "ROBBERY",
    "FRAUD", "DUI", "DRUG OFFENSE", "TRESPASSING", "DISORDERLY CONDUCT",
]

DISPOSITIONS = [
    "ARREST MADE", "CLOSED - NO LEADS", "UNFOUNDED",
    "EXCEPTIONALLY CLEARED", "OPEN/ACTIVE",
]

DISTRICTS = ["A1", "B1", "C1", "D1", "E1", "F1", "G1"]

STREETS = [
    "MAIN ST", "STATE ST", "SOUTH TEMPLE", "NORTH TEMPLE",
    "WEST TEMPLE", "BROADWAY", "200 SOUTH", "400 SOUTH",
    "900 SOUTH", "1300 SOUTH",
]

UCR_DESCRIPTIONS = [
    "LARCENY-THEFT", "BURGLARY", "AGGRAVATED ASSAULT",
    "MOTOR VEHICLE THEFT", "ROBBERY", "FRAUD", "VANDALISM",
    "DRUG/NARCOTIC VIOLATIONS", "DRIVING UNDER INFLUENCE",
]

FIELDNAMES = [
    "CASENO", "REPORTEDDATETIME", "OCCURRED_DATETIME",
    "CRIMEGRADE", "CRIMETYPE", "ADDRESS", "CITY",
    "ZIPCODE", "POLICEDISTRICT", "DISPOSITION", "UCRDESC",
]


def _random_date() -> str:
    start = datetime(2016, 1, 1)
    offset = timedelta(days=random.randint(0, 365), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return (start + offset).strftime("%Y-%m-%dT%H:%M:%S")


def generate(file_path: str, count: int = 200) -> None:
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for i in range(count):
            reported = _random_date()
            writer.writerow({
                "CASENO": f"16-{100000 + i}",
                "REPORTEDDATETIME": reported,
                "OCCURRED_DATETIME": reported,
                "CRIMEGRADE": random.choice(["FELONY", "MISDEMEANOR", "INFRACTION"]),
                "CRIMETYPE": random.choice(CRIME_TYPES),
                "ADDRESS": f"{random.randint(100, 999)} {random.choice(STREETS)}",
                "CITY": "SALT LAKE CITY",
                "ZIPCODE": str(random.choice([84101, 84102, 84103, 84104, 84105, 84106, 84107, 84108])),
                "POLICEDISTRICT": random.choice(DISTRICTS),
                "DISPOSITION": random.choice(DISPOSITIONS),
                "UCRDESC": random.choice(UCR_DESCRIPTIONS),
            })
    print(f"[Generator] Created {count} sample records at '{file_path}'.")
