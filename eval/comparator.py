import json


def compare_reports(

    baseline_file,

    current_file

):

    with open(

        baseline_file,

        "r",

        encoding="utf-8"

    ) as f:

        baseline = json.load(f)

    with open(

        current_file,

        "r",

        encoding="utf-8"

    ) as f:

        current = json.load(f)

    base_rate = baseline["summary"]["pass_rate"]

    current_rate = current["summary"]["pass_rate"]

    improvement = round(

        current_rate - base_rate,

        2

    )

    return {

        "baseline": base_rate,

        "current": current_rate,

        "improvement": improvement,

        "status": (

            "Improved"

            if improvement >= 0

            else "Regressed"

        )

    }