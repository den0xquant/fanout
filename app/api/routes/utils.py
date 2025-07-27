from fastapi import APIRouter


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check", summary="Health Check Endpoint")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    Returns a simple message indicating the service is healthy.
    """
    return {"status": "healthy", "message": "Service is running smoothly."}
