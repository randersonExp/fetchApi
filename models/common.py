import uuid
from typing import NewType

UUIDStr = NewType("UUIDStr", str)

def getUuid() -> uuid.UUID:
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    return random_uuid

def getUuidStr() -> UUIDStr:
    uuid = getUuid()
    return str(uuid)

