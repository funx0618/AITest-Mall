"""
测试数据加载工具
从 data/ 目录加载 YAML 格式的测试数据
"""

import yaml
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"


def load_yaml(file_path: str) -> dict:
    full_path = DATA_DIR / file_path
    with open(full_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
