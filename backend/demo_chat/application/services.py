import boto3
import json

from demo_chat.repositories.dynamodb.tables import DynamoDBHandler


class WebSocketServices:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, endpoint_url, table_name):
        
        self.client = boto3.client(
            'apigatewaymanagementapi', 
            endpoint_url=endpoint_url
        )
        self.DB = DynamoDBHandler(table_name)

    def send_to_one(self, connectionId, body):        
        try:
            self.client.post_to_connection(
                ConnectionId=connectionId,
                Data=json.dumps(body)
            )
        except Exception as err:
            print(f"Error: {err}")

    def send_to_all(self, ids, body):        
        for id in ids:
            self.send_to_one(id, body)

    def connect(self):
        return {}

    def set_name(self, name, connectionId):
                
        self.DB.put_item({'connectionId': connectionId, 'name': name})
        
        self.send_to_one(
            connectionId,
            {
                'systemMessage': f"Welcome {name}"
            }
        )
        
        self.send_to_all(
            list(self.DB.get_all_keys()), 
            {
                'members': list(self.DB.get_all_values())
            }
        )
        
        self.send_to_all(
            list(self.DB.get_all_keys()), 
            {
                'systemMessage': f"{self.DB.get_item(connectionId)} has joined the chat"
            }
        )
        return {}

    def send_public(self, message, connectionId):        
        self.send_to_all(
            list(self.DB.get_all_keys()), 
            {
                'publicMessage': f"{self.DB.get_item(connectionId)}: {message}"
            }
        )
        return {}

    def send_private(self, message, send_to, connectionId):        
        to = next(
            (key for key, value in self.DB.get_all() if value == send_to),
            None
        )
        
        if to:
            self.send_to_one(to, {'privateMessage': f"{self.DB.get_item(connectionId)}: {message}"})
        return {}

    def disconnect(self, connectionId):        
        self.send_to_all(
            list(self.DB.get_all_keys()), 
            {
                'systemMessage': f"{self.DB.get_item(connectionId)} has left the chat"
            }
        )
        
        self.DB.delete_item(connectionId)
        
        self.send_to_all(
            list(self.DB.get_all_keys()), 
            {
                'members': list(self.DB.get_all_values())
            }
        )
        
        return {}