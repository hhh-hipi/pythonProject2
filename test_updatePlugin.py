import time
import uiautomator2 as u2
from datetime import datetime
import logging
import os


class TestCloud:

    def setup_class(self):
        """
            类初始化函数
        """
        self.d = u2.connect("")
        # 创建截图保存目录
        os.makedirs("error_screenshots", exist_ok=True)

    def handle_popups(self):
        """
            处理启动流程的各种弹窗
        """
        buttons = ["同意，进入使用", "允许", "同意", "我知道了", "跳过", "关闭"]
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


    def start_cloud_game(self, game_element):
        """
        启动云游戏并进行游戏测试
        Args:
            game_element: 游戏元素的xpath对象
        Returns:
            bool: 云游戏是否启动成功
        """
        try:
            # 点击云游戏
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击云玩启动按钮...")
            game_element.click()
            time.sleep(2)
            # 处理可能遇到的温馨提示弹窗
            if self.d(resourceId="com.xmcy.hykb:id/left_button").exists:
                self.d(resourceId="com.xmcy.hykb:id/left_button").click()
            if self.d.xpath(
                    '//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').exists:
                self.d.xpath(
                    '//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').click()
            # 等待插件加载并启动游戏
            if self.d(resourceId="com.xmcy.hykb:id/cloud_game_start_tv").wait(timeout=300):
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载成功，开始启动游戏")
                time.sleep(2)
                # 点击开始云玩
                self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/cloud_game_start_tv"]').click()
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击开始云玩")
                # 检测边玩边下按钮/云玩顶部带宽延迟元素判断是否进入云玩成功
                if self.d(resourceId="com.hykb.yuanshenmap:id/ping_view").wait(timeout=120):
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 成功进入云玩")
                    time.sleep(2)
                    # 使用系统返回按钮退出
                    self.d.press("back")
                    time.sleep(1)
                    self.d(resourceId="com.hykb.yuanshenmap:id/cloud_game_dialog_right_tv").click()
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 游戏已退出")
                    return True
                elif self.d(resourceId="com.hykb.yuanshenmap:id/tv_download_btw").wait(timeout=120):
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 成功进入云玩")
                    time.sleep(2)
                    # 使用系统返回按钮退出
                    self.d.press("back")
                    time.sleep(3)
                    self.d.press("back")
                    time.sleep(1)
                    self.d(resourceId="com.hykb.yuanshenmap:id/cloud_game_dialog_right_tv").click()
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 游戏已退出")
                    return True
                else:
                    # 添加截图
                    screenshot_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                    self.d.screenshot(f"error_screenshots/cloud_game_fail_{screenshot_time}进入云玩失败.png")
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进入云玩失败")
                    return False
            else:
                # 添加截图
                screenshot_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                self.d.screenshot(f"error_screenshots/cloud_game_fail_{screenshot_time}插件加载失败.png")
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载失败")
                return False

        except Exception as e:
            logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动云游戏过程发生异常: {str(e)}")
            return False

    def test_update_plugin(self):
        try:
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动好游快爆")
            self.d.app_start("com.xmcy.hykb")
            # 处理启动弹窗
            start_time = time.time()
            while time.time() - start_time < 30:
                self.handle_popups()
                time.sleep(1)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动完成，弹窗处理结束")
            time.sleep(2)
            self.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/recyclerview_homeindex_item_often_play"]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.ImageView[1]'))
            time.sleep(2)
            self.d.app_stop("com.xmcy.hykb")
            time.sleep(2)
            self.d.app_start("com.xmcy.hykb")
            # 处理启动弹窗
            start_time = time.time()
            while time.time() - start_time < 30:
                self.handle_popups()
                time.sleep(1)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动完成，弹窗处理结束")
            time.sleep(2)
            self.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/recyclerview_homeindex_item_often_play"]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.ImageView[1]'))

        finally:
            # 清理数据
            # logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始清除应用数据...")
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始卸载插件...")
            try:
                time.sleep(2)
                self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.view.ViewGroup[1]/android.widget.ImageView[1]').click()
                time.sleep(2)
                self.d(resourceId="com.xmcy.hykb:id/settings_icon").click()
                time.sleep(2)
                self.d(resourceId="com.xmcy.hykb:id/text_setting_download_install").click()
                time.sleep(2)
                self.d(resourceId="com.xmcy.hykb:id/cg_plugin").click()
                time.sleep(2)
                self.d(resourceId="com.xmcy.hykb:id/right_button").click()
                time.sleep(2)
                if (self.d(text="卸载云玩&地图工具组件").exists):
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 删除云玩插件失败")
                else:
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 云玩插件已卸载")
                time.sleep(2)
                # 先停止应用
                self.d.app_stop("com.xmcy.hykb")
                time.sleep(2)
                # # 尝试清除数据
                # self.d.app_clear("com.xmcy.hykb")
                # logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 应用数据已清除")
            except Exception as e:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 删除云玩插件失败: {str(e)}")
                self.d.app_stop("com.xmcy.hykb")
                time.sleep(2)
                # logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 清除应用数据失败: {str(e)}")
                # 尝试使用 shell 命令清除
                # try:
                #     self.d.shell(['pm', 'clear', 'com.xmcy.hykb'])
                #     logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 通过shell命令清除应用数据成功")
                # except Exception as e:
                #
                #     logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] shell命令清除应用数据也失败: {str(e)}")
