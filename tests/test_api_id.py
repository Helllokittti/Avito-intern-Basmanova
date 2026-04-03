import re
import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def test_e2e_create_and_get():
    seller_id = random.randint(111111, 999999)

    payload = {
        "sellerID": seller_id,
        "name": "auto test",
        "price": 100,
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

    create = requests.post(
        f"{BASE_URL}/api/1/item",
        json=payload,
        headers=headers
    )

    print("CREATE STATUS:", create.status_code)
    print("CREATE RESPONSE:", create.text)

    assert create.status_code == 200

    data = create.json()

    match = re.search(r"([0-9a-fA-F-]{36})", data["status"])
    assert match is not None, "UUID не найден в ответе"

    item_id = match.group(1)

    get = requests.get(
        f"{BASE_URL}/api/1/item/{item_id}",
        headers=headers
    )

    print("GET STATUS:", get.status_code)
    print("GET RESPONSE:", get.text)

    assert get.status_code == 200
