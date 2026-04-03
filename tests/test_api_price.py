import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def test_negative_price_should_return_400():
    seller_id = random.randint(111111, 999999)

    payload = {
        "sellerID": seller_id,
        "name": "negative price test",
        "price": -100,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(
        f"{BASE_URL}/api/1/item",
        json=payload,
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 400, response.text
