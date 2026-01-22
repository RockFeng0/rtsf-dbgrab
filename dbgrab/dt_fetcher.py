#! python3
# -*- encoding: utf-8 -*-
import re
from datetime import datetime, timedelta
from dbgrab.dt_factory import (
    check_data,
    logger,
    get_month_start_end_dates,
    get_year_start_end_dates,
    get_day_dates,
)
from dbgrab.dt_extractor import DataExtractor
from dbgrab.cons import j_conf


class DataBaseFetcher(object):
    """
    数据库数据抓取器，基于数据库提取器和SQL模板文件抓取数据，并保存到csv
    """

    def __init__(self, db_alias=None, chunk_size=200000, is_iter=False, db_cfg_file='database.yml', sql_cfg_file='tables.yml'):
        """
        :param db_alias: 数据库别名，从database.yml配置文件中获取，如: oceanbase, oracle, postgres
        :param chunk_size: 数据抽取的批次大小，默认200000
        :param is_iter: 是否以迭代器模式抽取数据，默认False， 该参数已失效
        :param db_cfg_file: 数据库配置文件路径，默认database.yml
        :param sql_cfg_file: SQL模板配置文件路径，默认tables.yml
        :return:            
        """
        
        # 读取yaml配置并初始化引擎
        j_conf.init_engines(db_cfg_file=db_cfg_file)

        # 根据配置的别名，获取引擎
        self._engine = j_conf.ENGINE_MAP.get(db_alias)
        if not self._engine:
            raise ValueError(f'未知的数据库别名, 已配置的: {j_conf.ENGINE_MAP}')

        # 读取yaml配置并初始化SQL预清洗的模板
        j_conf.init_sql_template(sql_cfg_file=sql_cfg_file)
        if not j_conf.SQL_CONFIG:
            print(f"Waring: 未配置数据提取模板 : {j_conf.SQL_CONFIG}")

        # 设置引擎和提取文件存储路径，初始化抽取/提取器
        self._dt_extractor = DataExtractor(self._engine, j_conf.FETCH_FILE_PATH)

        self._db_alias = db_alias
        self._chunk_size = chunk_size
        self._is_iter = is_iter

    @property
    def extractor(self):
        return self._dt_extractor.extractor

    @property
    def engine(self):
        return self._engine

    @property
    def to_csv(self):
        return self._data_fetcher()

    @property
    def to_csv_iter(self):
        return self._data_fetcher_iter()

    def _data_fetcher(self):
        @self._dt_extractor.fetch_db_iter(chunk_size=self._chunk_size)
        def fetch_data_func(table_name, start_date=None, end_date=None, T_1=False, fmt="%Y%m%d"):
            """
            :param table_name: Oracle库的表名, 从tables.yml配置文件中获取
            :param T_1: 当天抽取 当天时间-1天的数据
            :param start_date: 数据抽取的开始时间，如 20231001
            :param end_date: 数据抽取的结束时间，如 20240831
            :param fmt: 指定日期过滤格式，默认为%Y%m%d，如：20231001
            :return:
            """

            if T_1:
                # T+1
                start_date = end_date = (
                        datetime.now() - timedelta(days=1, microseconds=0, seconds=0)
                ).strftime(fmt)
            elif start_date is None or end_date is None:
                raise ValueError("start_date or end_date is None")

            print(f"{j_conf.SQL_CONFIG['tables'][table_name]['desc']}")

            fetch_sql = j_conf.SQL_CONFIG["tables"][table_name]['sql'].format(start_date=start_date, end_date=end_date)

            count_query = re.sub(r"SELECT.+FROM", "SELECT count(1) FROM", fetch_sql, flags=re.DOTALL | re.I)
            count_sql = re.sub(r"ORDER BY.*$", "", count_query, flags=re.DOTALL | re.I)

            print(f"Count SQL({start_date}-{end_date}): ---\n{count_sql.strip()}")
            logger.debug(f"Count SQL({start_date}-{end_date}): ---\n{count_sql.strip()}")

            count = check_data(self._engine, count_sql)[0]

            print(f"Count num: {count}")
            logger.debug(f"Count num: {count}")

            file_date = end_date.replace("-", "")
            file_name = "A_paycenter_{}_D_{}_01".format(table_name.split('.')[1], file_date)

            return [(file_name, file_date, fetch_sql, count)]

        return fetch_data_func

    def _data_fetcher_iter(self):
        @self._dt_extractor.fetch_db_iter(chunk_size=self._chunk_size)
        def fetch_data_iter_func(table_name, start_date, end_date, index=1, mode="month", fmt="%Y%m%d"):
            """
            :param table_name: Oracle库的表名, 从tables.yml配置文件中获取
            :param start_date: 数据抽取的开始时间，如 20231001
            :param end_date: 数据抽取的结束时间，如 20240831
            :param index: 数据抽取的索引，默认1, (可根据日志记录的断点时间，调整index,start_date,end_date从断点开始抽取)
            :param mode: 数据抽取的模式，默认month，可选month, year, day
            :param fmt: 指定日期过滤格式，默认为%Y%m%d，如：20231001
            :return:
            """

            if mode == "day":
                s_e_dates = get_day_dates(start_date, end_date, fmt)
            elif mode == "month":
                # 基线 - 亿级别数据 按月拆
                s_e_dates = get_month_start_end_dates(start_date, end_date, fmt)
            elif mode == "year":
                # 按年拆
                s_e_dates = get_year_start_end_dates(start_date, end_date, fmt)
            else:
                raise Exception("Unknown mode: %s, should be 'month' or 'year'." % mode)

            logger.debug(f'{mode} start - end : {s_e_dates}')

            print(f"{j_conf.SQL_CONFIG['tables'][table_name]['desc']}")
            logger.debug(f"{j_conf.SQL_CONFIG['tables'][table_name]['desc']}")

            _filter = j_conf.SQL_CONFIG["tables"][table_name]['filter']
            if _filter is None:
                raise Exception("No datetime filter.")

            print(f"Datetime during: {start_date} - {end_date}\n-")
            logger.debug(f"Datetime during: {start_date} - {end_date}\n-")

            for _start_date, _end_date in s_e_dates:
                fetch_sql = j_conf.SQL_CONFIG["tables"][table_name]['sql'].format(start_date=_start_date, end_date=_end_date)

                # count_sql = f"select count(1) from {table_name} where {_filter} >= '{_start_date}' and {_filter} <='{_end_date}'"
                count_query = re.sub(r"SELECT.+FROM", "SELECT count(1) FROM", fetch_sql, flags=re.DOTALL | re.I)
                count_sql = re.sub(r"ORDER BY.*$", "", count_query, flags=re.DOTALL | re.I)

                print(f"Count SQL({_start_date}-{_end_date}): ---\n{count_sql.strip()}")
                logger.debug(f"Count SQL({_start_date}-{_end_date}): ---\n{count_sql.strip()}")

                count = check_data(self._engine, count_sql)[0]

                print(f"Count num: {count}")
                logger.debug(f"Count num: {count}")
                if count == 0:
                    continue

                file_date = end_date.replace("-", "")
                file_name = "A_paycenter_{}_D_{}_{}".format(table_name.split('.')[1], file_date, "%03d" % index)
                index += 1
                print(f"File: {file_name}")
                logger.debug(f"File: {file_name}")
                yield file_name, end_date, fetch_sql, count

        return fetch_data_iter_func