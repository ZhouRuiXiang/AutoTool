import datetime
import math
import re
import time
from datetime import datetime

from loguru import logger
from model.order_info import OrderInfo
from model.product import Product
from service.device import open_device


logger = logger.bind(module="fish")



def open_fish_and_refresh():
    d = open_device()
    """
    一键擦亮
    :param d: 设备
    :return:
    """
    d.app_stop('com.taobao.idlefish')
    # 打开fish
    d.app_start('com.taobao.idlefish')
    # 点击“我的”
    # 点击“我的”
    d.xpath(
        '//*[@content-desc="我的，未选中状态"]/android.widget.RelativeLayout[1]/'
        'android.widget.LinearLayout[1]/'
        'android.widget.FrameLayout[1]').click()
    time.sleep(2)
    # 点击“我发布的”
    d(descriptionContains="我发布的", className='android.widget.ImageView').click()
    time.sleep(2)
    refresh_element = d.xpath('//*[@content-desc="一键擦亮"]')
    if refresh_element.exists:
        refresh_element.click()
        logger.info("【闲鱼】擦亮成功")
    else:
        logger.warning("【闲鱼】已擦亮, 无需重复擦亮")
    time.sleep(2)
    d.app_stop('com.taobao.idlefish')


def open_fish_and_batch_parse_order_info():
    d = open_device()
    """
    获取订单数据 & 入库
    :param d: 设备
    :return:
    """
    d.app_stop('com.taobao.idlefish')
    # 打开fish
    d.app_start('com.taobao.idlefish')
    time.sleep(5)
    # 点击“我的”
    d.xpath(
        '//*[@content-desc="我的，未选中状态"]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]').click()
    time.sleep(2)
    # 获取店铺名称
    store_name = d.xpath('//android.widget.ScrollView/android.view.View[1]').info.get('contentDescription')
    # 点击“我卖出的”
    sell_out_elements = d(descriptionContains="我卖出的", className='android.widget.ImageView')
    sell_out_elements.click()
    time.sleep(1)
    # 点击“待发货”
    sell_out_elements = d(descriptionContains="待发货", className='android.view.View')
    sell_out_elements.click()
    time.sleep(1)
    logger.info("【闲鱼】开始获取订单信息")
    product_element_scroll_xpath = '//android.widget.ScrollView'
    if d.xpath(product_element_scroll_xpath).exists:
        # 超过四个商品待发货  带滚轮
        for i in range(4):
            i = i + 1
            product_element_xpath = f'//android.widget.ScrollView/android.view.View[{i}]'
            if d.xpath(product_element_xpath).exists:
                product_element = d.xpath(product_element_xpath)

                parse_product_and_deliver_info(d, store_name, product_element)
        # 滚轮下滑 逐个获取全部发货信息
        while not d.xpath('//*[@content-desc="哎呀，到底了"]').exists:
            width, height = d.window_size()
            # 向下滑动页面
            d.swipe(width // 2, height * 3 // 4, width // 2, height // 18, 1.2)
            for i in range(5):
                i = i + 1
                product_element_xpath = f'//android.widget.ScrollView/android.view.View[{i}]'
                if not d.xpath(product_element_xpath).exists:
                    break
                if d.xpath(product_element_xpath).info.get('contentDescription') == "哎呀，到底了":
                    break
                if d.xpath(product_element_xpath).exists:
                    product_element = d.xpath(product_element_xpath)
                    parse_product_and_deliver_info(d, store_name, product_element)
        for i in range(4):
            i = i + 1
            product_element_xpath = f'//android.widget.ScrollView/android.view.View[{i}]'
            if d.xpath(product_element_xpath).exists:
                product_element = d.xpath(product_element_xpath)
                parse_product_and_deliver_info(d, store_name, product_element)
    else:
        # 小于四个商品待发货 不带滚轮
        for i in range(4):
            i = i + 1
            product_element_xpath = f'//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[7]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[{i}]'
            if not d.xpath(product_element_xpath).exists:
                logger.info("【闲鱼】暂无订单数据, 请稍后再试!")
                break
            if d.xpath(product_element_xpath).info.get('contentDescription') == "哎呀，到底了":
                break
            if d.xpath(product_element_xpath).exists:
                product_element = d.xpath(product_element_xpath)
                parse_product_and_deliver_info(d, store_name, product_element)

    # 关闭应用
    d.app_stop('com.taobao.idlefish')


def parse_product_and_deliver_info(d, store_name, product_element):
    """
    解析商品和订单信息
    :param d: 设备
    :param store_name: 商铺名称
    :param product_element:  商品元素
    :param product_dict_info: 商品信息map
    :return:
    """
    product_dict_info = {}
    # 获取商品信息
    product_info = product_element.info.get('contentDescription')

    product_element.click()
    user_info_xpath = '//android.widget.ScrollView/android.widget.ImageView[2]'
    user_info_text = d.xpath(user_info_xpath).info.get('contentDescription')
    # 获取订单编号、支付宝交易号
    trans_id_xpath = '//android.widget.ScrollView/android.view.View[1]'
    trans_id_text = d.xpath(trans_id_xpath).info.get('contentDescription')
    trans_id_list = trans_id_text.split("复制")
    order_id = trans_id_list[0].split("订单编号")[1].replace("\n", "")
    logger.info(f"【闲鱼】正在获取订单信息, 订单编号:{order_id}")
    alipay_trans_id = trans_id_list[1].split("支付宝交易号")[1].replace("\n", "")

    # 发货信息处理
    lines = user_info_text.replace("复制\n", "").split("\n")
    delivery_info = ['delivery_user', 'delivery_phone', 'delivery_full_address']
    delivery_user_info = {key: value for key, value in zip(delivery_info, lines)}

    product_info_arr = product_info.split("\n")

    if '×' in product_info:
        product_dict_info["product_count"] = int(product_info_arr[5][1:])
    else:
        product_dict_info["product_count"] = 1
    # 无商品尺寸
    product_no_size_list = Product.get_product_list_by_no_size(0)

    no_size_flag = 0
    for product_no_size in product_no_size_list:
        if product_no_size.name in product_info_arr[2]:
            no_size_flag = 1

    for index, value in enumerate(product_info_arr):

        if index == 0:
            product_dict_info["username"] = value
        elif index == 2:
            product_dict_info["product_name"] = value
        elif index == 3:
            if no_size_flag:
                product_dict_info["total_price"] = value[1:]
            else:
                product_size_str = format_size_string(value)
                # product_dict_info["product_size"] = value.split(";")[0].split(":")[1]
                product_dict_info["product_size"] = product_size_str
        elif index == 4:
            if not no_size_flag:
                product_dict_info["total_price"] = value[1:]

    if "product_size" in product_dict_info:
        product_size = product_dict_info["product_size"]
    else:
        product_size = "默认"
    # 将客户真实信息 写入数据库持久化
    order = OrderInfo.get_order_by_order_id(order_id)
    if order is None:
        OrderInfo.create_order(order_id=order_id, store_name=store_name,
                               alipay_trans_id=alipay_trans_id, nickname=product_dict_info["username"],
                               product_name=product_dict_info['product_name'],
                               product_count=product_dict_info['product_count'],
                               sale_price=product_dict_info["total_price"],
                               product_size=product_size,
                               deliver_user=delivery_user_info['delivery_user'],
                               deliver_phone=delivery_user_info['delivery_phone'],
                               deliver_full_address=delivery_user_info['delivery_full_address'], order_status=1,
                               month=datetime.now().strftime('%Y%m')
                               )
        logger.info(f"【闲鱼】订单入库成功, 订单编号:{order_id}")
    else:
        logger.warning(f"【闲鱼】订单已入库, 订单编号:{order_id}")
    # 返回上一级
    d.xpath(
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.widget.ImageView[1]').click()


def deliver_and_notify_user():
    d = open_device()
    """
    发货
    :param d:
    :return:
    """
    logger.info("【闲鱼】准备发货, 开始获取闲鱼待发货的订单")
    # 查询出所有的pdd已发货闲鱼待发货待提醒订单
    notify_order_list = OrderInfo.get_order_list_by_status(3)
    if not notify_order_list:
        logger.info("【闲鱼】库中暂未查询到待发货（待通知）订单")
        return
    notify_order_dict = {order.order_id: order for order in notify_order_list}

    d.app_stop('com.taobao.idlefish')
    # 打开fish
    d.app_start('com.taobao.idlefish')
    time.sleep(5)
    # 点击“我的”
    d.xpath(
        '//*[@content-desc="我的，未选中状态"]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]').click()
    time.sleep(2)
    # 获取店铺名称
    store_name = d.xpath('//android.widget.ScrollView/android.view.View[1]').info.get('contentDescription')
    # 点击“我卖出的”
    sell_out_elements = d(descriptionContains="我卖出的", className='android.widget.ImageView')
    sell_out_elements.click()
    time.sleep(5)
    # 点击“待发货”
    sell_out_elements = d(descriptionContains="待发货", className='android.view.View')
    sell_out_elements.click()
    time.sleep(5)
    product_element_scroll_xpath = '//android.widget.ScrollView'
    if d.xpath(product_element_scroll_xpath).exists:
        # 超过四个商品待发货  带滚轮
        while not d.xpath('//*[@content-desc="哎呀，到底了"]').exists:
            time.sleep(5)
            width, height = d.window_size()

            for i in range(5):
                i = i + 1
                if d.xpath(product_element_scroll_xpath).exists:
                    product_element_xpath = f'//android.widget.ScrollView/android.view.View[{i}]'
                else:
                    product_element_xpath = f'//*[@resource-id="android:id/content"]' \
                                            f'/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]' \
                                            f'/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]' \
                                            f'/android.view.View[1]/android.view.View[1]/android.view.View[7]' \
                                            f'/android.view.View[1]/android.view.View[1]/android.view.View[1]' \
                                            f'/android.view.View[1]/android.view.View[{i}]'
                if not d.xpath(product_element_xpath).exists:
                    break
                if d.xpath(product_element_xpath).info.get('contentDescription') == "哎呀，到底了":
                    break
                order_id = get_order_id_from_product_element(d, product_element_xpath)

                if order_id in notify_order_dict:
                    # 发货
                    deliver_goods(d, notify_order_dict[order_id].track_num, order_id)
                else:
                    logger.warning(f"【闲鱼】订单暂不可发货, 订单编号:{order_id}")
                    # 返回上一级
                    d.xpath('//*[@resource-id="android:id/content"]'
                            '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                            '/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]'
                            '/android.view.View[1]/android.view.View[1]/android.widget.ImageView[1]').click()

            # 向下滑动页面
            d.swipe(width // 2, height * 3 // 4, width // 2, height // 18, 1.2)

        for i in range(5):
            i = i + 1
            if d.xpath(product_element_scroll_xpath).exists:
                product_element_xpath = f'//android.widget.ScrollView/android.view.View[{i}]'
            else:
                product_element_xpath = f'//*[@resource-id="android:id/content"]' \
                                        f'/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]' \
                                        f'/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]' \
                                        f'/android.view.View[1]/android.view.View[1]/android.view.View[7]' \
                                        f'/android.view.View[1]/android.view.View[1]/android.view.View[1]' \
                                        f'/android.view.View[1]/android.view.View[{i}]'
            if not d.xpath(product_element_xpath).exists:
                break
            if d.xpath(product_element_xpath).info.get('contentDescription') == "哎呀，到底了":
                break
            order_id = get_order_id_from_product_element(d, product_element_xpath)

            if order_id in notify_order_dict:
                # 发货
                deliver_goods(d, notify_order_dict[order_id].track_num, order_id)
            else:
                logger.warning(f"【闲鱼】订单暂不可发货, 订单编号:{order_id}")
                # 返回上一级
                d.xpath('//*[@resource-id="android:id/content"]'
                        '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                        '/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]'
                        '/android.view.View[1]/android.view.View[1]/android.widget.ImageView[1]').click()

    else:
        # 小于四个商品待发货 不带滚轮
        i = 1
        while True:
            product_element_xpath = f'//*[@resource-id="android:id/content"]' \
                                    f'/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]' \
                                    f'/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]' \
                                    f'/android.view.View[1]/android.view.View[1]/android.view.View[7]' \
                                    f'/android.view.View[1]/android.view.View[1]/android.view.View[1]' \
                                    f'/android.view.View[1]/android.view.View[{i}]'
            if not d.xpath(product_element_xpath).exists:
                break
            if d.xpath(product_element_xpath).info.get('contentDescription') == "哎呀，到底了":
                break
            order_id = get_order_id_from_product_element(d, product_element_xpath)
            if order_id in notify_order_dict:
                # 发货
                deliver_goods(d, notify_order_dict[order_id].track_num, order_id)
            else:
                logger.warning(f"【闲鱼】订单暂不可发货, 订单编号:{order_id}")
                # 返回上一级
                d.xpath('//*[@resource-id="android:id/content"]'
                        '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                        '/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]'
                        '/android.view.View[1]/android.view.View[1]/android.widget.ImageView[1]').click()
            i = i + 1

    # 关闭应用
    d.app_stop('com.taobao.idlefish')


