"""
Authentication and session configuration.

Implements SAML 2.0 federation with NIH's enterprise identity provider
and enforces session controls per NIST SP 800-53 AC-12 and IA-2.
"""

import os
from typing import List


class AuthConfig:
    # SAML 2.0 Identity Provider settings
    IDP_ENTITY_ID: str = os.environ.get("IDP_ENTITY_ID", "https://idp.nih.gov/saml2")
    IDP_SSO_URL: str = os.environ.get("IDP_SSO_URL", "https://idp.nih.gov/saml2/sso")
    IDP_X509_CERT: str = os.environ.get("IDP_X509_CERT", "")

    # Service Provider settings
    SP_ENTITY_ID: str = os.environ.get("SP_ENTITY_ID", "https://rdp.nhlbi.nih.gov")
    SP_ACS_URL: str = os.environ.get("SP_ACS_URL", "https://rdp.nhlbi.nih.gov/auth/saml/callback")

    # Session controls (AC-12: Session Termination)
    SESSION_TIMEOUT_MINUTES: int = int(os.environ.get("SESSION_TIMEOUT_MINUTES", "30"))
    MAX_CONCURRENT_SESSIONS: int = int(os.environ.get("MAX_CONCURRENT_SESSIONS", "1"))
    SESSION_LOCK_IDLE_MINUTES: int = int(os.environ.get("SESSION_LOCK_IDLE_MINUTES", "15"))

    # JWT settings
    JWT_ALGORITHM: str = "RS256"
    JWT_EXPIRY_SECONDS: int = 1800  # 30 minutes, matching session timeout
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "")

    # Allowed CORS origins (production values injected via environment)
    ALLOWED_ORIGINS: List[str] = os.environ.get(
        "ALLOWED_ORIGINS", "https://rdp.nhlbi.nih.gov"
    ).split(",")

    # Password policy (IA-5: Authenticator Management)
    PASSWORD_MIN_LENGTH: int = 15
    PASSWORD_COMPLEXITY_REQUIRED: bool = True
    PASSWORD_HISTORY_COUNT: int = 24
    PASSWORD_MAX_AGE_DAYS: int = 60

    # Account lockout (AC-7: Unsuccessful Logon Attempts)
    MAX_FAILED_ATTEMPTS: int = 3
    LOCKOUT_DURATION_MINUTES: int = 30
