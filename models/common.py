import uuid, re
from typing import NewType

UUIDStr = NewType("UUIDStr", str)

def getUuid() -> uuid.UUID:
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    return random_uuid

def getUuidStr() -> UUIDStr:
    uuid = getUuid()
    return str(uuid)

def non_whitespace_validator(value):
    if not value or not value.strip():
        raise ValueError('Field must contain at least one non-whitespace character')
    return value

def validate_custom_regex(regexStr: str, v: str):
    regex_pattern = rf'{regexStr}'  # Replace this with your custom regex pattern
    if not re.match(regex_pattern, v):
        raise ValueError(f'Value "{v}" does not match the custom regex pattern "{regexStr}"')
    return v

def validate_float_total(total: str):
    validate_custom_regex("^\d+\.\d{2}$", total)
