"""
This file contains the models and corresponding business logic for processing and fetching receipts.
"""
import asyncio
from pydantic import BaseModel, validator
from typing import List, Union
from datetime import datetime
import math

from fetchApi.models.common import getUuidStr, UUIDStr, validate_custom_regex, validate_float_total

# An in-memory key-value store to simulate a database. Note: We would not do this in a prod-ready app :)
pointsDatabase = dict()

class Item(BaseModel):
  shortDescription: str # pattern: ^[\w\s\-]+$
  price: str # Ex: "6.49", should follow pattern: ^\d+\.\d{2}$

  @validator('price')
  def validate_total(cls, v):
    validate_float_total(v)
    return v
  
  @validator('shortDescription')
  def validate_description(cls, v):
    validate_custom_regex("^[\w\s\-]+$", v)
    return v

class Receipt(BaseModel):
    """
    Example Data:
    {
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

    This should generate 28 points.
    """
    retailer: str
    purchaseDate: str # Should be a date YYYY-MM-DD like so: "2022-01-01"
    purchaseTime: str # should be time lie HH:MM ex: "13:01"
    items: List[Item]
    total: str # Ex: "6.49", should follow pattern: ^\d+\.\d{2}$

    @validator('retailer')
    def validate_retailer_name(cls, v):
      if not v or not v.strip() or v[0].isspace():  # Check if the string is empty or starts with whitespace
          raise ValueError('Invalid retailer name')
      return v

    @validator('purchaseDate')
    def validate_date_format(cls, v):
      try:
          datetime.strptime(v, '%Y-%m-%d')
      except ValueError:
          raise ValueError('Incorrect date format, should be YYYY-MM-DD')
      return v

    @validator('purchaseTime')
    def validate_date_format(cls, v):
      try:
        datetime.strptime(v, '%H:%M')
      except ValueError:
        raise ValueError('Incorrect time format, should be HH:MM')
      return v    
    
    @validator('total')
    def validate_total(cls, v):
      validate_float_total(v)
      return v
  
    @classmethod
    def calculate_points(self, receipt: 'Receipt') -> int:
        """
        TODO: write unit tests around this.
        This function calculates the number of points that should be rewarded to a given receipt and returns the
        value as an integer
        
        These rules collectively define how many points should be awarded to a receipt.
        - One point for every alphanumeric character in the retailer name.
        - 50 points if the total is a round dollar amount with no cents.
        - 25 points if the total is a multiple of 0.25.
        - 5 points for every two items on the receipt.
        - If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up 
          to the nearest integer. The result is the number of points earned.
        - 6 points if the day in the purchase date is odd.
        - 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        """
        def is_round(number: float) -> bool:
            """
            Computes whether or not a floating point number is round. 
            TODO: For easy reuse, we might want to break this out into a shared utils file.
            """
            return number == int(number)
        
        # convert obj to dict for easy processing.
        points = 0

        # Rule 1: One point for every alphanumeric character in the retailer name.
        points += sum(c.isalnum() for c in receipt['retailer'])

        # Rule 2: 50 points if the total is a round dollar amount with no cents.
        total = float(receipt['total'])
        if is_round(total):
            points += 50

        # Rule 3: 25 points if the total is a multiple of 0.25.
        if total % 0.25 == 0:
            points += 25

        # Rule 4: 5 points for every two items on the receipt.
        points += len(receipt['items']) // 2 * 5

        # Rule 5: If the trimmed length of the item description is a multiple of 3,
        # multiply the price by 0.2 and round up to the nearest integer.
        for item in receipt['items']:
            trimmed_length = len(item['shortDescription'].strip())
            if trimmed_length % 3 == 0:
                price = float(item['price'])
                points += math.ceil(price * 0.2) # Round up to nearest integer. Note: math.ceil returns an int.

        # Rule 6: 6 points if the day in the purchase date is odd.
        purchase_date = datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
        if purchase_date.day % 2 != 0:
            points += 6

        # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        purchase_time = datetime.strptime(receipt['purchaseTime'], '%H:%M').time()
        if datetime.strptime('14:00', '%H:%M').time() < purchase_time < datetime.strptime('16:00', '%H:%M').time():
            points += 10

        return points

    @classmethod
    async def postReceipt(self, receipt: 'Receipt') -> UUIDStr:
        """
        Helper function for calculating and storing the points associated with a single receipt.
        After processing, this function returns a unique id.
        """
        await asyncio.sleep(.4) # sleeping to simulate the time it takes to write to a db
        points = self.calculate_points(receipt=receipt)
        receiptId = getUuidStr()
        # TODO: In a real-world app, we would probably save the receipt's metadata. For this exercise, I
        # will just save the points.
        pointsDatabase[receiptId] = points
        return receiptId
    
    @staticmethod
    async def getReceipt(receiptId: UUIDStr) -> Union[int, None]:
        """
        fetches a single receipt's points by receipt ID (a UUID4). We return None if the receipt DNE.
        """
        await asyncio.sleep(.3) # sleeping to simulate the time it takes to read from a db
        return pointsDatabase.get(receiptId)
