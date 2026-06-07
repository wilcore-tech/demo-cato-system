"""
Stripe payment integration client.

Handles data access subscription billing for external researchers
who require enhanced dataset access tiers. Introduces a new
external data flow to Stripe's API (api.stripe.com).

SECURITY NOTE: This module introduces an external data flow not
previously authorized in the SSP. A Security Impact Analysis (SIA)
is required before deployment per the Configuration Management Plan.
Relevant controls: SC-8 (new external connection), AC-4 (information
flow enforcement), SR-2/SR-3 (new third-party dependency).
"""

import os
import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

STRIPE_API_BASE = "https://api.stripe.com/v1"
STRIPE_API_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")


class StripeClient:
    """
    HTTP client for Stripe payment API.

    All calls go to api.stripe.com over HTTPS (TLS 1.2+).
    API key stored in AWS Secrets Manager; injected via environment variable.
    """

    def __init__(self):
        if not STRIPE_API_KEY:
            raise ValueError("STRIPE_SECRET_KEY environment variable is not set.")
        self.session = requests.Session()
        self.session.auth = (STRIPE_API_KEY, "")
        self.session.headers.update({
            "Stripe-Version": "2023-10-16",
            "User-Agent": "NHLBI-RDP/1.5.0 StripeClient",
        })
        self.session.verify = True  # Always verify TLS

    def create_customer(self, email: str, researcher_id: str) -> Dict[str, Any]:
        """Create a Stripe customer for a new subscription."""
        logger.info("Creating Stripe customer for researcher %s", researcher_id)
        response = self.session.post(
            f"{STRIPE_API_BASE}/customers",
            data={
                "email": email,
                "metadata[researcher_id]": researcher_id,
            },
        )
        response.raise_for_status()
        return response.json()

    def create_subscription(
        self, customer_id: str, price_id: str
    ) -> Dict[str, Any]:
        """Subscribe a customer to a data access tier."""
        logger.info("Creating subscription for customer %s, price %s", customer_id, price_id)
        response = self.session.post(
            f"{STRIPE_API_BASE}/subscriptions",
            data={
                "customer": customer_id,
                "items[0][price]": price_id,
            },
        )
        response.raise_for_status()
        return response.json()

    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel an active subscription (e.g., on account termination)."""
        logger.info("Canceling subscription %s", subscription_id)
        response = self.session.delete(
            f"{STRIPE_API_BASE}/subscriptions/{subscription_id}"
        )
        response.raise_for_status()
        return response.json()

    def verify_webhook(self, payload: bytes, sig_header: str) -> Dict[str, Any]:
        """
        Verify and parse an inbound Stripe webhook event.
        Uses HMAC-SHA256 signature verification.
        """
        import hmac
        import hashlib

        if not STRIPE_WEBHOOK_SECRET:
            raise ValueError("STRIPE_WEBHOOK_SECRET is not configured.")

        timestamp, signatures = self._parse_stripe_sig_header(sig_header)
        signed_payload = f"{timestamp}.{payload.decode('utf-8')}"
        expected_sig = hmac.new(
            STRIPE_WEBHOOK_SECRET.encode(),
            signed_payload.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not any(hmac.compare_digest(expected_sig, sig) for sig in signatures):
            raise ValueError("Webhook signature verification failed.")

        return {"verified": True, "timestamp": timestamp}

    @staticmethod
    def _parse_stripe_sig_header(header: str):
        parts = dict(item.split("=", 1) for item in header.split(","))
        timestamp = parts.get("t", "")
        sigs = [v for k, v in parts.items() if k == "v1"]
        return timestamp, sigs
