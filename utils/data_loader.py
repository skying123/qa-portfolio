import os
import yaml

"""
读取yaml中的测试数据
"""
def load_test_data():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(root_dir, "data", "users.yaml")
    with open(data_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)