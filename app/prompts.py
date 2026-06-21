from langchain_core.prompts import (
    ChatPromptTemplate
)

# =====================================================
# FEW SHOT EXAMPLES
# =====================================================

example_list = [

    {
        "question":
        "Analyze transactions for account 90-221",

        "answer":
        """
14 transactions flagged.

8 structuring transactions.

4 rapid transfers.

Risk Score: 87

Recommend SAR Filing.
"""
    },

    {
        "question":
        "Screen Viktor Petrov",

        "answer":
        """
OFAC Match Found.

Confidence: 94%

Action:
Freeze Account
"""
    },

    {
        "question":
        "Generate SAR",

        "answer":
        """
SAR Draft Generated.

Structuring activity detected.

Deadline:
30 Days
"""
    }

]


# =====================================================
# SEMANTIC EXAMPLE SELECTOR
# =====================================================

def get_examples(user_question):

    user_question = user_question.lower()

    selected_examples = []

    for ex in example_list:

        if any(

            word in user_question

            for word in

            ex["question"].lower().split()

        ):

            selected_examples.append(ex)

    if not selected_examples:

        selected_examples = example_list[:2]

    output = ""

    for ex in selected_examples:

        output += f"""

User:
{ex['question']}

Assistant:
{ex['answer']}

"""

    return output


# =====================================================
# PROMPT TEMPLATE
# =====================================================

prompt = ChatPromptTemplate.from_template(
"""
You are an AML & Fraud Detection Co-Pilot.

Conversation History:

{history}

====================================================

Relevant Examples:

{examples}

====================================================

Tool Output:

{tool_output}

====================================================

User Question:

{question}

====================================================

Instructions:

1. Explain suspicious activity.
2. Mention risk score.
3. Mention AML typology.
4. Mention sanctions matches.
5. Mention filing deadlines.
6. Recommend actions.
7. Use banking terminology.
8. Be concise and professional.

====================================================

Answer:
"""
)