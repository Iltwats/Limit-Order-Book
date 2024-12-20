from sortedcontainers import SortedDict
from collections import deque
from models import Order, Trade


class OrderBook:
    def __init__(self):
        # sorteddict, allows for efficient insertion, deletion, and lookup operations in O(log n) time.
        self.bids = SortedDict()  # Price level to orders
        self.asks = SortedDict()
        self.order_id_map = {}  # Order ID to Order object
        self.trades = []
        self.last_traded_price = None

    def initialize_dummy_data(self):
        # orders = [
        #     Order(quantity=100, price=10.00, side=1),  # Buy order
        #     Order(quantity=150, price=10.50, side=1),  # Buy order
        #     Order(quantity=200, price=11.00, side=-1),  # Sell order
        #     Order(quantity=250, price=11.50, side=-1),  # Sell order
        # ]
        # for order in orders:
        #     self.place_order(order)
        pass

    def place_order(self, order):
        self.order_id_map[order.order_id] = order

        if order.side == 1:
            self._add_order(self.bids, order)
            self._match_order(order, self.asks, self.bids)
        else:
            self._add_order(self.asks, order)
            self._match_order(order, self.bids, self.asks)

    def modify_order(self, order_id, new_price):
        order = self.order_id_map.get(order_id)
        if not order or order.status != "open":
            return False

        order_queue = self.bids if order.side == 1 else self.asks
        # Remove from current price level
        orders_at_price = order_queue[order.price]
        orders_at_price.remove(order)
        if not orders_at_price:
            del order_queue[order.price]

        # Update price and re-insert
        order.price = new_price
        self._add_order(order_queue, order)
        return True

    def cancel_order(self, order_id):
        order = self.order_id_map.get(order_id)
        if not order or order.status != "open":
            return False

        order_queue = self.bids if order.side == 1 else self.asks
        orders_at_price = order_queue[order.price]
        orders_at_price.remove(order)
        if not orders_at_price:
            del order_queue[order.price]

        order.status = "canceled"
        return True

    def _add_order(self, order_queue, order):
        if order.price not in order_queue:
            order_queue[order.price] = deque()
        order_queue[order.price].append(order)

    def _match_order(self, incoming_order, opposite_queue, own_queue):
        if incoming_order.side == 1:
            # Buy order, match against lowest ask
            price_levels = opposite_queue.keys()
            comparison = lambda price: price <= incoming_order.price
        else:
            # Sell order, match against highest bid
            price_levels = reversed(opposite_queue.keys())
            comparison = lambda price: price >= incoming_order.price

        for price in price_levels:
            if not comparison(price):
                break

            orders_at_price = opposite_queue[price]
            while orders_at_price and incoming_order.quantity > 0:
                resting_order = orders_at_price[0]
                traded_qty = min(incoming_order.quantity, resting_order.quantity)

                # Ensure traded_qty is positive
                if traded_qty <= 0:
                    break

                trade_price = resting_order.price

                # Update orders
                incoming_order.quantity -= traded_qty
                incoming_order.traded_quantity += traded_qty

                if incoming_order.traded_quantity > 0:
                    incoming_order.average_traded_price = (
                        incoming_order.average_traded_price
                        * (incoming_order.traded_quantity - traded_qty)
                        + trade_price * traded_qty
                    ) / incoming_order.traded_quantity
                else:
                    incoming_order.average_traded_price = trade_price

                resting_order.quantity -= traded_qty
                resting_order.traded_quantity += traded_qty

                if resting_order.traded_quantity > 0:
                    resting_order.average_traded_price = (
                        resting_order.average_traded_price
                        * (resting_order.traded_quantity - traded_qty)
                        + trade_price * traded_qty
                    ) / resting_order.traded_quantity
                else:
                    resting_order.average_traded_price = trade_price

                # Determine which order is the buy order and which is the sell order
                if incoming_order.side == 1:
                    bid_order_id = incoming_order.order_id
                    ask_order_id = resting_order.order_id
                else:
                    bid_order_id = resting_order.order_id
                    ask_order_id = incoming_order.order_id

                # Create the trade object
                trade = Trade(
                    bid_order_id=bid_order_id,
                    ask_order_id=ask_order_id,
                    price=trade_price,
                    quantity=traded_qty,
                )
                self.trades.append(trade)

                # Update the last traded price
                self.last_traded_price = trade_price

                # Update order statuses
                if resting_order.quantity == 0:
                    resting_order.status = "filled"
                    orders_at_price.popleft()
                    if not orders_at_price:
                        del opposite_queue[price]
                else:
                    resting_order.status = "open"

                if incoming_order.quantity == 0:
                    incoming_order.status = "filled"
                    return
                else:
                    incoming_order.status = "open"

        # If not fully matched, add to own queue
        if incoming_order.quantity > 0 and incoming_order.status != "filled":
            self._add_order(own_queue, incoming_order)

    def get_order_by_id(self, order_id):
        return self.order_id_map.get(order_id)

    def get_current_price(self):
        return self.last_traded_price

    def get_all_orders(self):
        return list(self.order_id_map.values())

    def get_all_trades(self):
        return self.trades


order_book = OrderBook()
