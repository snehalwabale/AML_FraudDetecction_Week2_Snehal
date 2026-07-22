import json
from pathlib import Path
from datetime import datetime

from eval.regression_suite import run_regression_suite


REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(
    exist_ok=True
)


def save_json(results):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file = REPORT_DIR / f"eval_{timestamp}.json"

    with open(

        file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            results,

            f,

            indent=4

        )

    return str(file)


def print_summary(summary):

    print()

    print("=" * 60)

    print(" AML & Fraud Detection Evaluation ")

    print("=" * 60)

    print()

    print(f"Total Questions : {summary['total']}")

    print(f"Passed          : {summary['passed']}")

    print(f"Pass Rate       : {summary['pass_rate'] * 100:.2f}%")

    print()

    print("=" * 60)


def run_all():

    results = run_regression_suite()

    report = save_json(results)

    print_summary(

        results["summary"]

    )

    return {

        "status": "completed",

        "report": report,

        "summary": results["summary"]

    }


if __name__ == "__main__":

    run_all()