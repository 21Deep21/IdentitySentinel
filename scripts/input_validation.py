"""Safe bounded-input demonstration for Project 4."""

MAX_TOKEN_LENGTH = 4096


def validate_token_length(token):
    """Reject oversized token strings before processing."""
    if not isinstance(token, str):
        return False, "Input must be a string"

    if not token:
        return False, "Empty token rejected"

    if len(token) > MAX_TOKEN_LENGTH:
        return False, "Token exceeds maximum permitted length"

    return True, "Token length accepted"


if __name__ == "__main__":
    test_cases = {
        "Normal input": "A" * 100,
        "Empty input": "",
        "Maximum boundary": "A" * 4096,
        "Oversized input": "A" * 5000,
    }

    for name, token in test_cases.items():
        accepted, message = validate_token_length(token)

        print(f"{name}:")
        print(f"  Length: {len(token)}")
        print(f"  Accepted: {accepted}")
        print(f"  Result: {message}\n")
