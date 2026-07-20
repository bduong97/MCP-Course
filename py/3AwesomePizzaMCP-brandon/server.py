import base64

import requests
from mcp.server.fastmcp import FastMCP
from typing import List
from mcp.types import CallToolResult, ImageContent, TextContent
from api_client import OrderItem
mcp = FastMCP("Awesome pizza MCP")


@mcp.tool(name="test_tool", description="Test tool description")
def say_hello() -> str:
    return "Hello from MCP!"


@mcp.tool(name="get_pizza_menu_with_images", description="Get the daily pizza menu")
def get_pizza_menu_with_images() -> CallToolResult:
    from api_client import get_daily_menu

    menu = get_daily_menu()
    content = []
    for item in menu:
        content.append(TextContent(type="text", text=item["name"]))
        content.append(TextContent(type="text", text=item["description"]))
        image_url = f"http://localhost:3000/{item['imageUrl']}"
        image_response = requests.get(image_url)

        img_data = base64.b64encode(image_response.content).decode("utf-8")
        content.append(ImageContent(type="image", data=img_data, mimeType="image/png"))
    return CallToolResult(content=content)

@mcp.tool(name="make_order", description="Make an order at awesome pizza; Returns an order ID")
def make_order(items: List[OrderItem]) -> str:
    from api_client import make_order
    order_response = make_order({
        "sender": "MCP user",
        "contents": items
    })
    return  order_response['order_id']

@mcp.tool(name="check_order_status", description="Check the status of an order by its id")
def check_order_status(order_id: str) -> str:
    from api_client import check_order_status
    order_status = check_order_status(order_id)
    return order_status

@mcp.tool(name="cancel_order", description="Cancels an order; Needs the order ID")
def cancel_order(order_id: str) -> str:
    from api_client import cancel_order
    order_status = cancel_order(order_id)
    return order_status