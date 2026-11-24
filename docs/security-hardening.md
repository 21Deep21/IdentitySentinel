
# Project 4 — Identity and Session Security Hardening Guide

## 1. Objective

Recommend preventive, detective, and corrective controls
for a fictional application using browser sessions,
JWT, OAuth 2.0, OpenID Connect, and protected APIs.

These recommendations are based on the threat model
and selected observations from the local WebGoat lab.

## 2. Session and Cookie Security

- [ ] Enforce HTTPS in production.
- [ ] Configure session cookies with Secure.
- [ ] Configure session cookies with HttpOnly.
- [ ] Select an appropriate SameSite policy.
- [ ] Regenerate session identifiers after authentication.
- [ ] Invalidate authenticated sessions on logout.
- [ ] Implement idle and absolute session timeouts.
- [ ] Avoid exposing session identifiers in URLs or logs.

## 3. JWT Security

- [ ] Verify JWT signatures with trusted keys.
- [ ] Enforce an explicit allowed-algorithm policy.
- [ ] Reject unexpected unsigned JWTs.
- [ ] Validate issuer (iss).
- [ ] Validate audience (aud).
- [ ] Validate expiration (exp).
- [ ] Validate not-before (nbf), where applicable.
- [ ] Validate token type and intended purpose.
- [ ] Reject malformed or oversized tokens.
- [ ] Never trust claims solely because they decode.

## 4. OAuth 2.0 and OpenID Connect

- [ ] Use Authorization Code Flow with PKCE.
- [ ] Register and validate exact redirect URIs.
- [ ] Validate state when used for CSRF protection.
- [ ] Validate OIDC nonce when applicable.
- [ ] Validate ID token signature, issuer and audience.
- [ ] Prevent authorization-code reuse.
- [ ] Use short-lived access tokens.
- [ ] Protect refresh tokens against disclosure.
- [ ] Do not use ID tokens as API access tokens.

## 5. Protected API Security

- [ ] Require authentication for protected endpoints.
- [ ] Enforce object-level authorization.
- [ ] Enforce function-level authorization.
- [ ] Apply least-privilege permissions.
- [ ] Validate access-token audience and scopes.
- [ ] Avoid exposing internal error details.
- [ ] Apply appropriate rate limiting.

## 6. Browser and Application Security

- [ ] Use context-aware output encoding.
- [ ] Avoid unsafe DOM operations.
- [ ] Configure Content Security Policy.
- [ ] Apply CSRF protection where needed.
- [ ] Validate input size and format.
- [ ] Avoid storing sensitive tokens in localStorage.
- [ ] Keep frameworks and dependencies updated.

## 7. Logging and Monitoring

- [ ] Log authentication successes and failures.
- [ ] Log authorization failures.
- [ ] Detect suspicious login activity.
- [ ] Monitor unusual token-validation failures.
- [ ] Redact credentials, tokens and session IDs.
- [ ] Restrict access to security logs.
- [ ] Define log retention and incident-response rules.

## 8. Before-and-After Remediation Matrix

The following are proposed improvements for the
fictional application, not changes implemented in WebGoat.

| Risk | Before: Insecure Design | After: Recommended Control | Verification |
|---|---|---|---|
| Session cookie exposure | Cookie lacks Secure on a production HTTPS service | Enforce HTTPS and Secure cookies | Inspect Set-Cookie over HTTPS |
| JWT validation weakness | API trusts decoded claims without signature verification | Verify signature, issuer, audience and expiration | Reject invalid synthetic test tokens in an authorized test environment |
| Broken API authorization | API checks login but not resource ownership | Enforce object-level access checks | Confirm users cannot access other users' resources |
| OAuth redirect misuse | Redirect URI accepted without strict matching | Require registered redirect URI matching and PKCE | Reject unregistered redirect URIs |
| Sensitive logging | Tokens recorded in plaintext logs | Redact sensitive fields and restrict log access | Review sanitized log samples |

## 9. Defense-in-Depth Strategy

### Prevention
TLS, secure cookies, PKCE, validated tokens,
least privilege, safe coding and input limits.

### Detection
Authentication monitoring, token-validation
failure alerts, API access logs and security reviews.

### Response
Session revocation, credential reset,
incident investigation, containment and recovery.

### Verification
Repeat controlled security tests after changes,
review configurations and confirm mitigations.

## 10. Project Limitations

- WebGoat is intentionally vulnerable.
- The proposed OAuth/OIDC application is fictional.
- No production application was modified.
- The JWT inspector performs offline claim inspection only.
- A passing claim inspection does not establish token authenticity.
