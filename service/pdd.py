import datetime
import math
import re
import time
from model.product import Product
from model.product_config import ProductConfig
from model.order_info import OrderInfo
from loguru import logger

from service.device import open_device

logger = logger.bind(module="pdd")


def parse_and_save_trace_info(d):
    try:
        # 通过pdd的订单编号进行查询
        pdd_order_element_1 = '//*[@resource-id="android:id' \
                              '/content"]/android.widget.FrameLayout[1]' \
                              '/android.support.v7.widget.RecyclerView[1]' \
                              '/android.view.ViewGroup[1]' \
                              '/android.widget.TextView[2]'

        pdd_order_element_2 = '//*[@resource-id="android:id/content"]' \
                              '/android.widget.FrameLayout[1]' \
                              '/android.view.ViewGroup[1]' \
                              '/android.widget.FrameLayout[2]' \
                              '/android.support.v7.widget.RecyclerView[1]' \
                              '/android.view.ViewGroup[1]' \
                              '/android.widget.TextView[2]'
        pdd_order_element_3 = '//*[@resource-id="android:id/content"]' \
                              '/android.widget.FrameLayout[1]' \
                              '/android.view.ViewGroup[1]/android.widget.FrameLayout[2]' \
                              '/android.support.v7.widget.RecyclerView[1]' \
                              '/android.view.ViewGroup[3]' \
                              '/android.widget.TextView[2]'
        pdd_order_id = ""
        if d.xpath(pdd_order_element_1).exists and d.xpath(pdd_order_element_1).info.get('text') == '复制':
            d.xpath(pdd_order_element_1).click()
            confirm_alert = d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                                    '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]')
            if confirm_alert.exists:
                confirm_alert.click()
            pdd_order_id_text = d.clipboard.strip()
            if "订单编号" in pdd_order_id_text:
                pdd_order_id = pdd_order_id_text.split(': ')[1]
        if d.xpath(pdd_order_element_2).exists and d.xpath(pdd_order_element_2).info.get('text') == '复制':
            d.xpath(pdd_order_element_2).click()
            confirm_alert = d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                                    '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]')
            if confirm_alert.exists:
                confirm_alert.click()
            pdd_order_id_text = d.clipboard.strip()
            if "订单编号" in pdd_order_id_text:
                pdd_order_id = pdd_order_id_text.split(': ')[1]
        if d.xpath(pdd_order_element_3).exists and d.xpath(pdd_order_element_3).info.get('text') == '复制':
            d.xpath(pdd_order_element_3).click()
            confirm_alert = d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                                    '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]')
            if confirm_alert.exists:
                confirm_alert.click()
            pdd_order_id_text = d.clipboard.strip()
            if "订单编号" in pdd_order_id_text:
                pdd_order_id = pdd_order_id_text.split(': ')[1]
        order = OrderInfo.get_order_by_pdd_order_id(pdd_order_id)

        #
        if order is None or order.id is None:
            logger.warning(f"【拼多多】获取物流单号, 未查询到订单, pdd_order_id:{pdd_order_id}")
            return False

        if d.xpath('//*[@resource-id="android:id/content"]'
                   '/android.widget.FrameLayout[1]'
                   '/android.support.v7.widget.RecyclerView[1]'
                   '/android.widget.LinearLayout[1]'
                   '/android.view.ViewGroup[1]'
                   '/android.widget.TextView[3]').exists:
            d.xpath('//*[@resource-id="android:id/content"]'
                    '/android.widget.FrameLayout[1]'
                    '/android.support.v7.widget.RecyclerView[1]'
                    '/android.widget.LinearLayout[1]'
                    '/android.view.ViewGroup[1]'
                    '/android.widget.TextView[3]').click()
        elif d.xpath(
                '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                '/android.view.ViewGroup[1]/android.widget.FrameLayout[2]'
                '/android.support.v7.widget.RecyclerView[1]'
                '/android.widget.LinearLayout[1]'
                '/android.view.ViewGroup[1]'
                '/android.widget.TextView[3]').exists:
            d.xpath(
                '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                '/android.view.ViewGroup[1]/android.widget.FrameLayout[2]'
                '/android.support.v7.widget.RecyclerView[1]'
                '/android.widget.LinearLayout[1]'
                '/android.view.ViewGroup[1]'
                '/android.widget.TextView[3]').click()
        elif d.xpath('//*[@resource-id="android:id/content"]'
                '/android.widget.FrameLayout[1]'
                '/android.view.ViewGroup[1]'
                '/android.widget.FrameLayout[2]'
                '/android.support.v7.widget.RecyclerView[1]'
                '/android.widget.LinearLayout[1]'
                '/android.view.ViewGroup[1]'
                '/android.widget.TextView[3]').exists:
            d.xpath('//*[@resource-id="android:id/content"]'
                    '/android.widget.FrameLayout[1]'
                    '/android.view.ViewGroup[1]'
                    '/android.widget.FrameLayout[2]'
                    '/android.support.v7.widget.RecyclerView[1]'
                    '/android.widget.LinearLayout[1]'
                    '/android.view.ViewGroup[1]'
                    '/android.widget.TextView[3]').click()

        confirm_alert = d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                                '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]')
        if confirm_alert.exists:
            confirm_alert.click()

        # 获取剪切板中的物流单号
        trace_number = d.clipboard.strip()
        # 修改订单状态和物流单号
        if order.order_status == 2:
            order.update_order_status_and_trace_number(trace_number, 3)
            logger.info(f"【拼多多】获取物流单号, 订单{order.pdd_order_id}发货完成, 订单物流号码:{trace_number}")
            return False
        elif order.order_status in [3, 4, 5]:
            logger.info(f"【拼多多】获取物流单号, 订单{order.pdd_order_id}已发货, 无需重复发货")
            return False
    except Exception as e:
        logger.error(f"【拼多多】获取物流单号, 发生异常")
        logger.catch(e)
        return True


