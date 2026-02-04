#! python3
# -*- encoding: utf-8 -*-

import os
import pytest
from dbgrab.configs import  get_db_config

def test_conf():
    # 使用自定义.env文件
    env_file = os.path.join(os.path.dirname(__file__), '.env.example')

    # 打印读取到的.env配置
    print("📄 读取到的.env配置:")
    config = get_db_config(env_file)
    print(f"数据模型配置: {config.model_config}")
    print(f"所有配置: {[i for i in dir(config) if i.isupper()]}")

    print(f"  数据库配置:")
    for db_name, db_config in config.DATABASES.items():
        print(f"    🔹 {db_name}:")
        # 处理字典类型的配置
        print(f"      URL: {db_config.URL}")
        print(f"      连接池大小: {db_config.POOL_SIZE}")
        print(f"      最大溢出连接数: {db_config.MAX_OVERFLOW}")
        print(f"      连接回收时间: {db_config.POOL_RECYCLE}秒")
        print(f"      输出SQL日志: {db_config.ECHO}")

    print(f"  DATABASES: {config.DATABASES.keys()}")
    print(f"    DATABASES: {config.DATABASES}")
    print(f"  OCEANBASES: {config.OCEANBASES.keys()}")
    print(f"    OCEANBASES: {config.OCEANBASES}")


if __name__ == "__main__":
    pytest.main()