# 系统接口调用顺序

## 概述

本文档描述 Mall 系统各业务场景中接口的调用顺序和依赖关系，用于指导 API 自动化测试的编写。

## 1. 认证流程

```
┌─────────┐  POST /api/login   ┌─────────┐  返回 Token  ┌─────────┐
│  客户端  │ ────────────────→ │  服务端  │ ──────────→ │  客户端  │
└─────────┘                   └─────────┘              └─────────┘
                                    │
                                    │ 后续请求携带 Token
                                    ↓
                              Authorization: Bearer <token>
```

**接口调用顺序：**

```
1. POST /api/login          → 登录获取 Token
2. GET  /api/user/info      → 获取当前用户信息（验证 Token）
```

## 2. 用户管理接口

### 2.1 用户列表查询

```
1. POST /api/login                → 登录
2. GET  /api/user/list            → 获取用户列表
   └── 参数：page, pageSize, keyword（可选）
```

### 2.2 新增用户

```
1. POST /api/login                → 登录
2. POST /api/user/create          → 创建用户
   └── Body：{ username, password, role, ... }
3. GET  /api/user/list            → 验证用户已创建
```

### 2.3 编辑用户

```
1. POST /api/login                → 登录
2. GET  /api/user/list            → 获取用户 ID
3. PUT  /api/user/update/{id}     → 更新用户信息
   └── Body：{ username, role, ... }
4. GET  /api/user/detail/{id}     → 验证更新结果
```

### 2.4 删除用户

```
1. POST /api/login                → 登录
2. GET  /api/user/list            → 获取用户 ID
3. DELETE /api/user/delete/{id}   → 删除用户
4. GET  /api/user/list            → 验证用户已删除
```

## 3. 商品管理接口

### 3.1 商品列表

```
1. POST /api/login                → 登录
2. GET  /api/product/list         → 获取商品列表
   └── 参数：page, pageSize, category, keyword
```

### 3.2 商品详情

```
1. GET  /api/product/detail/{id}  → 获取商品详情
```

### 3.3 商品 CRUD（管理员）

```
1. POST /api/login                → 管理员登录
2. POST /api/product/create       → 创建商品
3. PUT  /api/product/update/{id}  → 更新商品
4. DELETE /api/product/delete/{id}→ 删除商品
```

## 4. 购物流程接口

```
1. POST /api/login                        → 登录
2. POST /api/cart/add                     → 添加商品到购物车
   └── Body：{ productId, quantity }
3. GET  /api/cart/list                    → 查看购物车
4. PUT  /api/cart/update/{id}             → 修改数量
   └── Body：{ quantity }
5. POST /api/order/create                 → 创建订单
   └── Body：{ cartIds, addressId }
6. POST /api/pay/create/{orderId}         → 发起支付
7. GET  /api/order/detail/{orderId}       → 查询订单状态
```

## 5. 订单管理接口

### 5.1 订单列表

```
1. POST /api/login                → 登录
2. GET  /api/order/list           → 获取订单列表
   └── 参数：page, pageSize, status
```

### 5.2 订单状态流转

```
1. POST /api/login                → 登录
2. GET  /api/order/detail/{id}    → 查看当前状态
3. POST /api/order/pay/{id}       → 支付（待支付 → 已支付）
4. POST /api/order/ship/{id}      → 发货（已支付 → 已发货）
5. POST /api/order/confirm/{id}   → 确认收货（已发货 → 已完成）
```

### 5.3 订单取消

```
1. POST /api/login                → 登录
2. POST /api/order/cancel/{id}    → 取消订单（待支付 → 已取消）
```

## 6. 接口依赖关系图

```
登录 (POST /login)
 ├── 用户管理
 │    ├── GET /user/list
 │    ├── POST /user/create
 │    ├── PUT /user/update/{id}
 │    └── DELETE /user/delete/{id}
 ├── 商品管理
 │    ├── GET /product/list
 │    ├── POST /product/create
 │    └── PUT /product/update/{id}
 ├── 购物流程
 │    ├── POST /cart/add
 │    ├── GET /cart/list
 │    └── POST /order/create
 └── 订单管理
      ├── GET /order/list
      ├── POST /order/pay/{id}
      └── POST /order/cancel/{id}
```

## 7. 接口测试策略

| 层级 | 测试内容 | 说明 |
|------|---------|------|
| 单接口 | 请求参数校验 | 合法/非法参数、边界值 |
| 单接口 | 返回值校验 | 状态码、响应结构、字段值 |
| 流程接口 | 多接口串联 | 按业务顺序调用，验证数据一致性 |
| 异常场景 | 错误处理 | Token 过期、权限不足、资源不存在 |

> **注意：** 以上接口路径为示例，实际接口地址请参考系统 API 文档或项目 `api/` 目录下的接口封装代码。
