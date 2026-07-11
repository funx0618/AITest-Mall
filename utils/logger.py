"""
日志工具 - 统一日志记录
职责：提供项目统一的 logger 实例，记录请求和响应信息
"""

import logging
import sys

# 创建项目统一 logger
logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

# 避免重复添加 handler
if not logger.handlers:
    # 控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # 日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
