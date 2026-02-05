#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import pytest
from dbgrab import ConfigGenerator
from dbgrab.cons import JayDeBeConfig


env_file=".env.example"
sql_file="temp/table.yml"


def test_jaydebe_config():
    """测试jaydebe配置加载"""
    print("加载配置文件...")

    generator = ConfigGenerator()
    generator.get_tables_template(sql_file)

    j_conf = JayDeBeConfig(env_file=env_file, sql_file=sql_file)
    print(f"SQL配置： {j_conf.sql_config}")
    print(f"引擎管理器： {j_conf.manager}")
    print(f"ENV配置： {[i for i in dir(j_conf.db_config) if i.isupper()]}")

    print("✓ 成功加载数据库配置")



if __name__ == "__main__":
    pytest.main()
