# pymysql 查询读取旧数据（事务快照问题）

## 出现位置

API 自动化

## 遇到的问题

在 `tests/api/admin/flow_tests/test_product_category_flow.py` 的 `test_create_category_hidden` 用例中：
通过/productCategory/update/navStatus api 将nav_status由0更新为1后，
验证在表中是否将数nav_status更新成功，但sql查询到的还是为0，导致测试用例一直失败，
但/productCategory/list/ 中返回的nav_status为1
且这个2个api用的都是同一个表pms_product_category

上面的问题出现后让AI去分析原因

AI 排查过程：
navStatus 这个api有bug？更新了缓存但未写入数据库
饶过这个bug，用/productCategory/list/ 去验证是否更新成功
更新代码后运行时又出现了另一个问题，用/productCategory/delete/{id} 删除新增的商品分类，api返回成功了，但数据库中还是可以查到api删除的商品分类
上面的2个问题都是API 返回成功但未落库，猜测DB事务提交延迟导致测试中立即查询时记录还在


## 问题说明

在同一个测试用例中，API 调用成功后立即通过 DB 验证数据变更，但 `SELECT` 查询返回的仍是旧值。手动在 MySQL 客户端查询时数据已更新。

## 原因

`pymysql` 默认 `autocommit=False`，MySQL 默认隔离级别为 `REPEATABLE READ`。同一连接内所有 `SELECT` 读取的是第一次查询时建立的快照，无法看到后续 API 操作带来的数据库变更。

## 解决方案

在 `DBClient` 创建连接时添加 `autocommit=True`：

```python
self._conn = pymysql.connect(
    **DB_CONFIG,
    cursorclass=DictCursor,
    charset="utf8mb4",
    autocommit=True,  # 关键：每条 SQL 独立提交，避免读旧快照
)
```

**涉及文件**：`utils/db/db_client.py`、`tests/api/admin/flow_tests/test_product_category_flow.py`
