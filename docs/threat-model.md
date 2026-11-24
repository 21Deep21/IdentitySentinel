
# Project 4 — Session and Token Security Threat Model

## 1. Scope

This threat model covers a fictional single-page
application using OAuth 2.0, OpenID Connect, JWTs,
an authorization server, and a protected API.

The OWASP WebGoat laboratory is used separately
for controlled security observations.

## 2. Protected Assets

- User credentials
- Session cookies
- Access tokens and ID tokens
- Protected API resources
- User identity information
- Authentication and security logs

## 3. Trust Boundaries

1. User browser to client application
2. Browser to authorization server
3. Client application to protected API
4. Token issuer to token validator
5. Authenticated user to restricted resources

## 4. Risk Assessment Method

Likelihood: 1 (Rare) to 5 (Very Likely)
Impact: 1 (Negligible) to 5 (Critical)

Risk Score = Likelihood x Impact

Low: 1-5
Medium: 6-12
High: 13-25

Ratings are illustrative and should be reassessed
using actual deployment and testing evidence.

## 5. Threat Register

| ID | Threat | Likelihood | Impact | Score | Risk |
|---|---|---:|---:|---:|---|
| T01 | Session hijacking | 4 | 5 | 20 | High |
| T02 | JWT signature validation failure | 3 | 5 | 15 | High |
| T03 | Expired token acceptance | 3 | 4 | 12 | Medium |
| T04 | Cross-Site Request Forgery (CSRF) | 3 | 4 | 12 | Medium |
| T05 | Cross-Site Scripting (XSS) | 4 | 4 | 16 | High |
| T06 | Broken API access control | 4 | 5 | 20 | High |
| T07 | OAuth redirect manipulation | 3 | 5 | 15 | High |
| T08 | Sensitive token exposure in logs | 3 | 4 | 12 | Medium |

## 6. Recommended Mitigations

### T01 — Session Hijacking
Use HTTPS, Secure and HttpOnly cookies,
appropriate SameSite settings, session rotation
after authentication, and server-side logout
invalidation.

### T02 — JWT Signature Validation Failure
Verify signatures using trusted keys.
Use an explicit algorithm allowlist.
Reject unsigned tokens where signatures are
required. Validate issuer and audience.

### T03 — Expired Token Acceptance
Validate exp and other required time claims
server-side. Reject expired tokens and use
appropriate token lifetimes.

### T04 — CSRF
Use CSRF tokens for state-changing requests
where applicable. Configure SameSite cookies
and verify Origin headers when appropriate.

### T05 — XSS
Use context-aware output encoding,
safe DOM APIs, input validation, and
Content Security Policy as defense in depth.

### T06 — Broken API Access Control
Enforce authorization server-side for
every protected API resource and operation.
Use least privilege and object-level checks.

### T07 — OAuth Redirect Manipulation
Require exact registered redirect URI matching,
PKCE, state validation, and strict
authorization-server configuration.

### T08 — Token Exposure in Logs
Redact tokens, cookies, and credentials.
Restrict log access and define retention rules.

## 7. Evidence Mapping

SEC-01: Session cookie attributes observed
using OWASP ZAP.

SEC-02: Post-logout redirect observed using
OWASP ZAP.

JWT-01: Expired synthetic JWT detected.

JWT-02: Missing JWT claims detected.

JWT-03: Unsafe 'none' algorithm declaration
flagged by the offline inspector.

JWT-04: Complete synthetic claims passed
basic inspection checks.

These observations do not establish that
WebGoat has all threats listed above.

## 8. Limitations

- No production application was tested.
- OAuth/OIDC architecture is conceptual.
- JWT inspector does not verify signatures.
- Risk scores are illustrative.
- No real access tokens or credentials are used.
- Scanner alerts require manual verification.
