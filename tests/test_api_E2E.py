import random
import requests
import re

BASE_URL = "https://qa-internship.avito.com"


def test_e2e_create_and_get_item():
    seller_id = random.randint(111111, 999999)

    payload = {
        "sellerID": seller_id,
        "name": "Ручка",
        "price": 777,
        "statistics": {
            "likes": 10,
            "viewCount": 100,
            "contacts": 5
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

    response_json = create.json()
    status_text = response_json["status"]

    item_id = re.search(
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        status_text
    ).group()

    assert item_id is not None

    get = requests.get(
        f"{BASE_URL}/api/1/item/{item_id}",
        headers=headers
    )

    print("GET STATUS:", get.status_code)
    print("GET RESPONSE:", get.text)

    assert get.status_code == 200

    data = get.json()
    item = data[0] if isinstance(data, list) else data

    assert item["sellerId"] == seller_id
    assert item["name"] == payload["name"]
    assert item["price"] == payload["price"]
    assert item["statistics"]["likes"] == payload["statistics"]["likes"]
    assert item["statistics"]["viewCount"] == payload["statistics"]["viewCount"]
    assert item["statistics"]["contacts"] == payload["statistics"]["contacts"]

    delete = requests.delete(
        f"{BASE_URL}/api/2/item/{item_id}",
        headers=headers
    )

    print("DELETE STATUS:", delete.status_code)
    print("DELETE RESPONSE:", delete.text)

    assert delete.status_code in (200, 404)

    get = requests.get(
        f"{BASE_URL}/api/1/item/{item_id}",
        headers=headers
    )

    print("GET AFTER DELETE:", get.status_code)

    assert get.status_code in (404, 400)
