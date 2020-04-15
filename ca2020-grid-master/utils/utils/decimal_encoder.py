import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    """
    Simple helper function to serialize json objects containing Decimal values (as is required by DynamoDB)
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
