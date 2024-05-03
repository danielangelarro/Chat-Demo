import asyncio
import logging
import json

from demo_chat.application.services import WebSocketServices
from demo_chat.presentation.entry import websocket_endpoint


def lambda_handler(event, context):  
    domain = event.get("requestContext", {}).get("domainName")
    stage = event.get("requestContext", {}).get("stage")
    body = json.loads(event["body"]) if "body" in event else {}
    
    return asyncio.run(websocket_endpoint(
        routeKey=body["action"] if "action" in body else event["requestContext"]["routeKey"],
        context=event["requestContext"],
        payload=body,
        wss_url=f"https://{domain}/{stage}"
    ))