import time
import uiautomator2 as u2
from datetime import datetime

class TestLogin:
    def setup_class(self):
        self.d = u2.connect("")
        
    def handle_popups(self):
        # 处理各种可能的弹窗按钮
        buttons = ["同意，进入使用","允许", "同意", "我知道了", "跳过", "关闭"]
        for button in buttons:
            if self.d(text=button).exists:
                self.d(text=button).click()
                time.sleep(0.5)
        
        # 处理可能的系统权限弹窗
        if self.d.xpath('//*[@text="允许"]').exists:
            self.d.xpath('//*[@text="允许"]').click()
        if self.d.xpath('//*[@text="始终允许"]').exists:
            self.d.xpath('//*[@text="始终允许"]').click()
        # 处理可能首页弹窗
        if self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/dialog_home_notice_image_close"]').exists:
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/dialog_home_notice_image_close"]').click()

    def test_login(self):
        try:
            self.d.app_start("com.xmcy.hykb")
            self.d.wait_activity(".main.MainActivity", timeout=10)
            
            # 处理弹窗
            start_time = time.time()
            while time.time() - start_time < 10:
                self.handle_popups()
                time.sleep(1)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动完成，弹窗处理结束")
            
            # 点击首页的"我的"按钮
            if self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').exists:
                self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').click()
            else:
                self.d(text="我的").click()
                
            time.sleep(1)
            # 点击登录/注册按钮
            self.d(text="登录/注册").click()
            time.sleep(1)

            # 选择泰国地区号码登录
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/login_area_tv"]').click()
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/area_phone_recycler"]/android.widget.FrameLayout[8]').click()
            time.sleep(2)
            # 输入固定手机号
            phone_input = self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/phone_input_login_et_phone_number"]')
            phone_input.set_text("")
            phone_input.set_text("383938391006")
            time.sleep(3)
            
            # 点击获取验证码按钮
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/tv_get_verification_code"]').click()
            time.sleep(2)
            
            # 点击同意用户协议
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/bt_agree"]').click()
            
            # 等待验证码输入框出现并输入
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/verify_code_edit"]').wait(timeout=5)
            code_input = self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/verify_code_edit"]')
            if code_input.exists:
                code_input.set_text("")
                code_input.set_text("123456")
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 未找到验证码输入框")
                return
            
            # 等待登录完成
            time.sleep(3)
            
            # 验证登录结果
            assert self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/nickname"]').exists, "登录失败"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 登录成功！")
            
        finally:
            # 清理数据
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始清除应用数据...")
            self.d.app_clear("com.xmcy.hykb")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 应用数据已清除")