from typing import Dict


REQUIRED_FIELDS = [
    "name",
    "version",
    "author",
    "model_compatibility",
    "changelog",
    "input_variables",
    "template"
]


def validate_prompt(data: Dict):

    missing = []

    for field in REQUIRED_FIELDS:

        if field not in data:
            missing.append(field)

    if missing:

        return {
            "valid": False,
            "missing_fields": missing
        }

    return {
        "valid": True,
        "missing_fields": []
    }


def validate_version(version: str):

    parts = version.split(".")

    if len(parts) != 3:
        return False

    return all(
        part.isdigit()
        for part in parts
    )


def validate_prompt_version(data: Dict):

    result = validate_prompt(data)

    if not result["valid"]:
        return result

    if not validate_version(
        data["version"]
    ):

        return {
            "valid": False,
            "error": "Invalid semantic version format"
        }

    return {
        "valid": True
    }