def get_order_id_from_product_element(d, product_element_xpath):
    product_element = d.xpath(product_element_xpath)
    product_element.click()
    time.sleep(2)
    # 获取订单编号
    trans_id_xpath = '//android.widget.ScrollView/android.view.View[1]'
    trans_id_text = d.xpath(trans_id_xpath).info.get('contentDescription')
    trans_id_list = trans_id_text.split("复制")
    order_id = trans_id_list[0].split("订单编号")[1].replace("\n", "")
    return order_id


def deliver_goods(d, track_num, order_id):
    logger.info(f"【闲鱼】闲鱼订单编号:{order_id}, 开始发货")
    width, height = d.window_size()
    # 发货
    d.click(math.floor(width * 0.852), math.floor(height * 0.966))
    time.sleep(10)
    product_element_scroll_xpath = '//android.widget.ScrollView/android.view.View[2]/android.widget.ImageView[1]'
    d.xpath(product_element_scroll_xpath).click()
    time.sleep(1)
    d.xpath('//*[@text="请填写"]').click()
    time.sleep(2)
    search_box = d.xpath('//*[@text="请填写"]')
    # 搜索匹配关键词
    search_box.set_text(track_num)
    time.sleep(5)
    # 关闭输入法弹框
    d.click(math.floor(width * 0.929), math.floor(height * 0.707))
    time.sleep(1)
    d.click(math.floor(width * 0.929), math.floor(height * 0.707))
    time.sleep(1)
    # 提交按钮
    d.xpath('//*[@content-desc="提交"]').click()
    confirm_btn_element = '//*[@content-desc="确认"]'
    time.sleep(2)
    if d.xpath(confirm_btn_element).exists:
        d.xpath(confirm_btn_element).click()
        logger.info(f"【闲鱼】闲鱼订单编号:{order_id}, 发货完成")
    # time.sleep(8)
    # 联系买家
    # d.xpath('//*[@resource-id="android:id/content"]'
    #         '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
    #         '/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]'
    #         '/android.view.View[1]/android.view.View[1]/android.widget.ImageView[3]').click()
    # 发送物流单号
    # send_msg_box = d.xpath('//*[@content-desc="想跟TA说点什么..."]/android.view.View[1]')
    # send_msg_box.click()
    # send_msg_box.set_text(track_num)
    # d(description="发送", className='android.view.View').click()
    # logger.info(f"【闲鱼】闲鱼订单编号:{order_id}, 通知买家成功")
    time.sleep(3)
    # 修改订单状态
    OrderInfo.update_order_status_by_order_id(order_id, 4)
    # 返回待发货页面
    # d.xpath('//*[@content-desc="返回"]').click()
    time.sleep(2)
    # 返回上一级
    d.xpath('//*[@resource-id="android:id/content"]'
            '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
            '/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]'
            '/android.view.View[1]/android.view.View[1]/android.widget.ImageView[1]').click()


def format_size_string(size_str):
    result = []
    groups = re.findall(r'([^:;]+):([^:;]+)', size_str)
    for group in groups:
        result.append(group[1])
    return ';'.join(result)