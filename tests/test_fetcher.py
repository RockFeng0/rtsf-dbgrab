#! python3
# -*- encoding: utf-8 -*-

import pytest
from dbgrab import log
from dbgrab.dt_fetcher import DataBaseFetcher


def test_grab_mysql():
    # 设置日志
    log_file = "mytest.log"
    log.to_file(log_file)
    print("log: %s" % log_file)

    dbf = DataBaseFetcher("CREDIBLE").with_config(env_file=".env.dev", sql_file="tables.yml")  # oracle

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
    # 设置日志
    log_file = "mytest_ob.log"
    log.to_file(log_file)
    print("log: %s" % log_file)

    dbf = DataBaseFetcher("TRADE").with_config(env_file=".env.dev", sql_file="tables.yml") # oceanbase

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
