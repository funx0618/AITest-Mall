"""
角色用户端到端测试用例
测试目标：新增角色 → 分配菜单 → 新增用户 → 登录验证菜单权限
涉及页面：Admin http://localhost:8090
"""

import re
import pytest
from playwright.sync_api import Page, expect
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD
from ui.pages.admin.admin_login_page import LoginPage
from ui.flows.admin.role_flow import RoleFlow
from ui.flows.admin.admin_user_flow import AdminUserFlow
from utils.data_loader import load_yaml

# 加载测试数据
test_data = load_yaml("e2e/test_role_user_flow.yaml")


class TestRoleUserFlow:
    """角色 + 用户 + 菜单权限端到端测试"""

    def test_role_user_flow(self, admin_logged_in_page: Page, playwright):
        """完整流程：新增角色 → 分配营销菜单 → 新增用户 → 登录验证只有营销菜单"""
        data = test_data["test_role_user_flow"]
        role_name = data["role_name"]
        description = data["role_description"]
        menu_names = data["parent_menu_names"]
        resource_names = data["parent_resource_names"]
        username = data["username"]
        password = data["password"]
        nickname = data["nickname"]
        email = data["email"]
        expected_menus = data["expected_parent_menus"]
        not_expected_menus = data["not_expected_parent_menus"]

        # 使用conftest中的admin_logged_in_page fixture（已自动登录admin）
        admin_page = admin_logged_in_page
        login_page = LoginPage(admin_page)

        user_flow = AdminUserFlow(admin_page)
        role_flow = RoleFlow(admin_page)

        # ===== Step 1: 新增角色（如果已存在则先删除） =====
        existing_roles = role_flow.search_role(role_name)
        if existing_roles:
            role_flow.unassign_all_menus(role_name)
            role_flow.delete_role(role_name)
        role_flow.add_role(role_name, description)

        # ===== Step 2: 为角色分配营销菜单 =====
        role_flow.assign_menu(role_name, menu_names)

        # ===== Step 2.5: 为角色分配营销资源 =====
        role_flow.assign_resource(role_name, resource_names)

        # ===== Step 3: 新增用户（如果已存在则先删除） =====
        existing_users = user_flow.search_user(username)
        if existing_users:
            user_flow.delete_user(username)
        user_flow.add_user(username, password, nickname, email)

        # ===== Step 4: 为用户分配角色 =====
        user_flow.assign_role(username, role_name)

        # ===== Step 5: 用新用户重新登录 =====
        # 退出当前登录：点击右上角头像下拉箭头 → 点击退出
        admin_page.locator(".avatar-container .avatar-wrapper").click()
        admin_page.get_by_role("menuitem", name="退出").click()
        # 等待退出完成，回到登录页
        expect(admin_page).to_have_url(re.compile(r".*#/login"), timeout=10000)
        expect(login_page.username_input).to_be_visible(timeout=10000)
        expect(login_page.password_input).to_be_visible(timeout=5000)
        expect(login_page.login_btn).to_be_enabled(timeout=5000)
        login_page.login(username, password)
        # 等待登录结果
        expect(admin_page).to_have_url(re.compile(r".*#/home"), timeout=15000)

        # ===== Step 6: 验证左侧菜单只有营销模块 =====
        # 展开菜单：点击左上角三条横线图标展开侧边栏，等待菜单项文字出现
        hamburger = admin_page.locator('.hamburger-container')
        hamburger.click()
        # 等待侧边栏展开（菜单项出现文字）
        expect(admin_page.locator("div.el-sub-menu__title", has_text=expected_menus[0])).to_be_visible(timeout=5000)

        # 验证期望的菜单可见
        for menu_name in expected_menus:
            expect(admin_page.locator("div.el-sub-menu__title", has_text=menu_name)).to_be_visible(timeout=5000)

        # 验证不应出现的菜单不可见
        for menu_name in not_expected_menus:
            expect(admin_page.locator("div.el-sub-menu__title", has_text=menu_name)).to_be_hidden(timeout=5000)

        # ===== 清理：用默认账号重新登录，删除测试数据 =====
        # 退出当前登录：点击右上角头像下拉箭头 → 点击退出
        admin_page.locator(".avatar-container .avatar-wrapper").click()
        admin_page.get_by_role("menuitem", name="退出").click()
        expect(admin_page).to_have_url(re.compile(r".*#/login"), timeout=10000)
        expect(login_page.username_input).to_be_visible(timeout=10000)
        expect(login_page.password_input).to_be_visible(timeout=5000)
        expect(login_page.login_btn).to_be_enabled(timeout=5000)
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        # 等待登录完成，跳转到首页
        expect(admin_page).to_have_url(re.compile(r".*#/home"), timeout=15000)

        # 删除用户
        user_flow.delete_user(username)

        # 删除角色（会自动级联删除角色-菜单、角色-用户关系）
        role_flow.delete_role(role_name)

    def test_disabled_user_cannot_login(self, admin_logged_in_page: Page, playwright):
        """验证被禁用的用户无法登录系统"""
        data = test_data["test_disabled_user_cannot_login"]
        role_name = data["role_name"]
        username = data["username"]
        password = data["password"]
        nickname = data["nickname"]
        email = data["email"]

        admin_page = admin_logged_in_page
        login_page = LoginPage(admin_page)

        user_flow = AdminUserFlow(admin_page)
        role_flow = RoleFlow(admin_page)

        # ===== Step 0: 确保商品管理员角色存在 =====
        existing_roles = role_flow.search_role(role_name)
        if not existing_roles:
            role_flow.add_role(role_name, "拥有商品模块的菜单权限")
            role_flow.assign_menu(role_name, data["parent_menu_names"])
            role_flow.assign_resource(role_name, data["parent_resource_names"])

        # ===== Step 1: 新增禁用用户（如果已存在则先删除） =====
        existing_users = user_flow.search_user(username)
        if existing_users:
            user_flow.delete_user(username)
        # enabled=False 不起作用，后端 register 强制新建用户为启用状态
        user_flow.add_user(username, password, nickname, email)
        # 通过编辑将用户设为禁用
        user_flow.set_user_disabled(username)

        # ===== Step 2: 为用户分配商品管理员角色 =====
        user_flow.assign_role(username, role_name)

        # ===== Step 4: 验证该用户无法登录 =====
        # 退出当前 admin
        admin_page.locator(".avatar-container .avatar-wrapper").click()
        admin_page.get_by_role("menuitem", name="退出").click()
        expect(admin_page).to_have_url(re.compile(r".*#/login"), timeout=10000)
        expect(login_page.username_input).to_be_visible(timeout=10000)
        expect(login_page.password_input).to_be_visible(timeout=5000)
        expect(login_page.login_btn).to_be_enabled(timeout=5000)

        # 尝试用禁用账号登录
        login_page.login(username, password)
        # 应停留在登录页并显示错误提示（一闪而过，用组合定位器快速捕获）
        expect(admin_page).to_have_url(re.compile(r".*#/login"), timeout=10000)
        expect(login_page.error_message_containing("帐号已被禁用")).to_be_visible(timeout=5000)

        # ===== 清理：重新登录 admin，删除测试数据 =====
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        expect(admin_page).to_have_url(re.compile(r".*#/home"), timeout=15000)

        user_flow.delete_user(username)

    def test_role_switch(self, admin_logged_in_page: Page, playwright):
        """验证切换用户角色后菜单权限正确变化

        流程：
        1. 新增角色(订单管理员) + 分配菜单(订单) + 分配资源(订单列表)
        2. 新增用户，分配订单管理员角色
        3. 登录验证：只有订单下的订单列表子菜单
        4. 退出，将用户角色改为商品管理员
        5. 登录验证：有商品下的商品子菜单，没有订单下的订单列表
        """
        data = test_data["test_role_switch"]
        role_name = data["role_name"]
        role_description = data["role_description"]
        menu_names = data["sub_menu_names"]
        menu_expand_parents = data.get("parent_menu_names", [])
        resource_names = data["sub_resource_names"]
        username = data["username"]
        password = data["password"]
        nickname = data["nickname"]
        email = data["email"]
        new_role_name = data["new_role_name"]
        expected_visible_menus = data["expected_visible_menus"]
        not_expected_visible_menus = data["not_expected_visible_menus"]

        admin_page = admin_logged_in_page
        login_page = LoginPage(admin_page)

        user_flow = AdminUserFlow(admin_page)
        role_flow = RoleFlow(admin_page)

        # ===== Step 0: 确保商品管理员角色存在（Step 5 切换角色时需要） =====
        existing_product_roles = role_flow.search_role(new_role_name)
        if not existing_product_roles:
            role_flow.add_role(new_role_name, "拥有商品模块的菜单权限")
            role_flow.assign_menu(new_role_name, data["new_role_parent_menu_names"])
            role_flow.assign_resource(new_role_name, data["new_role_parent_resource_names"])

        # ===== Step 1: 新增订单管理员角色（如果已存在则先删除） =====
        existing_roles = role_flow.search_role(role_name)
        if existing_roles:
            role_flow.unassign_all_menus(role_name)
            role_flow.delete_role(role_name)
        role_flow.add_role(role_name, role_description)

        # ===== Step 2: 分配订单菜单和资源 =====
        role_flow.assign_menu(role_name, menu_names, expand_only=menu_expand_parents)
        role_flow.assign_resource(role_name, resource_names)

        # ===== Step 3: 新增用户并分配订单管理员角色 =====
        existing_users = user_flow.search_user(username)
        if existing_users:
            user_flow.delete_user(username)
        user_flow.add_user(username, password, nickname, email)
        user_flow.assign_role(username, role_name)

        # ===== Step 4: 登录验证只有订单菜单 =====
        admin_page.locator(".avatar-container .avatar-wrapper").click()
        admin_page.get_by_role("menuitem", name="退出").click()
        expect(admin_page).to_have_url(re.compile(r".*#/login"), timeout=10000)
        expect(login_page.username_input).to_be_visible(timeout=10000)
        expect(login_page.password_input).to_be_visible(timeout=5000)
        expect(login_page.login_btn).to_be_enabled(timeout=5000)
        login_page.login(username, password)
        expect(admin_page).to_have_url(re.compile(r".*#/home"), timeout=20000)

        # 展开侧边栏
        admin_page.locator('.hamburger-container').click()
        # 只分配了子菜单，侧边栏直接显示子菜单项
        for menu_name in expected_visible_menus:
            expect(admin_page.locator("li.el-menu-item", has_text=menu_name)).to_be_visible(timeout=5000)

        # 验证不应出现的菜单不可见
        for menu_name in not_expected_visible_menus:
            expect(admin_page.locator("div.el-sub-menu__title", has_text=menu_name)).to_be_hidden(timeout=5000)

        # ===== Step 5: 退出，将用户角色改为商品管理员 =====
        admin_page.locator(".avatar-container .avatar-wrapper").click()
        admin_page.get_by_role("menuitem", name="退出").click()
        expect(admin_page).to_have_url(re.compile(r".*#/login"), timeout=10000)
        expect(login_page.username_input).to_be_visible(timeout=10000)
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        expect(admin_page).to_have_url(re.compile(r".*#/home"), timeout=15000)

        user_flow.admin_page.goto()
        user_flow.assign_role(username, new_role_name)

        # ===== Step 6: 登录验证菜单已切换 =====
        admin_page.locator(".avatar-container .avatar-wrapper").click()
        admin_page.get_by_role("menuitem", name="退出").click()
        expect(admin_page).to_have_url(re.compile(r".*#/login"), timeout=10000)
        expect(login_page.username_input).to_be_visible(timeout=10000)
        expect(login_page.password_input).to_be_visible(timeout=5000)
        expect(login_page.login_btn).to_be_enabled(timeout=5000)
        login_page.login(username, password)
        expect(admin_page).to_have_url(re.compile(r".*#/home"), timeout=15000)

        # 展开侧边栏
        admin_page.locator('.hamburger-container').click()
        # 商品管理员分配的是父菜单「商品」，侧边栏显示父菜单
        expect(admin_page.locator("div.el-sub-menu__title", has_text="商品")).to_be_visible(timeout=5000)

        # 验证商品下的商品子菜单可见
        product_menu = admin_page.locator("div.el-sub-menu__title", has_text="商品")
        product_menu.click()
        expect(admin_page.get_by_role("link", name="商品列表")).to_be_visible(timeout=5000)

        # 验证订单列表不可见（已切换到商品管理员，不再有订单权限）
        expect(admin_page.locator("li.el-menu-item", has_text="订单列表")).to_be_hidden(timeout=5000)

        # ===== 清理 =====
        admin_page.locator(".avatar-container .avatar-wrapper").click()
        admin_page.get_by_role("menuitem", name="退出").click()
        expect(admin_page).to_have_url(re.compile(r".*#/login"), timeout=10000)
        expect(login_page.username_input).to_be_visible(timeout=10000)
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        expect(admin_page).to_have_url(re.compile(r".*#/home"), timeout=15000)

        user_flow.delete_user(username)
        role_flow.delete_role(role_name)
