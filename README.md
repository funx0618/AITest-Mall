# Mall 自动化测试项目

基于 **Playwright + pytest** 的 Mall 电商系统自动化测试框架，覆盖 UI 自动化和 API 自动化两个维度。

---

## 项目结构

```
AITest-Mall/
├── api/                  # API Service 层（封装接口请求）
│   ├── admin/            #   后台管理接口
│   ├── app/              #   前台商城接口
│   └── clients/          #   通用请求客户端
│
├── ui/                   # UI 自动化层
│   ├── pages/            #   Page Object Model（页面对象）
│   │   ├── admin/        #     后台管理页面
│   │   └── app/          #     前台商城页面
│   └── flows/            #   业务流程层（组合页面操作）
│       ├── admin/        #     后台业务流程
│       └── app/          #     前台业务流程
│
├── tests/                # 测试用例
│   ├── ui/               #   UI 测试用例
│   └── api/              #   API 测试用例
│       ├── admin/        #     后台接口用例
│       └── app/          #     前台接口用例
│
├── data/                 # 测试数据
│   ├── api/              #   API 测试数据（YAML）
│   ├── ui/               #   UI 测试数据（YAML）
│   ├── e2e/              #   E2E 测试数据
│   └── sql/              #   SQL 脚本
│
├── config/               # 配置文件
├── utils/                # 工具类
├── docs/                 # 项目文档
├── conftest.py           # pytest 全局 fixture
├── pytest.ini            # pytest 配置
└── requirements.txt      # Python 依赖
```

---

## 技术栈

| 类别 | 技术 |
|------|------|
| 测试框架 | pytest 9.x |
| UI 自动化 | Playwright (Python) |
| API 测试 | Playwright request context |
| 测试报告 | Allure |
| 数据格式 | YAML |
| 数据库验证 | PyMySQL |
| 被测系统 | Mall（Spring Boot + Vue） |

---

## 环境准备

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
playwright install chromium
```

### 3. 启动被测服务

| 服务 | 地址 |
|------|------|
| 后台管理前端 | http://localhost:8090 |
| 前台商城前端 | http://localhost:8060 |
| 后台管理 API | http://localhost:8080 |
| 前台商城 API | http://localhost:8085 |
| MySQL 数据库 | localhost:3306 |

---

## 运行测试

```bash
# 运行全部 UI 测试
pytest tests/ui/ -v

# 运行单个 UI 测试文件
pytest tests/ui/test_coupon.py -v

# 运行单个测试用例
pytest tests/ui/test_coupon.py::TestCoupon::test_add_coupon_specified_claim -v

# 运行全部 API 测试
pytest tests/api/ -v

# 生成 Allure 报告
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

> 默认配置了 `--headed`（有头模式），可在 `pytest.ini` 中移除以切换为无头模式。

---

## 核心设计

### Page Object Model（三层架构）

```
tests/ui/test_xxx.py       ← 测试用例：编排测试步骤 + 断言
    ↓ 调用
ui/flows/admin/xxx_flow.py ← 业务流程：组合多个页面操作为完整业务场景
    ↓ 调用
ui/pages/admin/xxx_page.py ← 页面对象：元素定位 + 基础交互
```

- **Page**：只负责元素定位和基础操作（点击、输入、获取文本）
- **Flow**：组合多个 Page 操作，封装完整业务流程
- **Test**：调用 Flow + 添加断言验证

### UI 断言规范

- **统一使用 `expect`**，禁止使用 `assert`
- 等待：`expect(locator).to_be_visible()` / `.to_be_enabled()`
- 断言：`expect(locator).to_contain_text()` / `.to_have_attribute()`
- 禁止使用 `wait_for`、`wait_for_timeout`、`time.sleep`

### API 断言规范

- **统一使用 `assert`**，禁止使用 `expect`
- 示例：`assert response.status_code == 200`

### 测试数据管理

- 数据文件命名与测试文件一一对应（如 `test_coupon.yaml` ↔ `test_coupon.py`）
- YAML 中的 key 与测试方法名一致，通过 `load_yaml` 按方法名自动加载

---

## 环境配置

编辑 `config/settings.py` 修改环境参数：

```python
# 数据库
DB_CONFIG = {"host": "localhost", "port": 3306, ...}

# 后台管理
ADMIN_BASE_URL = "http://localhost:8090"
ADMIN_API_BASE_URL = "http://localhost:8080"

# 前台商城
WEB_BASE_URL = "http://localhost:8060"
APP_API_BASE_URL = "http://localhost:8085"
```

---

## 全局 Fixture（conftest.py）

| Fixture | 说明 |
|---------|------|
| `admin_logged_in_page` | 后台管理已登录的 Page |
| `app_logged_in` | 前台商城已登录的 Page（手机端视窗） |
| `admin_api_context` | 后台管理 API 请求上下文（已携带 token） |
| `app_token` | 前台商城 API token |
| `db` | MySQL 数据库连接 |
