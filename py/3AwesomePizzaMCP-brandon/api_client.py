import requests
from typing import TypedDict, List
BASE_URL = "http://localhost:3000/api"


def get_daily_menu():
    try:
        resp = requests.get(
            f"{BASE_URL}/daily-menu",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        resp.raise_for_status()
        menu = resp.json()['data']
        return menu
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": str(e), "data": []}
    except Exception as error:
        return {
            "success": False,
            "message": f"Unknown error occured: {str(error)}",
            "data": [],
        }

class OrderItem (TypedDict):
    '''
    Type definition for order item
    '''
    name: str
    quantity: int

class OrderDetails(TypedDict):
    sender: str
    contents: List[OrderItem]

def make_order(order_details: OrderDetails) -> dict:
    try:
        response = requests.post(
            f"{BASE_URL}/orders",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json=order_details
        )
        response.raise_for_status()
        response_json = response.json()
        return {
            'order_id': response_json['data']['id']
        }
    except Exception as error:
        return {
            'success': False,
            'message': f'Unknown error occured: {str(error)}',
            'order_id': ''
        }

def check_order_status(order_id: str) -> str:
    try:
        response = requests.get(
            f"{BASE_URL}/orders/{order_id}",
            headers={"Accept": "application/json", "Content-Type": "application/json"}
        )
        response.raise_for_status()
        response_json = response.json()
        if response_json.get('success'):
            return response_json['data']['status']
        else:
            return response_json.get('message', 'Unknown error')
    except requests.exceptions.RequestException as error:
        return str(error)
    except Exception as error:
        return f"Unknown error occured: {str(error)}"