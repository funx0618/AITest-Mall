"""
App Tab Bar Component Object
组件：uni-app 底部导航栏（uni-tabbar）
职责：封装底部 tab 切换操作，供多个 Page Object 复用
"""

from playwright.sync_api import Page, expect


class AppTabBar:
    """App 底部导航栏组件对象

    定位策略：优先定位用户实际操作的交互容器（.uni-tabbar__item），
    而不是只定位显示文字的叶子节点（.uni-tabbar__label）。
    """

    def __init__(self, page: Page):
        self.page = page
        self.tabbar = page.locator(".uni-tabbar")
        self._home_tab = self.tabbar.locator(".uni-tabbar__item").filter(has_text="首页")
        self._cart_tab = self.tabbar.locator(".uni-tabbar__item").filter(has_text="购物车")
        self._my_tab = self.tabbar.locator(".uni-tabbar__item").filter(has_text="我的")

    def _is_visible(self) -> bool:
        """检查 tabbar 是否可见（非 hidden）"""
        try:
            return self.tabbar.is_visible()
        except Exception:
            return False

    def click_home(self):
        """点击首页 tab"""
        self._home_tab.click()
        return self

    def click_cart(self):
        """点击购物车 tab"""
        self._cart_tab.click()
        return self

    def click_my(self):
        """点击我的 tab"""
        self._my_tab.click()
        return self

    def go_back(self):
        """点击页面左上角返回箭头（非 tabbar 页面才有）"""
        back_btn = self.page.locator("uni-page-head .uni-page-head-btn")
        if back_btn.count() > 0 and back_btn.is_visible():
            back_btn.click()
        else:
            # 无返回按钮时用浏览器后退
            self.page.go_back()
        return self

    def back_to_tabbar(self, max_retries: int = 5):
        """连续点击返回箭头，直到 tabbar 可见（回到 tabbar 页面）"""
        for _ in range(max_retries):
            if self._is_visible():
                return self
            self.go_back()
            self.page.wait_for_timeout(500)
        return self
