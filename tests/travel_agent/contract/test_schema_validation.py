import jsonschema

from tests.travel_agent.contract.schemas import FLIGHT_SCHEMA, HOTEL_SCHEMA


def test_flight_schema_accepts_sample():
    sample = [
        {
            "carrier": "United",
            "flight": "UA100",
            "route": "SFO -> LAX",
            "depart": "2025-01-10",
            "return": "2025-01-12",
            "price": 120.5,
            "currency": "EUR",
        }
    ] * 3
    jsonschema.validate(sample, FLIGHT_SCHEMA)


def test_hotel_schema_accepts_sample():
    sample = [
        {
            "name": "Hotel SFO",
            "city": "San Francisco",
            "checkout": "2025-01-11",
            "price_per_night": 145.0,
            "currency": "EUR",
        }
    ] * 3
    jsonschema.validate(sample, HOTEL_SCHEMA)