def get_trace_number():
    d = open_device()
    logger.info("【拼多多】获取物流单号, 正在获取待收货订单的物流单号")
    # 关闭再打开 pdd
    d.app_stop('com.xunmeng.pinduoduo')
    d.app_start('com.xunmeng.pinduoduo')

    time.sleep(5)
    # 关闭多余弹出框
    close_modal(d)
    # 个人中心
    d(text='个人中心', className='android.widget.TextView').click()
    time.sleep(1)
    # 待收货
    d(text='待收货', resourceId='com.xunmeng.pinduoduo:id/pdd', className='android.widget.TextView').click()

    while not d.xpath('//*[@text="没找到订单？试试查看全部或切换账号"]').exists:
        for i in range(4):
            i = i + 1
            trace_element_xpath = f'//android.support.v7.widget.RecyclerView/android.view.ViewGroup[{i}]' \
                # f'/android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.TextView[3]'

            trace_element_xpath = f'//android.support.v7.widget.RecyclerView/android.view.ViewGroup[{i}]' \
                                  f'/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.TextView[3]'
            # 商品列表
            product_element_xpath = f'//android.support.v7.widget.RecyclerView' \
                                    f'/android.view.ViewGroup[{i}]' \
                                    f'/android.view.ViewGroup[2]'
            if d.xpath(product_element_xpath).exists:
                if d.xpath(trace_element_xpath).exists:
                    # 查看物流
                    btn_text = d.xpath(trace_element_xpath).info.get('text')
                    if btn_text != '查看物流':
                        continue
                    d.xpath(trace_element_xpath).click()
                    time.sleep(3)
                    # 修改订单状态及物流信息
                    end_flag = parse_and_save_trace_info(d)
                    time.sleep(2)
                    # 返回按钮
                    d.xpath('//*[@resource-id="android:id/content"]'
                            '/android.widget.FrameLayout[1]'
                            '/android.widget.RelativeLayout[1]/android.view.ViewGroup[1]'
                            '/android.widget.ImageView[1]').click()
                    if end_flag:
                        d.app_stop('com.xunmeng.pinduoduo')
                        return

        width, height = d.window_size()
        # 向下滑动页面
        d.swipe(width // 2, height * 3 // 4, width // 2, height // 15, 1.2)

    for i in range(3):
        i = i + 1
        trace_element_xpath = f'//android.support.v7.widget.RecyclerView/android.view.ViewGroup[{i}]' \
                              f'/android.widget.FrameLayout[2]/android.widget.LinearLayout[1]' \
                              f'/android.widget.TextView[3]'
        if d.xpath(trace_element_xpath).exists:
            # 查看物流
            btn_text = d.xpath(trace_element_xpath).info.get('text')
            if btn_text != '查看物流':
                continue
            d.xpath(trace_element_xpath).click()
            time.sleep(3)
            # 修改订单状态及物流信息
            end_flag = parse_and_save_trace_info(d)
            time.sleep(2)
            # 返回按钮
            d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                    '/android.widget.RelativeLayout[1]/android.view.ViewGroup[1]'
                    '/android.widget.ImageView[1]').click()
            if end_flag:
                d.app_stop('com.xunmeng.pinduoduo')
                return


