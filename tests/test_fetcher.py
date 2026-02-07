#! python3
# -*- encoding: utf-8 -*-

import pytest
from dbgrab import log
from dbgrab.dt_fetcher import DataBaseFetcher

env_file= "cmft_conf/.env.cmft"
sql_file= "cmft_conf/tables.yml"
log_file = "temp/mytest.log"

def test_grab_mysql():
    # 设置日志
    log.to_file(log_file)
    print("log: %s" % log_file)

    dbf = DataBaseFetcher(env_file, sql_file).with_engine("CREDIBLE")  # oracle

    # T+1
    print(dbf.to_csv(table_name='credible_db.fetcher_task_record', T_1=True))
    print("✓ 数据抓取器（DataBaseFetcher） T+1抓取功能，测试成功")

    #  指定日期
    print(dbf.to_csv(table_name='credible_db.fetcher_task_record', start_date="20250818", end_date="20251026"))
    print("✓ 数据抓取器（DataBaseFetcher） 指定日期抓取功能，测试成功")

    # 迭代抽取
    print(dbf.to_csv_iter(table_name='credible_db.fetcher_task_record', start_date="20250818", end_date="20251026", mode="day"))
    print("✓ 数据抓取器（DataBaseFetcher） 迭代抽取抓取功能，测试成功")

def test_grab_oceanbase():
    # 设置日志 - oceanbase 库 需要安装java jdk,并配置JAVA_HOME
    log.to_file(log_file)
    print("log: %s" % log_file)

    dbf = DataBaseFetcher(env_file, sql_file).with_engine("TRADE")  # oceanbase

    # T+1
    print(dbf.to_csv(table_name='TRADEDBADM.WTAORDLT', T_1=True))
    print("✓ 数据抓取器（DataBaseFetcher） T+1抓取功能，测试成功")

    #  指定日期
    print(dbf.to_csv(table_name='TRADEDBADM.WTAORDLT', start_date="20251204", end_date="20260204"))
    print("✓ 数据抓取器（DataBaseFetcher） 指定日期抓取功能，测试成功")

    # 迭代抽取
    print(dbf.to_csv_iter(table_name='TRADEDBADM.WTAORDLT', start_date="20200101", end_date="20251026", mode="year"))
    print("✓ 数据抓取器（DataBaseFetcher） 迭代抽取抓取功能，测试成功")


if __name__ == "__main__":
    pytest.main()
