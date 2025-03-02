import time

import uiautomator2 as u2

d = u2.connect("192.168.31.232:40375")
# print(d.info)
d.app_start("com.xmcy.hykb")

# 等待应用启动，最多等待10秒，每0.5秒检查一次
d.wait_activity(".main.MainActivity", timeout=10)

def handle_popups():
    # 处理各种可能的弹窗按钮
    buttons = ["同意，进入使用","允许", "同意", "我知道了", "跳过", "关闭"]
    for button in buttons:
        if d(text=button).exists:
            d(text=button).click()
            time.sleep(0.5)
    
    # 处理可能的系统权限弹窗
    if d.xpath('//*[@text="允许"]').exists:
        d.xpath('//*[@text="允许"]').click()
    if d.xpath('//*[@text="始终允许"]').exists:
        d.xpath('//*[@text="始终允许"]').click()

# 循环检查并处理弹窗，持续10秒
start_time = time.time()
while time.time() - start_time < 10:
    handle_popups()
    time.sleep(1)

print("启动完成，弹窗处理结束")
