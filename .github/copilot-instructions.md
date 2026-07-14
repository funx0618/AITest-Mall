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

## API 自动化开发工作流（强制）

开发 API 自动化测试时，**必须遵循以下流程**：

### 1. 添加 API Service
- **路径**：`api/admin/` 或 `api/app/`（根据目标端选择）
- **格式**：参考 `api/admin/services/order_service.py`
- **职责**：封装 API 文档中同个 Controller 下的 API 请求方法

### 2. 生成测试数据
- **路径**：`data/api/`
- **命名规则**：测试数据文件名 **必须** 与对应测试用例文件名一致（如 `test_order_list.yaml`）
- **Key 规则**：YAML 中的 key **必须** 与测试方法名一致，以便按方法名自动加载对应测试数据

### 3. 编写测试用例
- **路径**：`tests/api/admin/` 或 `tests/api/app/`
  - `service_tests/` — 单个 API 接口用例
  - `flow_tests/` — 业务流程用例（跨多个接口的完整业务场景）
- **断言**：统一使用 `assert`（禁止 `expect`）

### 3.1 单接口用例验证规则（强制）
- **API 文档**：`docs/api docs/` 下有各模块的 API 说明文件（如 `order-api.md`、`admin-product-api.md`）
- **编写单个 API 用例前**：必须先阅读对应的 API 文档，获取该接口的参数定义和**涉及表**
- **验证范围**：`service_tests/` 中的用例必须按照 API 文档中列出的**涉及表**进行数据验证，确保接口操作的数据落库正确

### 4. 工具类
- **路径**：`utils/`（公共工具方法，如数据加载、请求封装等）

### 文件对应关系示意
```
docs/api docs/order-api.md         # API 文档（接口定义 + 涉及表）
api/admin/order_service.py         # Service 层（封装 API 请求，对应 api docs 中的 Controller）
data/api/test_order_list.yaml      # 测试数据
tests/api/admin/service_tests/
    test_order_list.py             # 单接口用例（按涉及表验证）
tests/api/admin/flow_tests/
    test_order_flow.py             # 业务流程用例
utils/data_loader.py               # 工具类
```
