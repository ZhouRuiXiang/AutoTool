from flask import Flask, request, jsonify
from playhouse.shortcuts import model_to_dict
from models import OrderInfo

app = Flask(__name__)

# 新增订单接口
@app.route('/order', methods=['POST'])
def create_order():
    order_data = request.json
    try:
        OrderInfo.create(**order_data)
        return jsonify({'message': '订单创建成功'})
    except:
        return jsonify({'message': '订单创建失败'})

# 修改订单状态接口
@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    new_status = request.json.get('order_status')
    try:
        order = OrderInfo.get(OrderInfo.order_id == order_id)
        order.order_status = new_status
        order.save()
        return jsonify({'message': '订单状态更新成功'})
    except OrderInfo.DoesNotExist:
        return jsonify({'message': '订单不存在'})

# 查询订单信息接口
@app.route('/order/<int:order_id>', methods=['GET'])
def get_order_info(order_id):
    try:
        order = OrderInfo.get(OrderInfo.order_id == order_id)
        order_data = model_to_dict(order)
        return jsonify(order_data)
    except OrderInfo.DoesNotExist:
        return jsonify({'message': '订单不存在'})