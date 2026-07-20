import requests

BASE_URL = "http://localhost:3000/api"


def get_daily_menu():
    try:
        resp = requests.get(
            f"{BASE_URL}/daily-menu",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": str(e), "data": []}
    except Exception as error:
        return {
            "success": False,
            "message": f"Unknown error occured: {str(error)}",
            "data": [],
        }

