import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def regulatory_compliance_score(answer: str):

    keywords = [

        "sar",
        "str",
        "aml",
        "compliance",
        "suspicious",
        "report"

    ]

    score = 0

    answer = answer.lower()

    for keyword in keywords:

        if keyword in answer:

            score += 1

    return round(

        score / len(keywords),

        2

    )


def citation_density(answer: str):

    citations = re.findall(

        r"\[.*?\]",

        answer

    )

    words = max(

        len(answer.split()),

        1

    )

    return round(

        len(citations) / words,

        3

    )


def role_appropriateness(

    role,

    retrieved_documents

):

    violations = 0

    total = max(

        len(retrieved_documents),

        1

    )

    for document in retrieved_documents:

        allowed = document.metadata.get(

            "allowed_roles",

            []

        )

        if allowed and role not in allowed:

            violations += 1

    return round(

        1 - (violations / total),

        2

    )


def hitl_trigger_precision(

    triggered,

    expected

):

    if expected == 0:

        return 1.0

    return round(

        triggered / expected,

        2

    )


def answer_stability(

    answer_one,

    answer_two

):

    embeddings = embedding_model.encode(

        [

            answer_one,

            answer_two

        ]

    )

    similarity = cosine_similarity(

        [embeddings[0]],

        [embeddings[1]]

    )[0][0]

    return round(

        float(similarity),

        3

    )


def golden_set_pass_rate(

    passed,

    total

):

    if total == 0:

        return 0

    return round(

        passed / total,

        2

    )