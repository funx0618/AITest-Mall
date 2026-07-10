# 自动化框架设计

## 概述

本文档描述 Mall 项目的自动化测试框架架构设计，涵盖目录结构、分层模型、技术选型及核心约定。

## 技术栈

| 技术 | 用途 |
|------|------|
| Python | 测试脚本语言 |
| Playwright | UI 自动化 |
| Pytest | 测试运行器 |
| Requests | API 自动化 |
| PyYAML | 测试数据管理 |

## 框架分层

```
┌─────────────────────────────────┐
│         tests/                  │  测试用例层
│   ├── ui/                       │    UI 测试用例
│   ├── api/                      │    API 测试用例
│   └── e2e/                      │    端到端测试
├─────────────────────────────────┤
│         ui/flows/               │  业务流程层
│   └── admin_user_flow.py        │    封装完整业务流程
├─────────────────────────────────┤
│         ui/pages/               │  页面对象层（POM）
│   ├── login_page.py             │    登录页
│   └── admin_user_page.py        │    用户管理页
├─────────────────────────────────┤
│         api/                    │  接口封装层
├─────────────────────────────────┤
│         utils/                  │  工具层
│   └── data_loader.py            │    数据加载器
├─────────────────────────────────┤
│         data/ui/                │  测试数据层
│   └── test_user.yaml            │    用户测试数据
└─────────────────────────────────┘
```

## 目录结构

```
AITest-Mall/
├── conftest.py              # Pytest fixtures（浏览器、登录态等）
├── requirements.txt         # Python 依赖
├── config/
│   └── settings.py          # 全局配置（URL、超时等）
├── data/
│   └── ui/
│       └── test_user.yaml   # UI 测试数据
├── tests/
│   ├── ui/                  # UI 测试用例
│   ├── api/                 # API 测试用例
│   └── e2e/                 # 端到端测试
├── ui/
│   ├── pages/               # Page Object Model
│   └── flows/               # 业务流程封装
├── api/                     # 接口封装
└── utils/
    └── data_loader.py       # 通用工具
```

## 核心设计原则

### Page Object Model（POM）

- `ui/pages/`：每个页面一个类，封装元素定位和基础交互方法
- `ui/flows/`：组合多个页面对象，封装完整业务流程
- 测试用例只调用 flow 层方法，不直接操作 page 层

### 断言规范

| 场景 | 断言方式 | 说明 |
|------|---------|------|
| UI 测试 | `expect(locator)` | Playwright 原生断言 |
| API 测试 | `assert` | Python 原生断言 |

### 等待策略

- **禁止使用** `time.sleep`、`wait_for_timeout`
- **统一使用** `expect` 系列方法进行智能等待：
  - `expect(locator).to_be_visible(timeout)` — 等待元素可见
  - `expect(locator).to_be_enabled(timeout)` — 等待元素可交互
  - `expect(page).to_have_url()` — 等待页面导航

### 数据驱动

- 测试数据存放在 `data/` 目录，使用 YAML 格式
- 通过 `utils/data_loader.py` 统一加载

## 运行方式

```bash
# 运行全部 UI 测试
pytest tests/ui/ -v

# 运行全部 API 测试
pytest tests/api/ -v

# 运行指定测试文件
pytest tests/ui/test_login.py -v
```
