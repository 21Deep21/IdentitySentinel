# Session, JWT, OAuth 2.0 and OpenID Connect Security Lab

**Course:** CSCS7016 — Application Security  
**Project:** Group Project 4  
**Environment:** Fedora Linux 44  
**Implementation:** Python 3.14, Docker, OWASP WebGoat, OWASP ZAP and Fiddler Everywhere

## 1. Project Overview

This project investigates web session security, JWT claim inspection, authentication controls, and secure identity architecture.

It combines controlled application-security observations using OWASP WebGoat, ZAP and Fiddler with an offline Python JWT inspector, a bounded-input demonstration, threat modeling, and security-hardening recommendations.

OAuth 2.0 and OpenID Connect are covered through a proposed identity architecture rather than a deployed identity provider.

## 2. Objectives

- Examine HTTP session cookies and authentication behavior.
- Inspect JWT headers and claims using synthetic tokens.
- Identify expired tokens, missing claims and unsafe algorithm declarations.
- Demonstrate safe input-length validation.
- Model OAuth 2.0 and OpenID Connect authentication flows.
- Develop a risk-ranked threat model and defense-in-depth recommendations.

## 3. Tools and Technologies

| Tool | Purpose |
|---|---|
| OWASP WebGoat | Local application-security training environment |
| OWASP ZAP 2.17.0 | HTTP inspection and session-security observations |
| Fiddler Everywhere 8.4.0 | Independent HTTP traffic inspection |
| Python 3.14 | JWT inspector and input-validation demonstration |
| Docker | Local WebGoat deployment |
| Git | Source control and reproducibility |

## 4. Laboratory Architecture

WebGoat runs locally through Docker at:

`http://127.0.0.1:8080/WebGoat`

OWASP ZAP was configured as an HTTP proxy on `127.0.0.1:8090`. A separate Chrome profile was used to inspect WebGoat traffic through ZAP.

Fiddler Everywhere's Clean Browser was used independently to capture WebGoat requests and responses.

The proposed OAuth/OIDC architecture is documented in [Authentication Flow](diagrams/authentication-flow.md).

## 5. Security Investigation

### SEC-01 — Session Cookie Attributes

ZAP captured a WebGoat response containing a `JSESSIONID` session cookie.

Observed attributes:

- `HttpOnly`: Present
- `Path`: `/WebGoat`
- `Secure`: Not explicitly present
- `SameSite`: Not explicitly present

These observations were made in a local HTTP training environment. They do not independently establish a production vulnerability.

Evidence: `evidence/zap-session-headers.png`

### SEC-02 — Post-Logout Authentication

After logout, revisiting `/WebGoat/` produced an HTTP 302 redirect to `/WebGoat/login`.

This demonstrates the observed post-logout navigation behavior but does not independently prove server-side session invalidation.

Evidence: `evidence/zap-logout-redirect.png`

### SEC-03 — Fiddler Traffic Inspection

Fiddler Everywhere captured the WebGoat login redirect and HTTP response headers, including the `Set-Cookie` header.

Evidence: `evidence/fiddler-session-headers.png`

## 6. Python JWT Inspector

The offline inspector decodes synthetic JWT headers and payloads and examines:

- `iss` — Issuer
- `aud` — Audience
- `sub` — Subject
- `iat` — Issued-at time
- `exp` — Expiration time
- `alg` — Declared algorithm

The inspector does not verify cryptographic signatures or establish token authenticity.

### Running the Inspector

```bash
python scripts/jwt_inspector.py "$(cat sample_data/expired_jwt.txt)"
```

### Verified Test Results

| Test case | Observed result |
|---|---|
| Expired JWT | Expiration warning |
| Missing claims | Missing `iss`, `aud`, and `exp` warnings |
| `none` algorithm | Unsafe algorithm declaration warning |
| Complete claims | No basic claim warnings |

Full output: [JWT Inspector Results](evidence/jwt-inspector-results.txt)

## 7. Input-Validation Demonstration

A separate Python script demonstrates token-length validation.

Run:

```bash
python scripts/input_validation.py
```

| Input | Length | Result |
|---|---:|---|
| Normal | 100 | Accepted |
| Empty | 0 | Rejected |
| Maximum boundary | 4096 | Accepted |
| Oversized | 5000 | Rejected |

Full output: [Input Validation Results](evidence/input-validation-results.txt)

This demonstrates input-size checking, not comprehensive memory safety.

## 8. Threat Modeling

The proposed identity architecture includes eight risk scenarios:

1. Session hijacking
2. JWT signature-validation failure
3. Expired-token acceptance
4. Cross-Site Request Forgery
5. Cross-Site Scripting
6. Broken API access control
7. OAuth redirect manipulation
8. Sensitive token exposure in logs

Risk scores use a 1–5 likelihood scale and a 1–5 impact scale.

See [Threat Model](docs/threat-model.md).

## 9. Security Hardening

Recommendations cover secure cookies, TLS, JWT verification, OAuth PKCE, OIDC validation, API authorization, logging, token storage, and defense in depth.

See [Security Hardening Guide](docs/security-hardening.md).

## 10. Project Structure

```text
application-security-project4/
├── diagrams/
│   └── authentication-flow.md
├── docs/
│   ├── security-hardening.md
│   └── threat-model.md
├── evidence/
│   ├── fiddler-session-headers.png
│   ├── input-validation-results.txt
│   ├── jwt-inspector-results.txt
│   ├── webgoat-http-response-sanitized.txt
│   ├── zap-logout-redirect.png
│   └── zap-session-headers.png
├── sample_data/
│   ├── expired_jwt.txt
│   ├── missing_claims_jwt.txt
│   ├── none_algorithm_jwt.txt
│   └── valid_claims_jwt.txt
├── scripts/
│   ├── input_validation.py
│   └── jwt_inspector.py
└── README.md
```

## 11. Ethical Scope

All application testing was performed against a local OWASP WebGoat training instance.

Only synthetic JWTs were used for offline analysis. No production identity providers, third-party applications, or real user accounts were tested.

## 12. Limitations

- JWT signatures are not cryptographically verified by the inspector.
- The OAuth/OIDC architecture is conceptual.
- No complete OAuth/OIDC authentication service was implemented.
- The WebGoat investigation covers selected security behaviors.
- Risk ratings are illustrative.
- The bounded-input script does not demonstrate native memory exploitation.
- Further testing is required to verify server-side session invalidation.

## 13. Conclusion

The project demonstrates practical session-security inspection, offline JWT claim analysis, input validation, and structured security risk assessment.

The results emphasize that secure identity systems require layered protection across authentication, token validation, authorization, browser security, logging, and monitoring.