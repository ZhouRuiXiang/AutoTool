from peewee import *

db = MySQLDatabase('fishsale',
                   user='root',
                   password='xcc86977@@',
                   host='8.137.14.45',
                   charset='utf8mb4',
                   port=3306
                   )


class OrderInfo(Model):
    class Meta:
        database = db
        table_name = 'order_info'

    id = IntegerField(primary_key=True)
    order_id = CharField(max_length=50)
    alipay_trans_id = CharField(max_length=50)
    pdd_order_id = CharField(max_length=50)
    store_name = CharField(max_length=20)
    nickname = CharField(max_length=20)
    product_name = CharField(max_length=100)
    product_count = IntegerField()
    product_size = CharField(max_length=20)
    sale_price = DecimalField(max_digits=10, decimal_places=2)
    cost_price = DecimalField(max_digits=10, decimal_places=2)
    deliver_user = CharField(max_length=10)
    deliver_phone = CharField(max_length=11)
    deliver_full_address = CharField(max_length=200)
    deliver_province = CharField(max_length=10)
    deliver_city = CharField(max_length=20)
    deliver_district = CharField(max_length=50)
    deliver_detail = CharField(max_length=100)
    # 订单状态(1-待发货 2-已下单 3-已发货 4-已提醒用户 5-已完成 6-已退货 7-下单失败 8-暂时无货 9-提醒用户失败)
    order_status = IntegerField()
    month = CharField(max_length=10)
    # 物流单号
    track_num = CharField(max_length=50)
    product_config_id = IntegerField()
    create_time = DateField()
    update_time = DateField()

    # 新增订单
    @classmethod
    def create_order(cls, order_id, alipay_trans_id, store_name, nickname, product_name, product_count, sale_price,
                     product_size, deliver_user, deliver_phone, deliver_full_address, order_status, month):
        return cls.create(order_id=order_id, alipay_trans_id=alipay_trans_id, store_name=store_name,
                                nickname=nickname, product_name=product_name, product_count=product_count,
                                sale_price=sale_price, product_size=product_size, deliver_user=deliver_user,
                                deliver_phone=deliver_phone,
                                deliver_full_address=deliver_full_address, order_status=order_status,
                                month=month).id

    # 修改订单收货信息
    def update_order_deliver_info(self, deliver_province, deliver_city, deliver_district, deliver_detail):
        order = self.get(OrderInfo.id == self.id)
        order.deliver_province = deliver_province
        order.deliver_city = deliver_city
        order.deliver_district = deliver_district
        order.deliver_detail = deliver_detail

        order.save()

    # 修改订单状态-下单
    def update_order_status_and_cost_price(self, product_config_id, cost_price, new_status):
        order = self.get(OrderInfo.id == self.id)
        order.cost_price = cost_price
        order.order_status = new_status
        order.product_config_id = product_config_id
        order.save()

    def update_order_pdd_order_id(self, pdd_order_id):
        order = self.get(OrderInfo.id == self.id)
        order.pdd_order_id = pdd_order_id
        order.save()

    def update_order_status_and_trace_number(self, trace_number, new_status):
        """
        修改订单状态-已发货
        :param trace_number:物流单号
        :param new_status: 订单状态
        :return:
        """
        order = self.get(OrderInfo.id == self.id)
        order.track_num = trace_number
        order.order_status = new_status
        order.save()

    def update_order_status(self, new_status):
        order = self.get(OrderInfo.id == self.id)
        order.order_status = new_status
        order.save()

    @classmethod
    def update_order_status_by_order_id(cls, order_id, new_status):
        order = cls.get(OrderInfo.order_id == order_id)
        order.order_status = new_status
        order.save()

    # 查询订单通过闲鱼订单编号
    @classmethod
    def get_order_by_order_id(cls, order_id):
        order = cls.get_or_none(OrderInfo.order_id == order_id)
        return order

    # 查询订单通过pdd订单编号
    @classmethod
    def get_order_by_pdd_order_id(cls, pdd_order_id):
        order = cls.get_or_none(OrderInfo.pdd_order_id == pdd_order_id)
        return order


    @classmethod
    def get_order_list_by_status(cls, order_status):
        """
        查询指定订单状态的所有订单
        :param order_status:
        :return:
        """
        order_list = cls.select().where(cls.order_status == order_status)
        return order_list

