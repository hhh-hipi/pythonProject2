import time
import uiautomator2 as u2
from datetime import datetime

d = u2.connect("192.168.31.232:40375")
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
    # 处理可能首页弹窗
    if d.xpath('//*[@resource-id="com.xmcy.hykb:id/dialog_home_notice_image_close"]').exists:
        d.xpath('//*[@resource-id="com.xmcy.hykb:id/dialog_home_notice_image_close"]').click()

# 执行登录操作
def login():
    # 点击首页的"我的"按钮
    if d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').exists:
        d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').click()
    else:
        d(text="我的").click()
        
    time.sleep(1)
    # 点击登录/注册按钮
    d(text="登录/注册").click()
    time.sleep(1)

    #选择泰国地区号码登录
    d.xpath('//*[@resource-id="com.xmcy.hykb:id/login_area_tv"]').click()
    d.xpath('//*[@resource-id="com.xmcy.hykb:id/area_phone_recycler"]/android.widget.FrameLayout[8]').click()

    # 输入固定手机号
    phone_input = d.xpath('//*[@resource-id="com.xmcy.hykb:id/phone_input_login_et_phone_number"]')
    phone_input.set_text("")  # 清除文本
    phone_input.set_text("383938391006")
    time.sleep(3)
    # 点击获取验证码按钮
    d.xpath('//*[@resource-id="com.xmcy.hykb:id/tv_get_verification_code"]').click()
    # 点击同意用户协议
    time.sleep(2)
    d.xpath('//*[@resource-id="com.xmcy.hykb:id/bt_agree"]').click()
    
    # 等待验证码输入框出现并输入
    d.xpath('//*[@resource-id="com.xmcy.hykb:id/verify_code_edit"]').wait(timeout=5)  # 添加等待
    code_input = d.xpath('//*[@resource-id="com.xmcy.hykb:id/verify_code_edit"]')
    if code_input.exists:  # 添加存在性检查
        code_input.set_text("")
        code_input.set_text("123456")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 未找到验证码输入框")
        return
    
    # 等待登录完成
    time.sleep(3)
    
    # 验证是否登录成功
    if d.xpath('//*[@resource-id="com.xmcy.hykb:id/nickname"]').exists:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 登录成功！")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 登录可能失败，请检查验证码是否正确")


# 循环检查并处理弹窗，持续10秒
start_time = time.time()
while time.time() - start_time < 10:
    handle_popups()
    time.sleep(1)
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动完成，弹窗处理结束")
login()
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始清除应用数据...")
d.app_clear("com.xmcy.hykb")
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 应用数据已清除")