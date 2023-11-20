"""
Unittests for receipts API routes.
"""
import unittest
from datetime import datetime

from httpx import AsyncClient

from fetchApi.models.receipts import Receipt
from fetchApi.api.main import createApp

TEST_RECEIPT_ONE = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {
            "shortDescription": "Gatorade",
            "price": "2.25"
        },{
            "shortDescription": "Gatorade",
            "price": "2.25"
        },{
            "shortDescription": "Gatorade",
            "price": "2.25"
        },{
            "shortDescription": "Gatorade",
            "price": "2.25"
        }
    ],
    "total": "9.00"
}

def get_mock_receipt(mockReceipt: dict) -> Receipt:
    cpy = mockReceipt.copy()
    return Receipt(**cpy)

class ReceiptAPITestSuite(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.app = createApp()
    
    async def test_post_receipt(self):
        """Tests the POST request where we add a receipt for processing."""
        async with AsyncClient(app=self.app, base_url="http://testserver") as client:
            receipt = get_mock_receipt(mockReceipt=TEST_RECEIPT_ONE) # A "proper" receipt format
            newReceiptData = receipt.dict()
            # Post the receipt
            response = await client.post("/receipts/process", json=newReceiptData)
            assert response.status_code == 200
            res = response.json()

            # Check that the response is formatted correctly.
            receiptId = res['id']
            assert receiptId and len(receiptId) > 0, "should return receipt id"
            
            # Now we should also be able to retrieve points for this receipt!
            getPointsResponse = await client.get(f"/receipts/{receiptId}/points")
            assert getPointsResponse.status_code == 200
            res = getPointsResponse.json()
            assert isinstance(res["points"], int)

    async def test_post_receipt_malformed(self):
        """Tests the POST request where we try to add a malformed receipt for processing."""
        async with AsyncClient(app=self.app, base_url="http://testserver") as client:
            receipt = get_mock_receipt(mockReceipt=TEST_RECEIPT_ONE) # A "proper" receipt format
            newReceiptData = receipt.dict()
            # Remove a required key -- this should cause problems!
            newReceiptData.pop("total")
            # Post the receipt
            response = await client.post("/receipts/process", json=newReceiptData)
            assert response.status_code == 400, "Malformed data -- test should fail!"

    async def test_get_points_when_dne(self):
        """Test getting a receipt that DNE"""
        async with AsyncClient(app=self.app, base_url="http://testserver") as client:
            badReceiptId = "foobar"
            # Now we should get an error since the id is fake
            getPointsResponse = await client.get(f"/receipts/{badReceiptId}/points")
            assert getPointsResponse.status_code == 404, "We should return a 404 if the receipt DNE."
