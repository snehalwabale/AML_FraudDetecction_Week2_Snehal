import json
from pathlib import Path

from rag.qa_chain import generate_answer

from eval.llm_judge import judge_answer

from eval.custom_metrics import (
    regulatory_compliance_score,
    citation_density,
    role_appropriateness,
    answer_stability
)


GOLDEN_SET = Path(
    "eval/golden_set.json"
)


def load_golden_set():

    with open(
        GOLDEN_SET,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def run_regression_suite():

    dataset = load_golden_set()

    results = []

    passed = 0

    previous_answer = ""

    for sample in dataset:

        question = sample["question"]

        expected = sample["expected_answer"]

        role = sample.get(
            "role",
            "analyst"
        )

        answer, citations, trace = generate_answer(

            question,

            role

        )

        judge = judge_answer(

            question,

            answer,

            expected

        )

        compliance = regulatory_compliance_score(

            answer

        )

        density = citation_density(

            answer

        )

        role_score = role_appropriateness(

            role,

            trace

        )

        stability = 1.0

        if previous_answer:

            stability = answer_stability(

                previous_answer,

                answer

            )

        previous_answer = answer

        overall = (

            compliance

            + density

            + role_score

            + stability

        ) / 4

        if overall >= 0.85:

            passed += 1

        results.append(

            {

                "question": question,

                "expected": expected,

                "answer": answer,

                "judge": judge,

                "citations": citations,

                "metrics": {

                    "compliance": compliance,

                    "citation_density": density,

                    "role_score": role_score,

                    "stability": stability,

                    "overall": round(

                        overall,

                        2

                    )

                }

            }

        )

    summary = {

        "total": len(dataset),

        "passed": passed,

        "pass_rate": round(

            passed / len(dataset),

            2

        )

    }

    return {

        "summary": summary,

        "results": results

    }