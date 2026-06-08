"""
NIH AI Analysis Service client.

Integrates with the NIH Office of Research Infrastructure's
AI Analysis API to provide ML-assisted dataset summarization
and anomaly detection for clinical research data.

New interconnection — requires ISA update per CA-3.
Outbound traffic on port 443 to api.ai.nih.gov per SC-7.
"""

import os
import logging
import httpx
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NIH_AI_API_URL: str = os.environ.get("NIH_AI_API_URL", "https://api.ai.nih.gov/v1")
NIH_AI_API_KEY: str = os.environ.get("NIH_AI_API_KEY", "")


class NIHAIClient:
    """
    Async client for the NIH AI Analysis Service.

    All requests are authenticated via API key (SI-3 compliant).
    Data submitted for analysis is de-identified per PIA requirements.
    """

    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=NIH_AI_API_URL,
            headers={
                "Authorization": f"Bearer {NIH_AI_API_KEY}",
                "Content-Type": "application/json",
                "X-Client-Id": "nhlbi-rdp",
            },
            timeout=60.0,
            verify=True,
        )

    async def summarize_dataset(self, dataset_id: str, fields: List[str]) -> Dict[str, Any]:
        """
        Request an AI-generated summary of a dataset's statistical profile.
        Only de-identified aggregate statistics are transmitted (no PII).
        """
        payload = {"dataset_id": dataset_id, "fields": fields, "mode": "aggregate_only"}
        logger.info("AI summarize request for dataset %s", dataset_id)
        response = await self._client.post("/summarize", json=payload)
        response.raise_for_status()
        return response.json()

    async def flag_anomalies(self, dataset_id: str, threshold: float = 0.95) -> Dict[str, Any]:
        """Request anomaly detection on a dataset's aggregate distribution."""
        payload = {"dataset_id": dataset_id, "confidence_threshold": threshold}
        response = await self._client.post("/anomalies", json=payload)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self._client.aclose()
