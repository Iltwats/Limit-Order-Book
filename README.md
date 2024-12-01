# Order Matching Engine API
This project implements a simple order matching engine using Flask. It simulates a trading system where users can place buy and sell orders, which are then matched based on price and quantity. The system maintains an in-memory order book and provides RESTful API endpoints for interacting with the engine.

## Features
- **Place Order**: Submit new buy or sell orders.
- **Modify Order**: Update the price of existing orders.
- **Cancel Order**: Cancel existing orders.
- **Fetch Order**: Retrieve details of a specific order.
- **List All Orders**: Get all orders currently in the system.
- **List All Trades**: Get a history of all executed trades.
- **Get Current Price**: Retrieve the last traded price of the stock.

## Requirements
- Python 3.6+
- Flask
- Flask-CORS

## Setup Instructions
1. Clone the Repository

```bash
git clone https://github.com/Iltwats/order-matching-engine.git
cd order-matching-engine
```
2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Run the Application

```bash
python3 app.py
```
The application will start on http://localhost:5000.

## Data Models
### Order
Represents a buy or sell order in the system.

- Attributes:
   - order_id: Unique identifier for the order.
   - price: Price per unit.
   - quantity: Total quantity ordered.
   - side: 1 for buy, -1 for sell.
   - status: Current status (open, filled, canceled).
   - traded_quantity: Quantity that has been traded.
   - average_traded_price: Average price at which the order has been traded.
   - timestamp: Time when the order was placed.

### Trade
Represents an executed trade resulting from matching orders.

- Attributes:
    - trade_id: Unique identifier for the trade.
    - execution_timestamp: Time when the trade was executed.
    - price: Execution price.
    - quantity: Quantity traded.
    - bid_order_id: order_id of the buy order.
    - ask_order_id: order_id of the sell order.

## Important Functions
### 1. `_match_order` in `OrderBook` Class
**Purpose**: Matches incoming orders against existing orders in the opposite side of the order book.

**Key Steps**:

- **Identify Matching Orders**: Determines which existing orders can be matched based on price and side.
- **Execute Trades**: For each matching order, executes trades and updates the quantities and statuses.
- **Update Last Traded Price**: Keeps track of the most recent trade price.
- **Create Trade Records**: Generates Trade objects for each executed trade.

### 2. `place_order` Endpoint in `app.py`
**Purpose**: Handles incoming requests to place new orders.

**Key Steps:**

- Input Validation: Ensures that all required fields are present and valid.
- Order Creation: Creates an Order object with the provided details.
- Order Placement: Calls order_book.place_order(order) to add the order to the system.
- Response: Returns the order_id of the newly created order.

## Testing the Application
The code file contains a [`postman collection`](https://github.com/Iltwats/order-api/blob/main/Trade%20Matching%20Engine.postman_collection.json) with all the http requests available in this project.
