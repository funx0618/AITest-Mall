# Mall 项目自动化测试开发规范

## UI 自动化断言（强制）
- **UI 测试统一使用 `expect`**，禁止使用 `assert`
- 等待：`expect(locator).to_be_visible()` / `.to_be_enabled()` / `.to_have_url()`
- 断言：`expect(locator).to_contain_text()` / `.to_have_attribute()` / `.to_be_visible()`

## API 自动化断言（强制）
- **API 测试统一使用 `assert`**，禁止使用 `expect`
- 示例：`assert response.status_code == 200`
- 示例：`assert response.json()["code"] == 200`

## UI 自动化等待策略（强制）
- **禁止使用** `wait_for`、`wait_for_timeout`、`time.sleep`
- **统一使用 `expect`** 进行等待：
  - `expect(locator).to_be_visible(timeout)` — 等待元素可见
  - `expect(locator).to_be_enabled(timeout)` — 等待元素可交互（搜索/重置等点击操作后）
  - `expect(page).to_have_url()` — 等待页面导航完成
  - `expect(locator).to_contain_text()` — 等待文本内容出现

## 断言风格（强制）
- **禁止使用** `assert` 进行 Playwright 断言
- **统一使用 `expect`**：
  - `expect(locator).to_contain_text("xxx")` — 验证元素文本
  - `expect(locator).to_have_attribute("type", "text")` — 验证元素属性
  - `expect(page).to_have_url()` — 验证 URL
  - `expect(locator).to_be_visible()` — 验证元素可见性

## 代码结构
- **Page Object Model**：`ui/pages/` 存放页面对象（元素定位 + 基础交互）
- **业务流程**：`ui/flows/` 存放业务流程封装
- **测试用例**：`tests/ui/` 存放测试用例

## 常用定位器
- Element UI 错误提示：`.el-message--error`
- Element UI 成功提示：`.el-message--success`
- Element UI 表格数据行：`table` → 过滤含 `td` 的行

## 元素定位优先级（强制）
按以下顺序选择定位器，优先使用靠前的方式：
1. `get_by_role` / `get_by_label`
2. `:has()` 伪选择器
3. `name` / `placeholder`
4. `class`

## 登录凭据
- 用户名：`funx`，密码：`123456`
