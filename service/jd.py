import time

from service.device import open_device
from loguru import logger

from service.wechat import notify_user

logger = logger.bind(module="jd")


def monitor_product(product_name, wechat_username):
    """
        商品监控
    """
    d = open_device()

    d.app_stop('com.jingdong.app.mall')
    # 打开fish
    d.app_start('com.jingdong.app.mall')

    time.sleep(5)
    my_ele = d.xpath('//*[@text="我的"]')
    if my_ele.exists:
        my_ele.click()
        logger.info("【京东】点击我的")
    else:
        logger.warning("【京东】点击我的，失败")
        return

    time.sleep(1)
    favor_product_ele = d.xpath('//*[@text="商品收藏"]')

    if favor_product_ele.exists:
        favor_product_ele.click()
        logger.info("【京东】点击商品收藏")

    else:
        logger.warning("【京东】点击商品收藏，失败")
        return
    time.sleep(1)
    for i in range(4):
        index = i + 1
        # 商品名称
        product_text_ele = d.xpath(f'//*[@resource-id="com.jd.lib.favourites.feature:id/cy"]'
                                   f'/android.widget.RelativeLayout[{index}]'
                                   '/android.widget.RelativeLayout[1]'
                                   '/android.widget.TextView[1]')

        if product_text_ele.exists and product_text_ele.info.get(
                'text') is not None and product_name in product_text_ele.info.get('text'):
            # 开始监听
            logger.info(f"【京东】检索到监听商品: {product_name} ")

            cart_ele = d.xpath(f'//*[@resource-id="com.jd.lib.favourites.feature:id/cy"]'
                               f'/android.widget.RelativeLayout[{index}]'
                               f'/android.widget.RelativeLayout[1]'
                               f'/android.widget.RelativeLayout[2]'
                               f'/android.widget.ImageView[1]')
            if cart_ele.exists:
                # 获取价格
                price_ele = d.xpath(f'//*[@resource-id="com.jd.lib.favourites.feature:id/cy"]'
                                    f'/android.widget.RelativeLayout[{index}]'
                                    f'/android.widget.RelativeLayout[1]'
                                    f'/android.widget.TextView[2]')
                # 通知
                price_text = price_ele.info.get('text')
                if '¥' in price_text:
                    # 微信通知指定用户
                    message = f'【京东】您订阅的商品:{product_name}已上架, 价格:{price_text} \n\n本消息由星辰Robot自动发送, 请勿直接回复!'
                    notify_user(wechat_username, message)
                    logger.info(f"【京东】商品:{product_name}已上架, 价格:{price_text}, 通知用户:{wechat_username}成功")
                else:

                    message = f'【京东】您订阅的商品:{product_name}已上架, 价格未知 \n\n本消息由星辰Robot自动发送, 请勿直接回复!'
                    notify_user(wechat_username, message)
                    logger.info(f"【京东】商品:{product_name}已上架, 价格未知, 通知用户:{wechat_username}成功")

            else:
                logger.info(f"【京东】商品:{product_name}, 暂时无货")

    # 关闭 app
    d.app_stop('com.jingdong.app.mall')