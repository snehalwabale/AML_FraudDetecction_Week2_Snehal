from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

example_list = [

    {

        "question": "Analyze transactions for account 90-221",

        "answer": """
14 suspicious transactions detected.

8 structuring transactions identified.

Risk Score: 87

Recommendation:
File a Suspicious Activity Report (SAR).
"""

    },

    {

        "question": "Screen Viktor Petrov",

        "answer": """
Sanctions screening completed.

No confirmed OFAC match.

PEP Status: Negative.

Recommendation:
Continue monitoring.
"""

    },

    {

        "question": "Generate SAR",

        "answer": """
SAR Draft Generated.

AML Typology:
Structuring / Smurfing

Recommended Filing:
Within regulatory deadline.
"""

    }

]


def get_examples(question: str):

    question = question.lower()

    selected = []

    for example in example_list:

        if any(

            word in question

            for word in example["question"].lower().split()

        ):

            selected.append(example)

    if not selected:

        selected = example_list[:2]

    output = ""

    for example in selected:

        output += f"""

User:
{example["question"]}

Assistant:
{example["answer"]}

"""

    return output


prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
You are an AML & Fraud Detection Investigation Copilot.

You assist compliance officers, investigators and analysts.

Responsibilities:

- Transaction investigation
- AML typology detection
- Risk assessment
- Sanctions screening
- SAR assistance
- Regulatory guidance

Rules:

Use retrieved knowledge whenever available.

Use tool results whenever provided.

Do not fabricate facts.

If information is unavailable, clearly state that.

Keep responses concise, professional and suitable for banking investigations.
"""

        ),

        MessagesPlaceholder(

            variable_name="history"

        ),

        (

            "human",

            """
Relevant Examples

{examples}

Retrieved Context

{tool_output}

User Question

{question}
"""

        )

    ]

)