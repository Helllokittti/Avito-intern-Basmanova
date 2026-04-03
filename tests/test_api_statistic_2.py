import requests
import random
import re

BASE_URL = "https://qa-internship.avito.com"


def test_get_statistics_success():
    seller_id = random.randint(111111, 999999)

    payload = {
        "sellerID": seller_id,
        "name": "test item",
        "price": 100,
        "statistics": {
            "likes": 5,
            "viewCount": 5,
            "contacts": 10
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

    assert create.status_code == 200

    item_id = re.search(
        r"[0-9a-fA-F-]{36}",
        create.json()["status"]
    ).group()

    assert item_id

    response = requests.get(
        f"{BASE_URL}/api/2/statistic/{item_id}",
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

    stats = data[0]

    assert stats["contacts"] == 10
    assert stats["likes"] == 5
    assert stats["viewCount"] == 5

    assert isinstance(stats["contacts"], int)
    assert isinstance(stats["likes"], int)
    assert isinstance(stats["viewCount"], int)

def test_get_statistics_not_found():
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = requests.get(
        f"{BASE_URL}/api/2/statistic/{fake_id}",
        headers={"Accept": "application/json"}
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 404
