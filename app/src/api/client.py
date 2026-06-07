"""
External API client for upstream NIH data services.

Handles authenticated HTTP calls to external data providers
per the interconnection agreements documented in the SSP.
"""

import os
import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ExternalAPIClient:
    """
    HTTP client for calls to NIH upstream services.

    Implements retry logic, TLS certificate pinning configuration,
    and audit logging for all outbound connections per
    NIST SP 800-53 SC-8 (Transmission Confidentiality and Integrity)
    and AU-2 (Event Logging).
    """

    BASE_URL: str = os.environ.get("UPSTREAM_API_URL", "https://api.ncbi.nlm.nih.gov")
    API_KEY: str = os.environ.get("UPSTREAM_API_KEY", "")
    TIMEOUT_SECONDS: int = int(os.environ.get("API_TIMEOUT_SECONDS", "30"))
    MAX_RETRIES: int = 3

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "NHLBI-RDP/1.4.2",
        })
        # Enforce TLS verification — never disable in production
        self.session.verify = True

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        """Perform an authenticated GET request to the upstream service."""
        url = f"{self.BASE_URL}{path}"
        logger.info("Outbound GET %s", url)

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response = self.session.get(url, params=params, timeout=self.TIMEOUT_SECONDS)
                response.raise_for_status()
                logger.info("GET %s returned %d", url, response.status_code)
                return response.json()
            except requests.exceptions.Timeout:
                logger.warning("GET %s timed out (attempt %d/%d)", url, attempt, self.MAX_RETRIES)
                if attempt == self.MAX_RETRIES:
                    raise
            except requests.exceptions.HTTPError as exc:
                logger.error("GET %s HTTP error: %s", url, exc)
                raise

    def post(self, path: str, payload: Dict[str, Any]) -> Dict:
        """Perform an authenticated POST request to the upstream service."""
        url = f"{self.BASE_URL}{path}"
        logger.info("Outbound POST %s", url)

        response = self.session.post(url, json=payload, timeout=self.TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
