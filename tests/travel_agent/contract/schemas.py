FLIGHT_SCHEMA = {
    "type": "array",
    "minItems": 3,
    "items": {
        "type": "object",
        "required": [
            "carrier",
            "flight",
            "route",
            "depart",
            "return",
            "price",
            "currency",
        ],
        "properties": {
            "carrier": {"type": "string"},
            "flight": {"type": "string"},
            "route": {"type": "string"},
            "depart": {"type": "string"},
            "return": {"type": "string"},
            "price": {"type": "number"},
            "currency": {"type": "string"},
        },
        "additionalProperties": True,
    },
}

HOTEL_SCHEMA = {
    "type": "array",
    "minItems": 3,
    "items": {
        "type": "object",
        "required": [
            "name",
            "city",
            "checkout",
            "price_per_night",
            "currency",
        ],
        "properties": {
            "name": {"type": "string"},
            "city": {"type": "string"},
            "checkout": {"type": "string"},
            "price_per_night": {"type": "number"},
            "currency": {"type": "string"},
        },
        "additionalProperties": True,
    },
}
