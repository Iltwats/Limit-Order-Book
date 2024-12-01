import uuid
from datetime import datetime, timezone

class Order:
    def __init__(self, quantity, price, side):
        self.order_id = str(uuid.uuid4())
        self.price = price
        self.quantity = quantity
        self.side = side  # 1 for buy, -1 for sell
        self.status = 'open'
        self.traded_quantity = 0
        self.average_traded_price = 0.0
        self.timestamp = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'price': self.price,
            'quantity': self.quantity,
            'side': self.side,
            'status': self.status,
            'traded_quantity': self.traded_quantity,
            'average_traded_price': self.average_traded_price,
            'timestamp': self.timestamp.isoformat(),
        }

class Trade:
    def __init__(self, bid_order_id, ask_order_id, price, quantity):
        self.trade_id = str(uuid.uuid4())
        self.execution_timestamp = datetime.now(timezone.utc)
        self.price = price
        self.quantity = quantity
        self.bid_order_id = bid_order_id
        self.ask_order_id = ask_order_id

    def to_dict(self):
        return {
            'trade_id': self.trade_id,
            'execution_timestamp': self.execution_timestamp.isoformat(),
            'price': self.price,
            'quantity': self.quantity,
            'bid_order_id': self.bid_order_id,
            'ask_order_id': self.ask_order_id,
        }
