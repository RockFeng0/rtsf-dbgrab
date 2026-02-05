#! python3
# -*- encoding: utf-8 -*-

import pytest
from dbgrab import get_engine_manager, check_data, DataExtractor

env_file = ".env.dev"
manager = get_engine_manager(env_file)

def test_extractor_mysql():
    credible_engine = manager.get_engine("CREDIBLE")

    # noinspection SqlNoDataSourceInspection
    sql_query = r"select * from credible_db.fetcher_task_record ftr limit 50"

    # 检查数据量
    sql_query_count = sql_query.lower().replace('select * from', "select count(*) from")
    max_info = check_data(credible_engine, sql_query_count)
    print("Count总数: ", max_info)

    # 抽取数据
    dte = DataExtractor(credible_engine, manager._config.WORK_PATH)
    dte.extractor.set_file("credible_test").to_csv(sql_query, chunk_size=20000)

def test_extractor_oceanbase():
    trade_engine = manager.get_engine("TRADE")

    # noinspection SqlNoDataSourceInspection
    sql_query = "SELECT * FROM TRADEDBADM.WTAORDLT t where ROWNUM <= 1000"

    # 检查数据量
    sql_query_count = sql_query.lower().replace('select * from', "select count(*) from")
    max_info = check_data(trade_engine, sql_query_count)
    print("Count总数: ", max_info)

    # 抽取数据
    dte = DataExtractor(trade_engine, manager._config.WORK_PATH)
    dte.extractor.set_file("trade_test").to_csv(sql_query, chunk_size=20000)


if __name__ == "__main__":
    pytest.main()
