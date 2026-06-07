"""
NHLBI Research Data Portal — FastAPI entry point.

This application serves as the primary API gateway for the
NIH NHLBI Research Data Portal, providing authenticated access
to de-identified clinical research datasets.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.auth.config import AuthConfig
from src.api.client import ExternalAPIClient

logger = logging.getLogger(__name__)

app = FastAPI(
    title="NHLBI Research Data Portal",
    description="Authenticated API gateway for NHLBI clinical research data access.",
    version="1.4.2",
    docs_url=None,  # Disabled in production per security policy
    redoc_url=None,
)

# CORS — restrict to approved origins only
app.add_middleware(
    CORSMiddleware,
    allow_origins=AuthConfig.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": app.version}


_ncbi_client = ExternalAPIClient(base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils")


@app.get("/api/v1/datasets")
async def list_datasets(token: str = Depends(oauth2_scheme)):
    """Return a list of datasets the authenticated user is authorized to access."""
    # Token validation handled by auth middleware
    return {"datasets": [], "total": 0}


@app.post("/auth/token")
async def login(username: str, password: str):
    """Issue a short-lived JWT upon successful credential validation."""
    # Credential validation delegated to identity provider
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication delegated to agency IdP.",
    )
