import time

from rag.qa_chain import generate_answer


TEST_SET = [

    {
        "question": "Explain Structuring",
        "expected": "Structuring"
    },

    {
        "question": "What is Smurfing?",
        "expected": "Smurfing"
    },

    {
        "question": "What is AML?",
        "expected": "Anti Money Laundering"
    },

    {
        "question": "What is a Suspicious Activity Report?",
        "expected": "SAR"
    },

    {
        "question": "Explain PEP",
        "expected": "Politically Exposed Person"
    }

]


def evaluate():

    results = []

    total = len(TEST_SET)

    passed = 0

    total_time = 0

    for sample in TEST_SET:

        start = time.time()

        answer, citations, trace = generate_answer(

            sample["question"]

        )

        latency = round(

            time.time() - start,

            3

        )

        total_time += latency

        success = sample["expected"].lower() in answer.lower()

        if success:

            passed += 1

        results.append(

            {

                "question": sample["question"],

                "expected": sample["expected"],

                "answer": answer,

                "success": success,

                "latency": latency,

                "citations": len(citations)

            }

        )

    accuracy = round(

        (passed / total) * 100,

        2

    )

    avg_latency = round(

        total_time / total,

        3

    )

    return {

        "status": "completed",

        "accuracy": accuracy,

        "average_latency": avg_latency,

        "total_questions": total,

        "passed": passed,

        "failed": total - passed,

        "results": results

    }


def run_all():

    return evaluate()


if __name__ == "__main__":

    from pprint import pprint

    pprint(

        evaluate()

    )