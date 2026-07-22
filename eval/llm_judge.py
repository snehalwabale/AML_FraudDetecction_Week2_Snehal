from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

judge = ChatOpenAI(

    model="gpt-4o-mini",

    temperature=0

)


def judge_answer(

    question,

    answer,

    reference

):

    prompt = f"""
You are an independent AML compliance evaluator.

Question

{question}

Ground Truth

{reference}

Model Answer

{answer}

Evaluate using the following metrics.

1 Correctness (0-10)

2 Regulatory Compliance (0-10)

3 Completeness (0-10)

4 Hallucination Risk (0-10)

5 Overall Score (0-10)

Return ONLY

Correctness:
Compliance:
Completeness:
Hallucination:
Overall:
"""

    result = judge.invoke(prompt)

    return result.content