from fastapi import APIRouter, FastAPI, Response, status, HTTPException

from fetchApi.api.receipts import receiptsRouter

# Initialize API router
apiRouter = APIRouter()

# application instance
app = FastAPI(
    title="Fetch Receipts API",
    description="Backend for receipt processing.",
)

# Register all routers here
apiRouter.include_router(receiptsRouter)

# Inform the application about our fancy routes
app.include_router(apiRouter)

# Basic liveliness check
@app.get("/")
def root():
    message = "Liveliness check passed!!"
    return { "message": f"{message}" }
