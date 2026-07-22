import json
import csv
from pathlib import Path
from datetime import datetime

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


def export_json(results):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = REPORT_DIR / f"evaluation_{timestamp}.json"

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=4
        )

    return str(file_path)


def export_csv(results):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = REPORT_DIR / f"evaluation_{timestamp}.csv"

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "Question",
            "Overall Score",
            "Compliance",
            "Citation Density",
            "Role Score",
            "Stability"
        ])

        for row in results["results"]:

            metrics = row["metrics"]

            writer.writerow([

                row["question"],

                metrics["overall"],

                metrics["compliance"],

                metrics["citation_density"],

                metrics["role_score"],

                metrics["stability"]

            ])

    return str(file_path)