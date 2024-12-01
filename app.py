from flask import Flask, request, jsonify
from order_book import order_book
from models import Order
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    quantity = data.get('quantity')
    price = data.get('price')
    side = data.get('side')

    if not quantity or not price or not side:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        quantity = int(quantity)
        price = float(price)
        side = int(side)
        assert quantity > 0 and price > 0 and side in [1, -1]
    except (ValueError, AssertionError):
        return jsonify({'error': 'Invalid input data'}), 400

    order = Order(quantity=quantity, price=price, side=side)
    order_book.place_order(order)
    return jsonify({'order_id': order.order_id}), 201

@app.route('/orders/<order_id>', methods=['PUT'])
def modify_order(order_id):
    data = request.get_json()
    new_price = data.get('price')

    if not new_price:
        return jsonify({'error': 'Missing price field'}), 400

    try:
        new_price = float(new_price)
        assert new_price > 0
    except (ValueError, AssertionError):
        return jsonify({'error': 'Invalid price'}), 400

    success = order_book.modify_order(order_id, new_price)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Order not found or already filled'}), 404

@app.route('/orders/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    success = order_book.cancel_order(order_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Order not found or already filled'}), 404

@app.route('/orders/<order_id>', methods=['GET'])
def fetch_order(order_id):
    order = order_book.get_order_by_id(order_id)
    if order:
        return jsonify(order.to_dict()), 200
    else:
        return jsonify({'error': 'Order not found'}), 404

@app.route('/orders', methods=['GET'])
def fetch_all_orders():
    orders_list = [order.to_dict() for order in order_book.get_all_orders()]
    return jsonify(orders_list), 200

@app.route('/trades', methods=['GET'])
def fetch_all_trades():
    trades_list = [trade.to_dict() for trade in order_book.get_all_trades()]
    return jsonify(trades_list), 200

@app.route('/price', methods=['GET'])
def get_current_price():
    current_price = order_book.get_current_price()
    if current_price is not None:
        return jsonify({'current_price': current_price}), 200
    else:
        return jsonify({'message': 'No trades have occurred yet.'}), 200

if __name__ == '__main__':
    order_book.initialize_dummy_data()
    app.run(debug=True)
