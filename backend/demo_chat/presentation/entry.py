import logging

from demo_chat.application.services import WebSocketServices


async def websocket_endpoint(routeKey, context, payload, wss_url):    
    ws = WebSocketServices(endpoint_url=wss_url, table_name="chat-demo")
    
    print(f"websocket_endpoint invoked: {routeKey}")
    
    if routeKey == "$connect":
        ws.connect()
    
    if routeKey == "$disconnect":
        ws.disconnect(
            connectionId=context['connectionId']
        )

    if routeKey == "set_name":
        ws.set_name(
            name=payload['name'], 
            connectionId=context['connectionId']
        )
    
    if routeKey == "send_public":
        ws.send_public(
            message=payload['message'], 
            connectionId=context['connectionId']
        )
    
    if routeKey == "send_private":
        ws.send_private(
            message=payload['message'], 
            send_to=payload['to'], 
            connectionId=context['connectionId']
        )
    
    return { 'statusCode': 200 }
