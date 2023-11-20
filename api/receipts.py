"""
This file contains all routes related to processing receipts.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from fetchApi.models.receipts import Receipt
from fetchApi.models.common import UUIDStr

receiptsRouter = APIRouter(prefix="/receipts", tags=["receipts"])

class GetPointsResponse(BaseModel):
    # Note: Python 3's ints are "unlimited" in size, so this satisfies the 64 bit requirement. 
    # However, we could always put an additional validator, (or custom typing), around this if desired.
    points: int # Ex: 100

class PostReceiptsResponse(BaseModel):
    id: UUIDStr

@receiptsRouter.get("/{id}/points")
async def getPoints(id: UUIDStr) -> GetPointsResponse:
    """
    Fetches points for a given receipt id.

    TODO: Add authentication.
    TODO: If this API is customer-facing, then we should NOT return a response if the receipt id is tied to another 
    user's account.
    TODO: if 'id' is a string like, "adb6b560-0eef-42bc-9d16-df48f30e89b2", then we can probably do a pattern match
    on this value to detect invalid ids.
    """
    points = Receipt.getReceipt(receiptId=id)
    # Handle the "not found" case here.
    if points is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No receipt found for that id"
        )
    return GetPointsResponse(points=points)
    
@receiptsRouter.post("/process")
async def getPoints(receiptRaw: dict) -> PostReceiptsResponse:
    """
    Submits a receipt for processing

    TODO: Add authentication.
    TODO: If this API is customer-facing, then we should NOT return a response if the receipt id is tied to another 
    user's account.
    """
    try:
        receipt = Receipt(**receiptRaw)
    except Exception as e:
        # TODO - in a prod env we would log the specific error here for debugging purposes.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The receipt is invalid"
        )
    receiptUUID = Receipt.postReceipt(receipt=receipt.dict())
    return PostReceiptsResponse(id=receiptUUID)
