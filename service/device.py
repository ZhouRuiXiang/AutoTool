import uiautomator2 as u2



def open_device():
    d = u2.connect('ERLDU19906009848')  # USB链接设备。或者u2.connect_usb('123456f')
    # d = u2.connect('9CN0223C27040310')  # USB链接设备。或者u2.connect_usb('123456f')
    # 唤醒屏幕
    d.screen_on()
    return d
