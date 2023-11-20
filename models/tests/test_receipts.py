import unittest

from fetchApi.models.receipts import Receipt

TEST_RECEIPT_ONE = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
        },{
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
        },{
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
        },{
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
        },{
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
        }
    ],
    "total": "35.35"
}

TEST_RECEIPT_TWO = {
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

class TestSuite(unittest.IsolatedAsyncioTestCase):
    async def test_receipt_insertion(self):
        """
        Tests receipt insertion and retrieval. 
        """
        mockReceipt = get_mock_receipt(TEST_RECEIPT_ONE)
        receiptId = Receipt.postReceipt(receipt=mockReceipt.dict())
        assert len(receiptId) > 0, "postReceipt() should return a receiptId!"
        pointsEarned = Receipt.getReceipt(receiptId=receiptId)
        assert isinstance(pointsEarned, int) and pointsEarned > 0, "We should be able to fetch receipt points after posting"

    async def test_point_calculation(self):
        """
        Tests receipt point calculation.
        """
        mockReceiptOne = get_mock_receipt(TEST_RECEIPT_ONE)
        mockReceiptTwo = get_mock_receipt(TEST_RECEIPT_TWO)
        points = Receipt.calculate_points(receipt=mockReceiptOne.dict())
        assert points == 28, "Incorrect points calculation from receipt one."
        points = Receipt.calculate_points(receipt=mockReceiptTwo.dict())
        assert points == 109, "Incorrect points calculation from receipt two."
