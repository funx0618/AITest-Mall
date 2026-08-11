# Element UI 表格空态导致等待/行读取失败

## 问题描述

Element UI 的 `el-table` 在无数据时，`tbody tr` 内包含带 placeholder `td` 的空态行，
导致以下三类问题：

1. `search()` 中 `wait_for(state='attached')` 在有数据/无数据时行为不一致
2. `get_row_data()` 访问空态行中不存在的列数据而失败
3. `get_all_rows()` 的过滤条件过松，包含空态行

## 影响文件

| 文件 | 影响方法 |
|------|----------|
| `ui/pages/admin/role_page.py` | `search()`, `get_row_data()`, `get_all_rows()` |
| `ui/pages/admin/admin_user_page.py` | `search()` |

## 修复方案

### search() — `expect(locator.or_(empty_hint))` 替换 `wait_for`

```python
# Before
self.user_table.locator('tbody tr').first.locator('td').first.wait_for(state='attached', timeout=10000)

# After
first_td = self.user_table.locator('tbody tr').first.locator('td').nth(4)
empty_hint = self.page.locator('.el-table__empty-text').first
expect(first_td.or_(empty_hint)).to_be_attached(timeout=10000)
```

使用 `.nth(4)` 而非 `.first`，确保匹配到的是真实数据行的第 5 列，而非空态 placeholder `td`。

### get_all_rows() — `count() >= 5` 排除空态行

```python
# Before
rows.filter(has=self.page.locator('td')).filter(
    lambda row: row.locator('td').count() > 0
)

# After
rows.filter(has=self.page.locator('td')).filter(
    lambda row: row.locator('td').count() >= 5
)
```

空态行的 `td` 数量通常少于 5 个，用 `>= 5` 有效过滤掉空态行。

### get_row_data() — td 不足时安全返回

```python
td_count = row.locator('td').count()
if td_count < 5:
    return None
```

## 注意事项：`or_` strict 模式

Playwright `locator.or_()` 要求**每个分支的选择器不匹配到多个元素**。

```python
# ❌ 错误：逗号组合选择器会同时匹配 .el-table__empty-text 和 .el-table__empty-block
empty_hint = self.page.locator('.el-table__empty-text, .el-table__empty-block')

# ✅ 正确：只使用单一选择器
empty_hint = self.page.locator('.el-table__empty-text').first
```
