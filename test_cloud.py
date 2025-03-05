import time
import uiautomator2 as u2
from datetime import datetime
import logging
import os

class TestCloud:
    def setup_class(self):
        self.d = u2.connect("")
        # 创建截图保存目录
        os.makedirs("d:\\PycharmProjects\\pythonProject2\\error_screenshots", exist_ok=True)
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
        # 处理首页推送弹窗
        if self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/dialog_home_notice_image_close"]').exists:
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/dialog_home_notice_image_close"]').click()      
        if self.d.xpath('//android.widget.FrameLayout[2]').exists:
            self.d.click(0.905, 0.966)

    def test_cloud_game(self):
        try:
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动好游快爆")
            self.d.app_start("com.xmcy.hykb")
            self.d.wait_activity(".main.MainActivity", timeout=10)    
            # 处理弹窗
            start_time = time.time()
            while time.time() - start_time < 30:
                self.handle_popups()
                time.sleep(1)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动完成，弹窗处理结束")
            
            # 点击首页的"我的"按钮
            time.sleep(3)  # 增加等待时间，确保页面完全加载
            if self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').exists:
                self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').click()
            elif self.d(text="我的").exists:
                self.d(text="我的").click()
            else:
                # 如果都找不到，尝试通过坐标点击（根据实际坐标调整）
                self.d.click(0.9, 0.95)
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 通过坐标点击'我的'按钮")
                
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
            phone_input.set_text("383938391060")
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
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 未找到验证码输入框")
                return
            
            # 等待登录完成
            time.sleep(3)
            
            # 验证登录结果
            assert self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/nickname"]').exists, "登录失败"
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 登录成功！")
            time.sleep(2)
            if self.d.xpath('//*[@text="我知道了"]').exists:
                self.d.xpath('//*[@text="我知道了"]').click()
            time.sleep(3)
            # 点击进入我的收藏
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击进入我的收藏...")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/core_function_view"]/androidx.recyclerview.widget.RecyclerView[1]/android.view.ViewGroup[3]/android.widget.ImageView[1]').click()
            time.sleep(2)
            # 启动手游《原神》s6_8
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始启动手游《原神》s6_8...")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[5]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
            time.sleep(2)
            #处理可能遇到的温馨提示弹窗
            if self.d(resourceId="com.xmcy.hykb:id/left_button").exists:
                 self.d(resourceId="com.xmcy.hykb:id/left_button").click()
            if self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').exists:
                self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').click()               
            # 等待插件加载并启动游戏
            if self.d(resourceId="com.xmcy.hykb:id/cloud_game_start_tv").exists(timeout=60):
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载成功")
                # 重启应用
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 重启快爆应用...")
            self.d.app_stop("com.xmcy.hykb")
            time.sleep(1)
            self.d.app_start("com.xmcy.hykb")
            self.d.wait_activity(".main.MainActivity", timeout=10)           
            # 处理弹窗
            start_time = time.time()
            while time.time() - start_time < 30:
                self.handle_popups()
                time.sleep(1)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 重启完成，弹窗处理结束")
            # 点击首页的"我的"按钮
            time.sleep(3)  # 增加等待时间，确保页面完全加载
            if self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').exists:
                self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').click()
            elif self.d(text="我的").exists:
                self.d(text="我的").click()
            else:
                # 如果都找不到，尝试通过坐标点击（根据实际坐标调整）
                self.d.click(0.9, 0.95)
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 通过坐标点击'我的'按钮")

            # 点击进入我的收藏
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击进入我的收藏...")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/core_function_view"]/androidx.recyclerview.widget.RecyclerView[1]/android.view.ViewGroup[3]/android.widget.ImageView[1]').click()
            time.sleep(2)
            # 启动手游《原神》s6_8
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始启动手游《原神》s6_8...")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[5]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
            time.sleep(2)
            #处理可能遇到的温馨提示弹窗
            if self.d(resourceId="com.xmcy.hykb:id/left_button").exists:
                 self.d(resourceId="com.xmcy.hykb:id/left_button").click()
            if self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').exists:
                self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').click()               
            # 等待插件加载并启动游戏
            if self.d(resourceId="com.xmcy.hykb:id/cloud_game_start_tv").exists(timeout=60):
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件更新成功，开始启动游戏...")
                #点击开始云玩
                time.sleep(2)
                self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/cloud_game_start_tv"]').click()
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击开始云玩")
                # 检查是否进入云玩成功
                if self.d(resourceId="com.hykb.yuanshenmap:id/ping_view").exists(timeout=60):
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 成功进入云玩")
                    time.sleep(2)
                    # 使用系统返回按钮退出
                    self.d.press("back")
                    time.sleep(1)
                    self.d(resourceId="com.hykb.yuanshenmap:id/cloud_game_dialog_right_tv").click()
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 游戏已退出")
                else:
                    # 添加截图
                    screenshot_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                    self.d.screenshot(f"d:\\PycharmProjects\\pythonProject2\\error_screenshots\\cloud_game_fail_{screenshot_time}.png")
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进入云玩失败")
            else:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载失败")

            # 启动手游《蛋仔》s1_h8
            time.sleep(2)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始启动手游《蛋仔》s1_h8...")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[3]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
            time.sleep(2)
            #处理可能遇到的温馨提示弹窗
            if self.d(resourceId="com.xmcy.hykb:id/left_button").exists:
                 self.d(resourceId="com.xmcy.hykb:id/left_button").click()
            if self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').exists:
                self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').click()               
            # 等待插件加载并启动游戏
            if self.d(resourceId="com.xmcy.hykb:id/cloud_game_start_tv").exists(timeout=60):
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载成功，开始启动游戏...")
                #点击开始云玩
                time.sleep(2)
                self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/cloud_game_start_tv"]').click()
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击开始云玩")
                # 检查是否进入云玩成功
                if self.d(resourceId="com.hykb.yuanshenmap:id/ping_view").exists(timeout=60):
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 成功进入云玩")
                    time.sleep(2)
                    # 使用系统返回按钮退出
                    self.d.press("back")
                    time.sleep(1)
                    self.d(resourceId="com.hykb.yuanshenmap:id/cloud_game_dialog_right_tv").click()
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 游戏已退出")
                else:
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进入云玩失败")
            else:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载失败")
                # 启动手游《王者荣耀》s7_8
            time.sleep(2)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始动手游《王者荣耀》s7_8...")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
            time.sleep(2)
            #处理可能遇到的温馨提示弹窗
            if self.d(resourceId="com.xmcy.hykb:id/left_button").exists:
                 self.d(resourceId="com.xmcy.hykb:id/left_button").click()
            if self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').exists:
                self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').click()               
            # 等待插件加载并启动游戏
            if self.d(resourceId="com.xmcy.hykb:id/cloud_game_start_tv").exists(timeout=60):
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载成功，开始启动游戏...")
                #点击开始云玩
                time.sleep(2)
                self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/cloud_game_start_tv"]').click()
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击开始云玩")
                # 检查是否进入云玩成功
                if self.d(resourceId="com.hykb.yuanshenmap:id/tv_download_btw").exists(timeout=60):
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 成功进入云玩")
                    time.sleep(3)
                    # 使用系统返回按钮退出
                    self.d.press("back")
                    time.sleep(1)
                    self.d.press("back")
                    time.sleep(1)
                    self.d(resourceId="com.hykb.yuanshenmap:id/cloud_game_dialog_right_tv").click()
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 游戏已退出")
                else:
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进入云玩失败")
            else:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载失败")
                # 启动页游《黄金矿工-页游》s4_1
            time.sleep(2)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始启动页游《黄金矿工-页游》s4_1...")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
            time.sleep(2)
            #处理可能遇到的温馨提示弹窗
            if self.d(resourceId="com.xmcy.hykb:id/left_button").exists:
                 self.d(resourceId="com.xmcy.hykb:id/left_button").click()
            if self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').exists:
                self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').click()               
            # 等待插件加载并启动游戏
            if self.d(resourceId="com.xmcy.hykb:id/cloud_game_start_tv").exists(timeout=60):
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载成功，开始启动游戏...")
                #点击开始云玩
                time.sleep(2)
                self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/cloud_game_start_tv"]').click()
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击开始云玩")
                # 检查是否进入云玩成功
                if self.d(resourceId="com.hykb.yuanshenmap:id/ping_view").exists(timeout=60):
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 成功进入云玩")
                    time.sleep(2)
                    # 使用系统返回按钮退出
                    self.d.press("back")
                    time.sleep(1)
                    self.d(resourceId="com.hykb.yuanshenmap:id/cloud_game_dialog_right_tv").click()
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 游戏已退出")
                else:
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进入云玩失败")
            else:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载失败")
                # 启动端游《骑马与砍杀》s4_20
            time.sleep(2)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始动端游《骑马与砍杀》s4_20...")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
            time.sleep(2)
            #处理可能遇到的温馨提示弹窗
            if self.d(resourceId="com.xmcy.hykb:id/left_button").exists:
                 self.d(resourceId="com.xmcy.hykb:id/left_button").click()
            if self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').exists:
                self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').click()                
            # 等待插件加载并启动游戏
            if self.d(resourceId="com.xmcy.hykb:id/cloud_game_start_tv").exists(timeout=60):
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载成功，开始启动游戏...")
                #点击开始云玩
                time.sleep(2)
                self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/cloud_game_start_tv"]').click()
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击开始云玩")
                # 检查是否进入云玩成功
                if self.d(resourceId="com.hykb.yuanshenmap:id/ping_view").exists(timeout=60):
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 成功进入云玩")
                    time.sleep(2)
                    # 使用系统返回按钮退出
                    self.d.press("back")
                    time.sleep(1)
                    self.d(resourceId="com.hykb.yuanshenmap:id/cloud_game_dialog_right_tv").click()
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 游戏已退出")
                else:
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进入云玩失败")
            else:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载失败")
            
        finally:
            # 清理数据
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始清除应用数据...")
            try:
                # 先停止应用
                self.d.app_stop("com.xmcy.hykb")
                time.sleep(2)
                # 尝试清除数据
                self.d.app_clear("com.xmcy.hykb")
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 应用数据已清除")
            except Exception as e:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 清除应用数据失败: {str(e)}")
                # 尝试使用 shell 命令清除
                try:
                    self.d.shell(['pm', 'clear', 'com.xmcy.hykb'])
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 通过shell命令清除应用数据成功")
                except Exception as e:
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] shell命令清除应用数据也失败: {str(e)}")
