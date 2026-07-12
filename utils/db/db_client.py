"""
数据库客户端 - 封装 MySQL 查询
职责：提供统一的数据库查询接口
"""

import pymysql
from pymysql.cursors import DictCursor
from config.settings import DB_CONFIG


class DBClient:
    """MySQL 数据库客户端"""

    def __init__(self):
        self._conn = pymysql.connect(
            **DB_CONFIG,
            cursorclass=DictCursor,
            charset="utf8mb4",
        )

    def query(self, sql: str, params: tuple | list | None = None) -> list[dict]:
        """执行查询 SQL，返回结果列表"""
        with self._conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def close(self):
        """关闭连接"""
        self._conn.close()
