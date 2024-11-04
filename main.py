import datetime
import math
import re

from service.device import open_device
from service.fish import open_fish_and_batch_parse_order_info, open_fish_and_refresh, deliver_and_notify_user
from service.jd import monitor_product
from service.log import setup_logger
from service.pdd import open_pdd_and_deliver, get_trace_number
import schedule
import time
from loguru import logger

from service.wechat import notify_user

product_name = 'instax立拍立得'
notify_wechat = 'AZ'

def deliver():
    # 获取订单数据
    open_fish_and_batch_parse_order_info()
    # # 开始下单
    open_pdd_and_deliver()


def jd_monitor():
    monitor_product(product_name, notify_wechat)


if __name__ == '__main__':
    setup_logger("sale")

    # 擦亮
    # open_fish_and_refresh()

    # 获取订单 & 下单
    # deliver()

    # 获取物流单号
    # get_trace_number()

    # 发货
    # deliver_and_notify_user()

    # monitor_product('instax立拍立得', 'AZ')
    # monitor_product('富士拍立得', '星辰')


    # 凌晨00:01分执行擦亮任务
    schedule.every().day.at("00:01").do(open_fish_and_refresh)
    # 每小时05分 获取订单数据 & 下单
    schedule.every().hour.at(":05").do(deliver)
    # 每两个小时的15分 获取物流单号
    schedule.every(1).hours.at(":15").do(get_trace_number)
    # 每两个小时的40分 发货
    schedule.every(1).hours.at(":41").do(deliver_and_notify_user)
    # 每30分钟执行 京东商品监控
    schedule.every().hour.at(":00").do(jd_monitor)
    schedule.every().hour.at(":30").do(jd_monitor)

    # 定时任务
    while True:
        schedule.run_pending()
        time.sleep(1)