def open_pdd_and_deliver():
    d = open_device()
    """
    查询订单 & 发货
    :param d: 设备
    :return:
    """
    logger.info("【拼多多】开始下单, 正在获取订单信息")
    # 获取所有商品
    product_list = Product.get_all_product()
    # 直辖市映射关系
    municipality_list = {'北京': '北京市', '上海': '上海市', '天津': '天津市', '重庆': '重庆市'}
    # 待发货的订单列表
    order_list = OrderInfo.get_order_list_by_status(1)
    if len(order_list) == 0:
        logger.info("【拼多多】暂无下单数据, 请稍候再试!")
    for order_info in order_list:
        for product in product_list:
            if product.name in order_info.product_name:
                pdd_search_name = product.pdd_search_name
                # 获取商品配置信息
                product_config_list = ProductConfig.get_product_config_list_by_product_id(product.id)
                deliver(d, order_info, municipality_list, pdd_search_name, product_config_list)
            else:
                # TODO 下单商品未配置 微信告警
                pass

    # 关闭 app
    d.app_stop('com.xunmeng.pinduoduo')


def deliver(d, order_info, municipality_list, pdd_search_name, product_config_list):
    """
    发货
    :param d:
    :param order_info:
    :param municipality_list:
    :param pdd_search_name:
    :param product_config_list:
    :return:
    """
    logger.info(f"【拼多多】用户:{order_info.nickname}开始下单")
    # 关闭再打开 pdd
    d.app_stop('com.xunmeng.pinduoduo')
    d.app_start('com.xunmeng.pinduoduo')

    # 关闭多余弹出框
    close_modal(d)
    # 个人中心
    d(text='个人中心', className='android.widget.TextView').click()
    time.sleep(1)
    # 商品收藏
    d(text='商品收藏', resourceId='com.xunmeng.pinduoduo:id/tv_title', className='android.widget.TextView').click()
    # 获取搜索关键词
    # 搜索
    time.sleep(3)
    d.xpath('//*[@content-desc="搜索"]').click()
    search_box = d.xpath('//*[@text="搜索你收藏的商品"]')
    # 搜索匹配关键词
    search_box.set_text(pdd_search_name)
    time.sleep(4)
    # 搜索按钮
    d(text='管理', className='android.widget.TextView').click()
    time.sleep(1)
    # 收藏的商品
    # d.xpath(
    #     '//*[@resource-id="android:id/content"]/android.view.ViewGroup[1]'
    #     '/android.widget.FrameLayout[3]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]'
    #     '/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[1]'
    #     '/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.ImageView[1]').click()

    d.xpath(
        '//*[@resource-id="android:id/content"]/android.view.ViewGroup[1]'
        '/android.widget.FrameLayout[3]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]'
        '/android.support.v7.widget.RecyclerView[1]/android.widget.FrameLayout[1]'
        '/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.ImageView[1]').click()

    d(textContains='发起拼单', resourceId='com.xunmeng.pinduoduo:id/pdd').click()
    time.sleep(2)
    # 查看收货地址
    address_btn = d.xpath(
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
        '/android.widget.LinearLayout[1]/android.view.ViewGroup[2]/android.widget.LinearLayout[1]'
        '/android.view.ViewGroup[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]'
        '/android.view.ViewGroup[1]/android.widget.ImageView[2]')

    address_new_btn = d.xpath(
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
        '/android.widget.LinearLayout[1]/android.view.ViewGroup[2]'
        '/android.widget.LinearLayout[1]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]'
        '/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[1]/android.widget.ImageView[2]'
    )

    address_btn_2 = d.xpath(
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
        '/android.widget.LinearLayout[1]/android.view.ViewGroup[1]'
        '/android.widget.LinearLayout[1]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]'
        '/android.widget.LinearLayout[1]/android.view.ViewGroup[1]/android.widget.ImageView[2]'
    )

    if address_btn.exists:
        address_btn.click()
    elif address_new_btn.exists:
        address_new_btn.click()
    elif address_btn_2.exists:
        address_btn_2.click()

    # 修改收货地址
    d(text='修改', className='android.widget.TextView').click()
    # 用户

    user_name_edit_text = d.xpath(
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.widget.EditText[1]')
    user_name_edit_text.click()
    time.sleep(2)
    d.xpath('//*[@content-desc="清空收货人姓名"]').click()

    # 收货信息
    user_name_edit_text.set_text(order_info.deliver_user)
    time.sleep(3)
    # 手机号
    user_phone_edit_text = d.xpath(
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[4]/android.widget.EditText[1]')
    user_phone_edit_text.click()
    set_empty(d, user_phone_edit_text)
    user_phone_edit_text.set_text("17374158754")
    time.sleep(1)
    # 收货地址
    user__area_text = d.xpath(
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[5]/android.widget.FrameLayout[2]/android.widget.TextView[1]')
    user__area_text.click()
    time.sleep(1)

    # 拆分再组装收货信息
    full_address = order_info.deliver_full_address
    # 直辖市特殊处理
    if full_address[0: 2] in list(municipality_list.keys()):
        full_address = full_address.replace(full_address[0: 2], municipality_list[full_address[0: 2]], 1)
    # 封装省市区结果 {'province': 'xxx', 'city': 'xxx', 'direct': 'xxx', 'address': 'xxxx'}
    element_info = split_address(full_address)
    # 保存收货信息
    order_info.update_order_deliver_info(element_info['province'], element_info['city'],
                                         element_info['direct'], element_info['address'])

    # 循环点击 省（）、市、区（县市）
    scroll_for_text(d, element_info['province'], True)
    d(text=element_info['province'], resourceId="com.xunmeng.pinduoduo:id/pdd",
      className='android.widget.TextView').click()
    time.sleep(1)
    if (element_info['province'] in list(municipality_list.values())) and element_info['province'] != '重庆市':
        scroll_for_text(d, element_info['direct'], False)
        d(text=element_info['direct'], resourceId="com.xunmeng.pinduoduo:id/pdd",
          className='android.widget.TextView').click()
        time.sleep(1)
    else:
        scroll_for_text(d, element_info['city'], False)
        d(text=element_info['city'], resourceId="com.xunmeng.pinduoduo:id/pdd",
          className='android.widget.TextView').click()
        time.sleep(1)
        scroll_for_text(d, element_info['direct'], False)
        d(text=element_info['direct'], resourceId="com.xunmeng.pinduoduo:id/pdd",
          className='android.widget.TextView').click()
        time.sleep(1)
    # 清空 & 编辑详细地址
    d.xpath('//*[@content-desc="清空详细地址"]').click()
    address_details_text = d.xpath(
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[6]/android.view.ViewGroup[1]/android.widget.EditText[1]')
    address_details_text.click()
    # 详细地址拼接
    real_mobile_phone = order_info.deliver_phone
    address_detail = element_info['address'] \
                     + '【' + '联系' + real_mobile_phone[: 3] + '-' \
                     + real_mobile_phone[3: 7] \
                     + '-' + real_mobile_phone[7:] + '收】'
    address_details_text.set_text(address_detail)
    # 保存
    d.xpath(
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[7]').click()
    time.sleep(1)
    # 返回
    sell_out_elements = d(descriptionContains="返回", className='android.widget.TextView')
    sell_out_elements.click()
    # 匹配商品尺寸、数量
    add_element = d.xpath('//*[@content-desc="增加数量"]')
    count = order_info.product_count
    if count > 1:
        for i in range(count - 1):
            add_element.click()

    product_config_dict = {product_config.fish_config: product_config.pdd_search_config
                           for product_config in product_config_list}

    product_config_id_dict = {product_config.pdd_search_config: product_config.id
                              for product_config in product_config_list}

    cur_product_config_id_list = []
    pdd_search_size_list = []
    product_size_list = order_info.product_size.split(";")
    for index, product_size in enumerate(product_size_list):
        pdd_search_size = product_config_dict[product_size]
        pdd_search_size_list.append(pdd_search_size)
        cur_product_config_id_list.append(str(product_config_id_dict[pdd_search_size]))
    # 商品配置 ID 多个用,分割
    cur_product_config_ids = ','.join(cur_product_config_id_list)
    width, height = d.window_size()
    for pdd_search_size in pdd_search_size_list:
        while not d(textContains=pdd_search_size, className='android.widget.TextView').exists():
            # 向下滑动页面
            d.swipe(width // 2, height * 3 // 4, width // 2, height // 4, 1.2)
            time.sleep(2)
        d(textContains=pdd_search_size, className='android.widget.TextView').click()
        if d(textContains='该款式售罄', className='android.widget.TextView'):
            # TODO 没货 告警 微信提醒
            order_info.update_order_status(7)
            logger.warning(f"【拼多多】用户:{order_info.nickname}购买的:{pdd_search_name},无货")
            return
        time.sleep(1)
    order = d(textContains='0元下单', className='android.widget.TextView')
    cost_price_text = order.info.get('text')
    # 获取商品总成本价
    cost_price = cost_price_text.split('¥')[1]
    # 下单
    order.click()
    time.sleep(10)
    logger.info(f"【拼多多】用户:{order_info.nickname}:下单完成")
    order_info.update_order_status_and_cost_price(cur_product_config_ids, cost_price, 2)
    # 查看订单详情
    width, height = d.window_size()
    # d.click(math.floor(width * 0.5), math.floor(height * 0.78))
    d.click(math.floor(width * 0.5), math.floor(height * 0.75))
    d.click(math.floor(width * 0.5), math.floor(height * 0.65))

    # 获取pdd订单编号
    share_text_element = d.xpath('//*[@resource-id="com.xunmeng.pinduoduo:id/tv_title"]')
    time.sleep(3)
    if share_text_element.exists and share_text_element.info.get('text') == '待分享':
        d.click(math.floor(width * 0.918), math.floor(height * 0.5))

        confirm_alert = d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                                '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]')
        if confirm_alert.exists:
            confirm_alert.click()
        time.sleep(2)
        pdd_order_id = d.clipboard.strip()

        # 校验 pdd_order_id 是否正常
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y%m%d")
        if pdd_order_id is not None and pdd_order_id.startswith(formatted_date[2:]):
            # 修改订单状态
            order_info.update_order_pdd_order_id(pdd_order_id)
            logger.info(f"【拼多多】用户:{order_info.nickname}:保存pdd_order_id成功, pdd_order_id:{pdd_order_id}")
        else:
            logger.error(f"【拼多多】用户:{order_info.nickname}:保存pdd_order_id异常, pdd_order_id:{pdd_order_id}")

    else:
        logger.error(f"【拼多多】用户:{order_info.nickname}:保存pdd_order_id失败, 未找到pdd_order_id")


def close_modal(d):
    # model_7
    # model_7 = d.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
    #                   '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
    #                   '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
    #                   '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
    #                   '/android.view.ViewGroup[1]/android.view.ViewGroup[1]')
    # if model_7.exists:
    #     model_7.click()
    #     logger.info("【拼多多】已关闭广告弹框 7")
    #     time.sleep(1)
    time.sleep(5)

    # model_1
    modal_1 = d.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]')
    if modal_1.exists:
        modal_1.click()
        logger.info("【拼多多】已关闭广告弹框 1")
        time.sleep(1)
    # model_2
    modal_2 = d.xpath('//android.widget.FrameLayout[2]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]')
    if modal_2.exists:
        modal_2.click()
        time.sleep(1)
        logger.info("【拼多多】已关闭广告弹框 2")

    # model_3
    modal_3 = d.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[1]')
    if modal_3.exists:
        modal_3.click()
        logger.info("【拼多多】已关闭广告弹框 3")
        time.sleep(1)

    # model_4
    model_4 = d.xpath('//android.widget.FrameLayout[2]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[1]')
    if model_4.exists:
        model_4.click()
        logger.info("【拼多多】已关闭广告弹框 4")
        time.sleep(1)

    # model_5
    model_5 = d.xpath('//android.widget.FrameLayout[2]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[2]/android.widget.ImageView[1]')
    if model_5.exists:
        model_5.click()
        logger.info("【拼多多】已关闭广告弹框 5")
        time.sleep(1)

    # model_6
    model_6 = d.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                      '/android.view.ViewGroup[2]/android.widget.ImageView[1]')
    if model_6.exists:
        model_6.click()
        logger.info("【拼多多】已关闭广告弹框 6")
        time.sleep(1)


def scroll_for_text(d, element_info, isUp):
    """
    滚轮滑动
    :param d:
    :param element_info:
    :param isUp:
    :return:
    """
    width, height = d.window_size()
    # 向上滑到顶
    if isUp:
        d.swipe(width // 2, height * 3 // 4, width // 2, height * 2, 1.5)
        time.sleep(1)

    # 向下滑到底直到找到目标元素
    while not d(text=element_info, resourceId="com.xunmeng.pinduoduo:id/pdd",
                className='android.widget.TextView').exists():
        # 向下滑动页面
        d.swipe(width // 2, height * 3 // 4, width // 2, height // 4, 1.2)
        time.sleep(2)


def set_empty(d, edit_text):
    text_length = len(edit_text.get_text())
    # 模拟按键删除操作，删除文本框中的内容
    for i in range(text_length):
        d.press("del")


def split_address(full_address):
    """
    省市区地址提取
    :param full_address: 地址详情
    :return:
    """
    # 匹配收货地址的正则表达式
    full_address_dict = {}
    reg = r'([^省]+自治区|.*?省|.*?行政区|.*?市)([^市]+自治州|.*?行政单位|.*?盟|市辖区|.*?市|.*?县)([^县]+县|.*?区|.*?市|.*?旗|.*?镇|.*?海域|.*?岛)?(.*)'
    result = re.match(reg, full_address)
    # 获取省、市、县、村镇信息
    province = result.group(1) if result.group(1) else ""
    city = result.group(2) if result.group(2) else ""
    direct = result.group(3) if result.group(3) else ""
    address_detail = result.group(4) if result.group(4) else ""

    full_address_dict["province"] = province
    full_address_dict["city"] = city
    # 特殊省市区判断
    if city == "中山市" and address_detail.startswith("古镇镇"):
        full_address_dict["direct"] = "古镇"
        full_address_dict["address"] = address_detail[3:]
    else:
        full_address_dict["direct"] = direct
        full_address_dict["address"] = address_detail
    return full_address_dict
