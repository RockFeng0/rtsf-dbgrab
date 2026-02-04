#! python3
# -*- encoding: utf-8 -*-

# import sys
# _path = "/app/apprun/cothin/jupyternotebook/admin/rock/rtsf-dbfetcher"
# if _path not in sys.path:
#     sys.path.append(_path)
# sys.path

import os
os.environ["JAVA_HOME"] = r"D:\auto\python\rtsf-dbgrab\.venv\Lib\site-packages"
os.environ.get("JAVA_HOME")

from dbgrab.cons import j_conf
from dbgrab import get_month_start_end_dates, check_data, DataExtractor, get_engine_manager


def test_data_extractor():
    """数据抽取器（DataExtractor）测试"""

    try:
        # j_conf.init_engines(db_cfg_file=db_config_file)
        manager = get_engine_manager(".env.dev")

        engine = manager.get_engine("TRADE")
        print(f"Engine: {engine}")

        dte = DataExtractor(engine, manager._config.WORK_PATH)
        print(f"Extractor：{dte.extractor}")

        months = get_month_start_end_dates("20250801", "20250806", fmt="%Y%m%d")
        (first_day, last_day) = months[0]
        print(f"first_day and last_day: {(first_day, last_day)}")  # ('2025-08-01', '2025-08-31')

        # sql_template = "SELECT * FROM SWORDADM.BLACK_INFO t where TO_CHAR(t.create_date, 'YYYY-MM-DD') between '{}' and '{}'"

        sql_template =  """
        SELECT ord_dt,trn_usr_no FROM TRADEDBADM.WTAORDLT t
        WHERE TO_DATE(t.ord_dt, 'YYYYMMDD') >= TO_DATE('{first_day}','YYYYMMDD')
        AND TO_DATE(t.ord_dt, 'YYYYMMDD') <= TO_DATE('{last_day}', 'YYYYMMDD') 
        AND ROWNUM <= 100
        """

        query = sql_template.format(first_day, last_day)

        sql_query_count = query.lower().replace('select * from', "select count(*) from")
        max_info = check_data(engine, sql_query_count)
        print(sql_query_count)
        print("Count总数: ", max_info)

        # file_name = "risk-BLACK_INFO-m-{}".format("".join(first_day.split('-'))[:6])
        # dte.extractor.set_file(file_name).to_csv(query, chunk_size=20000)
        # print("✓ 抽取器（Extractor）数据提取测试成功")
    except Exception as e:
        print(f"✗ 抽取器（Extractor）数据提取测试失败: {e}")





if __name__ == "__main__":
    print("开始测试DataExtractor功能...\n")
    test_data_extractor()
    print("\n测试完成！")
