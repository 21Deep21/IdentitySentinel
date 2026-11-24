
import base64
import json
import sys
from datetime import datetime, timezone


def decode_part(part):
    """Decode a Base64URL-encoded JWT section."""
    try:
        padded = part + "=" * (-len(part) % 4)
        data = base64.urlsafe_b64decode(padded)
        result = json.loads(data)
        if not isinstance(result, dict):
            raise ValueError("JWT section must be a JSON object")
        return result
    except (ValueError, UnicodeDecodeError, base64.binascii.Error) as error:
        raise ValueError(f"Invalid JWT section: {error}")


def inspect_jwt(token):
    """Inspect synthetic JWT claims without verifying signatures."""
    parts = token.strip().split(".")

    if len(parts) != 3:
        raise ValueError("JWT must contain three sections")

    header = decode_part(parts[0])
    payload = decode_part(parts[1])

    print("\n=== JWT SECURITY INSPECTION ===")
    print("\nHeader:")
    print(json.dumps(header, indent=2))

    print("\nClaims:")
    for claim in ("iss", "aud", "sub", "iat", "exp"):
        print(f"  {claim}: {payload.get(claim, 'MISSING')}")

    warnings = []

    if header.get("alg") == "none":
        warnings.append("Unsafe algorithm declaration: none")
    elif "alg" not in header:
        warnings.append("Missing algorithm declaration")

    for claim in ("iss", "aud", "sub", "exp"):
        if not payload.get(claim):
            warnings.append(f"Missing or empty claim: {claim}")

    now = datetime.now(timezone.utc).timestamp()
    exp = payload.get("exp")

    if isinstance(exp, bool) or not isinstance(exp, (int, float)):
        if exp is not None:
            warnings.append("Invalid expiration claim type")
    elif exp <= now:
        warnings.append("Token has expired")

    print("\nSecurity observations:")
    if warnings:
        for warning in warnings:
            print(f"  [WARNING] {warning}")
    else:
        print("  No issues detected by basic claim checks")

    print("\nIMPORTANT: Signature NOT verified.")
    print("Decoded claims must NOT be trusted for authentication.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/jwt_inspector.py <synthetic-jwt>")
        sys.exit(1)

    try:
        inspect_jwt(sys.argv[1])
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)
