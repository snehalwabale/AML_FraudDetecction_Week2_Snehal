import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.tools import *


def test_transaction_analyzer():

    result = analyze_transactions(
        "55-389"
    )

    assert result["risk_score"] > 0


def test_sar_generator():

    result = generate_sar(

        "55-389",

        "Structuring"
    )

    assert "SAR" in result


def test_sanctions():

    result = screen_name(
        "Viktor Petrov"
    )

    assert result["confidence"] > 0


def test_risk_score():

    result = get_risk_score(
        "C-7781"
    )

    assert result["risk_score"] > 0


def test_alert_summary():

    result = alert_summary()

    assert result["open_alerts"] >= 0