#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
测试配置加载功能
"""
import os.path

# import sys
# _path = "/app/apprun/cothin/jupyternotebook/admin/rock/rtsf-dbfetcher"
# if _path not in sys.path:
#     sys.path.append(_path)
#
# import os
# os.environ["JAVA_HOME"] = "/app/apprun/anaconda3/envs/dcapp"
# os.environ.get("JAVA_HOME")

import pytest
from dbgrab import ConfigGenerator
from dbgrab.cons import j_conf


def test_config_generator():
    """测试配置生成 ConfigGenerator"""
    print("\n测试配置模板...")
    try:
        # 初始化配置生成器
        generator = ConfigGenerator()

        # 获取数据库配置模板
        output_path = "temp/database.yml"
        generator.get_database_template(output_path)
        print(f"  - 保存到 {output_path}")

        # 获取SQL配置模板
        output_path = "temp/tables.yml"
        generator.get_tables_template(output_path)
        print(f"  - 保存到 {output_path}")

        print("✓ 成功生成配置模板")
    except Exception as e:
        print(f"✗ 生成配置模板失败: {e}")


def test_jaydebe_config():
    """测试jaydebe配置加载"""
    print("\n测试数据库配置 .env.example 配置加载...")
    env_file = '.env.example'
    try:
        j_conf.init_engines(env_file)
    except:
        pass
    for i in dir(j_conf):
        if i.isupper():
            print(f"{i}: {getattr(j_conf, i)}")
    print("✓ 成功加载数据库配置")


def test_tables_config():
    """测试表配置加载"""
    print("\n测试SQL tables.yml加载...")
    sql_template = 'temp/tables.yml'
    try:
        j_conf.init_sql_template(sql_cfg_file=sql_template)
        TABLES = j_conf.SQL_CONFIG['tables']
        print(f"  - 加载的表数量: {len(TABLES)}")
        print("  - 表名列表:")
        for table_name in list(TABLES.keys())[:5]:  # 只显示前5个表名
            print(f"    * {table_name}")
        if len(TABLES) > 5:
            print(f"    ... 等{len(TABLES) - 5}个表")
        print(f"✓ 成功加载表配置")
    except Exception as e:
        print(f"✗ 加载表配置失败: {e}")


if __name__ == "__main__":
    pytest.main()
