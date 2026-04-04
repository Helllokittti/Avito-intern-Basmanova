import re
import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def test_delete_item_v2():
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

    assert create.status_code == 200, f"CREATE FAILED: {create.text}"

    data = create.json()

    item_id = re.search(
        r"[0-9a-fA-F-]{36}",
        data["status"]
    ).group()

    print("ITEM ID:", item_id)

## позитивный сценарий удаления существующего объявления

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

## негативный сценарий удаления несуществующего объявления
    delete = requests.delete(
        f"{BASE_URL}/api/2/item/{item_id}",
        headers=headers
    )

    print("DELETE STATUS:", delete.status_code)
    print("DELETE RESPONSE:", delete.text)

    assert delete.status_code == 404

## негативный сценарий удаления некорректного айди объявления

    delete = requests.delete(
        f"{BASE_URL}/api/2/item/aaabbb",
        headers=headers
    )

    print("DELETE STATUS:", delete.status_code)
    print("DELETE RESPONSE:", delete.text)

    assert delete.status_code == 400
