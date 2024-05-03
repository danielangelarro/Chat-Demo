import boto3


class DynamoDBHandler:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_item(self, connectionId):
        key = {'connectionId': connectionId}
        response = self.table.get_item(Key=key)

        return response['Item'] if 'Item' in response else None
    
    def get_all_keys(self):
        response = self.table.scan(
            ProjectionExpression='connectionId'
        )
        keys = [item['connectionId'] for item in response['Items']]

        return keys

    def get_all_values(self):
        response = self.table.scan(
            ProjectionExpression='#name',
            ExpressionAttributeNames={'#name': 'name'}
        )
        values = [item['name'] for item in response['Items']]

        return values

    def get_all(self):
        response = self.table.scan(
            ProjectionExpression='#connectionId, #name',
            ExpressionAttributeNames={'#connectionId': 'connectionId', '#name': 'name'}
        )
        key_value_pairs = [(item['connectionId'], item['name']) for item in response['Items']]
        
        return key_value_pairs

    def put_item(self, item):
        self.table.put_item(Item=item)

    def delete_item(self, key):
        self.table.delete_item(Key=key)
