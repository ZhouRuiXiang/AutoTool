import time

from service.device import open_device
from loguru import logger

logger = logger.bind(module="wechat")


def notify_user(username, message):
    """
    微信用户通知
    """
    d = open_device()

    d.app_stop('com.tencent.mm')
    # 打开wechat
    d.app_start('com.tencent.mm')
    time.sleep(2)
    # 点击搜索框
    d.xpath('//*[@resource-id="com.tencent.mm:id/meb"]').click()
    time.sleep(1)
    # 输入搜索用户
    search_box = d.xpath('//android.widget.RelativeLayout')
    search_box.set_text(username)
    time.sleep(2)
    contact_ele = d.xpath('//*[@resource-id="com.tencent.mm:id/mfg"]'
                          '/android.widget.RelativeLayout[2]'
                          '/android.widget.LinearLayout[1]'
                          '/android.widget.LinearLayout[1]')
    if contact_ele.exists:
        contact_ele.click()
        time.sleep(3)
        # 输入内容
        send_msg_box = d.xpath('//*[@resource-id="com.tencent.mm:id/o4q"]')
        send_msg_box.click()
        send_msg_box.set_text(message)
        time.sleep(1)
        # 发送消息
        d.xpath('//*[@resource-id="com.tencent.mm:id/bql"]').click()
        time.sleep(3)

        logger.info(f"【微信】通知用户: {username}成功, 通知内容:{message}")
    else:
        logger.warning(f"【微信】找不到通知联系人:{username}")

    d.app_stop('com.tencent.mm')