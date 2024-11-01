import datetime
import math
import re

from sqlalchemy.sql.functions import current_date

from service.device import open_device
from service.fish import open_fish_and_batch_parse_order_info, open_fish_and_refresh, deliver_and_notify_user
from service.jd import monitor_product
from service.log import setup_logger
from service.pdd import open_pdd_and_deliver, get_trace_number
import schedule
import time
from loguru import logger

from service.wechat import notify_user


def deliver():
    # 获取订单数据
    open_fish_and_batch_parse_order_info()
    # # 开始下单
    open_pdd_and_deliver()



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
    monitor_product('instax立拍立得', 'AZ')
    # monitor_product('富士拍立得', '星辰')


    # 凌晨00:01分执行擦亮任务
    schedule.every().day.at("00:01").do(open_fish_and_refresh)
    # 每小时05分 获取订单数据 & 下单
    schedule.every().hour.at(":05").do(deliver)
    # 每两个小时的20分 获取物流单号
    schedule.every(2).hours.at(":20").do(get_trace_number)
    # 每两个小时的40分 发货
    schedule.every(2).hours.at(":40").do(deliver_and_notify_user)
    # 定时任务
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


