import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def test_get_items_by_seller_id_and_validate_consistency():
    seller_id = random.randint(111111, 999999)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload_1 = {
        "sellerID": seller_id,
        "name": "Ручка",
        "price": 100,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        }
    }

    payload_2 = {
        "sellerID": seller_id,
        "name": "Ручка",
        "price": 200,
        "statistics": {
            "likes": 2,
            "viewCount": 2,
            "contacts": 2
        }
    }

    r1 = requests.post(f"{BASE_URL}/api/1/item", json=payload_1, headers=headers)
    assert r1.status_code == 200

    r2 = requests.post(f"{BASE_URL}/api/1/item", json=payload_2, headers=headers)
    assert r2.status_code == 200

    response = requests.get(
        f"{BASE_URL}/api/1/{seller_id}/item",
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        assert item["sellerId"] == seller_id, "Найден чужой sellerId"
        assert item["name"] is not None, "name пустой"
        assert item["name"] != "", "name пустая строка"