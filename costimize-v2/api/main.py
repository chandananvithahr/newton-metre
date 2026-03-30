"""FastAPI app -- thin wrapper around existing Python cost engines."""
import os
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api.routes import assembly, extract, estimate, material, similarity, estimates, usage, rfq

logger = logging.getLogger("costimize")
logging.basicConfig(level=logging.INFO)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Costimize API",
    description="Should-cost intelligence for mechanical parts",
    version="1.0.0",
    docs_url=None if os.getenv("ENVIRONMENT") == "production" else "/docs",
    redoc_url=None,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

_DEFAULT_ORIGINS = "https://frontend-theta-ecru-95.vercel.app"
if os.getenv("ENVIRONMENT") != "production":
    _DEFAULT_ORIGINS = "http://localhost:3000," + _DEFAULT_ORIGINS

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", _DEFAULT_ORIGINS).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all: log real error server-side, return generic message to client."""
    logger.error("Unhandled error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again."},
    )


app.include_router(extract.router, prefix="/api")
app.include_router(assembly.router, prefix="/api")
app.include_router(estimate.router, prefix="/api")
app.include_router(material.router, prefix="/api")
app.include_router(similarity.router, prefix="/api")
app.include_router(estimates.router, prefix="/api")
app.include_router(usage.router, prefix="/api")
app.include_router(rfq.router, prefix="/api")


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
