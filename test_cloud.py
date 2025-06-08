import time
import uiautomator2 as u2
from datetime import datetime
import logging
from hykb_interface import HykbUtils

class TestCloud:

    def setup_class(self):
        """
            类初始化函数
        """
        self.hykb = HykbUtils("5bf8ee8e")
        self.d = self.hykb.d

    def test_cloud_game(self):
        try:
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动好游快爆")
            self.d.app_start("com.xmcy.hykb")   
            # 处理启动弹窗
            start_time = time.time()
            while time.time() - start_time < 30:
                self.hykb.handle_popups()
                time.sleep(1)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动完成，弹窗处理结束")
            #调用登录函数
            self.hykb.login()
            # 点击进入我的收藏
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击进入我的收藏")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/core_function_view"]/androidx.recyclerview.widget.RecyclerView[1]/android.view.ViewGroup[3]/android.widget.ImageView[1]').click()
            time.sleep(2)
            #调用云玩启动函数
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试手游《原神》S6线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
            time.sleep(3)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试手游《王者荣耀》S7线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[3]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
            time.sleep(3)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试手游《蛋仔派对》S1线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
            time.sleep(3)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试端游《骑马与砍杀》S4_20线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[5]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
            time.sleep(3)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试页游《黄金矿工-页游》S4_1线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[6]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
            time.sleep(3)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试高配《黑神话：悟空》S4_50线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))

        finally:
            # 清理数据
            self.hykb.clean_app_data("com.xmcy.hykb")

