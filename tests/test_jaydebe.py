#! python3
# -*- encoding: utf-8 -*-

import os
import pytest
from dbgrab.jaydebe import get_engine_manager


def test_engine_map():
    # 使用自定义.env文件
    env_file = os.path.join(os.path.dirname(__file__), '.env.example')

    # 获取引擎管理器
    manager = get_engine_manager(env_file)

    # 列出所有引擎信息
    engines = manager.list_engines()
    print("\n📊 已配置的数据库引擎:")
    for name, info in engines.items():
        print(f"  🔹 {name}: {info}")

    # 获取指定的引擎
    print(f"获取指定的引擎: {manager.get_engine("USER2")}")

    # 获取指定的session
    with manager.get_session("USER2") as session:
        print(f"获取指定的session: {session}")

    # 关闭所有引擎
    manager.close_all_engines()

if __name__ == "__main__":
    pytest.main()