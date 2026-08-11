# Pytest Fixture 无法复用于测试清理段重新登录

## 问题描述

在 E2E 测试 `test_role_user_flow.py` 中，测试流程需要：

1. 以 admin 身份登录（通过 `admin_logged_in_page` fixture）
2. 执行业务操作（新增角色、分配菜单、新增用户等）
3. 退出 admin，以测试用户身份登录，验证菜单权限
4. **清理阶段**：退出测试用户，重新以 admin 身份登录，删除测试数据

第 4 步的"重新以 admin 身份登录"希望能复用 `admin_logged_in_page` fixture，而不是直接调用 `login_page.login("admin", "macro123")`。

## 原因分析

### 1. Fixture 只解析一次并缓存

```python
def test_role_user_flow(self, admin_logged_in_page: Page, ...):
```

`admin_logged_in_page` 作为测试方法参数，pytest 在测试开始前**执行一次并缓存结果**。整个测试过程中返回的是**同一个 page 对象**。

### 2. 测试过程中 page 状态已被改变

```
开始 → admin登录(admin_page) → 退出 → 测试用户登录 → 验证菜单 → 退出
                                                                    ↑
                                                          page 现在停在登录页，不再是 admin 已登录状态
```

测试中途执行了退出登录、换用户登录、再次退出等操作，`admin_page`（即 `page`）的浏览器状态已经改变。

### 3. `request.getfixturevalue` 不会重新执行

```python
request.getfixturevalue('admin_logged_in_page')
# → 返回缓存的同一个 page 对象（停在登录页，未重新登录）
# → 后续 delete_user / delete_role 操作会失败
```

对于 **function-scoped** fixture，`getfixturevalue` 只返回已解析的缓存值，**不会重新执行 fixture 函数体**（即不会再调用 `login_page.goto()` + `login_page.login()`）。

## 解决方案

### 采用方案：清理段直接在同一 page 上重新登录，从 config 获取凭证

```python
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD

# 清理段：退出测试用户后，直接在同一 page 上重新登录 admin
login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
```

- ✅ 简单直接，复用同一个 page 对象
- ✅ 无额外浏览器开销
- ✅ 账号密码从 `config/settings.py` 统一管理，避免硬编码

### 备选方案：新建独立的清理用 fixture

```python
@pytest.fixture
def cleanup_admin_page(browser: Browser) -> Page:
    """清理用的独立 admin 登录页面"""
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
    expect(page).to_have_url(re.compile(r".*#/home"), timeout=15000)
    yield page
    context.close()
```

- ✅ 完全遵循 fixture 模式
- ❌ 打开新的浏览器窗口，增加额外开销
- ❌ 新 page 的上下文与测试中的 page 独立，操作对象不同

## 结论

**pytest function-scoped fixture 不支持在同一 page 上"重新执行"**，因此清理阶段需要退出后在同一 page 上重新登录，直接调用 `login_page.login()` 是最简单高效的方案。账号密码通过 `config.settings` 统一管理，避免硬编码。
