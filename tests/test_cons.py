#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
测试配置加载功能
"""
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
        generator.get_database_template("temp/database.yml")
        print(f"  - 保存到 temp/database.yml")

        # 获取SQL配置模板
        generator.get_tables_template("temp/tables.yml")
        print(f"  - 保存到 dbconfig/tables.yml")

        print("✓ 成功生成配置模板")
    except Exception as e:
        print(f"✗ 生成配置模板失败: {e}")


def test_jaydebe_config():
    """测试jaydebe配置加载"""
    print("\n测试数据库配置 database.yml配置加载...")
    db_config_file = 'temp/database.yml'
    try:
        j_conf.init_engines(db_cfg_file=db_config_file)
    except:
        pass

    assert j_conf.WORK_PATH == "/xx/xx"
    assert j_conf.FETCH_LOG_PATH == "/xx/xx/logs"
    assert j_conf.FETCH_FILE_PATH == "/xx/xx/files"
    assert j_conf.ENGINE_MAP == {}
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
