#! python3
# -*- encoding: utf-8 -*-

import os
from datetime import datetime, timedelta
import calendar
import pandas as pd

from tqdm import tqdm
from rtsf.p_common import FileSystemUtils
from rtsf.p_applog import AppLog


# 获取给定日期范围，每个月的起止时间
def get_month_start_end_dates(start_date, end_date, fmt="%Y%m%d"):
    start_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")

    month_start_dates = []
    current_year = start_date.year
    current_month = start_date.month

    while True:
        month_start_date = datetime(current_year, current_month, 1)
        month_end_date = datetime(current_year, current_month, day=calendar.monthrange(current_year, current_month)[1])

        if month_start_date > end_date:
            break

        month_start_dates.append((month_start_date.strftime(fmt), month_end_date.strftime(fmt)))

        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1

    return month_start_dates


# 获取给定日期范围，每个年的起止时间
def get_year_start_end_dates(start_date, end_date, fmt="%Y%m%d"):
    start_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")

    year_start_dates = []
    current_year = start_date.year

    while True:
        year_start_date = datetime(year=current_year, month=1, day=1)
        year_end_date = datetime(year=current_year, month=12, day=31)

        if year_start_date > end_date:
            break

        year_start_dates.append((year_start_date.strftime(fmt), year_end_date.strftime(fmt)))

        current_year += 1

    return year_start_dates


# 获取给定日期范围，输出范围内每天的日期
def get_day_dates(start_date, end_date, fmt="%Y%m%d"):
    # get_day_dates("20231001", "20231007")

    start_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")

    # 使用 timedelta 逐日打印日期
    dates = []
    current = start_date
    while current <= end_date:
        dates.append((current.strftime(fmt), current.strftime(fmt)))
        current += timedelta(days=1)

    return dates


# 查看数据量
def check_data(conn, sql_query):
    """
    # 全部黑名单的数据量
    conn = conf.ORACLE_ENGINE
    check_data(conn, "SELECT count(*) FROM SWORDADM.BLACK_INFO t")
    # 转账到和包订单表 2023年全年的交易量
    conn = conf.PG_ENGINE
    check_data(conn, "SELECT count(1) FROM dd.ods_WTAORDLT t where t.ord_dt >= '20230101' and t.ord_dt <='20231231'")
    """
    conn = conn.raw_connection()
    cursor = conn.cursor()
    result = cursor.execute(sql_query)
    # Max num:  cursor.fetchall()
    return cursor.fetchone()



log = AppLog()
logger = log.get_logger()


class SqlExtractor(object):

    def __init__(self, engine, work_path):
        """
        Args:
            engine: 数据库引擎，如 SQLAlchemy 或 JayDeBeEngine 实例
            work_path: 数据提取工作目录路径
        """
        self.engine = engine
        # print(engine)
        self._file_name = None
        self._chk_file = None
        self._work_path = work_path
        self.count = 0

    def set_file(self, file_name):
        """
        :param file_name: 不带文件后缀的文件名
        """
        file_path, file_name = os.path.split(file_name)
        if file_path:
            raise Exception("Need file name without: %s" % file_path)

        file_name, ext = os.path.splitext(file_name)
        if ext:
            raise Exception("Need file name without: %s" % ext)

        csv_file = "{}.csv".format(file_name)
        self._file_name = os.path.join(self._work_path, csv_file)

        chk_file = "{}.chk".format(file_name)
        self._chk_file = os.path.join(self._work_path, chk_file)

        # FileSystemUtils.mkdirs(os.path.join(self._work_path, "logs"))
        # log_file = "{}_{}.log".format(file_name, datetime.now().strftime('%Y%m%d'))
        # log.to_file(os.path.join(self._work_path, "logs", log_file))

        return self

    def to_csv(self, sql_query, chunk_size=1024):
        """ read_sql_query的逻辑是
        1. 先用execute执行sql语句，然后在判断是否有chunksize，没有就直接返回所有数据，有的话根据chunksize返回一个iterator。
        2. 所以,使用chunk_size，这不是一个真正的分批次读取，如果数据量大，还是会导致内存爆炸直至卡死
        :param sql_query:
        :param chunk_size:
        :return:
        """

        if self._file_name is None:
            # print("Warning: need to call method 'set_file'.")
            logger.warning("Warning: need to call method 'set_file'.")
            return

        # print("Please wait...")
        logger.info("Please wait...")

        FileSystemUtils.force_delete_file(self._file_name)

        count_num = 0
        # self.count = 0
        chunks = pd.read_sql_query(sql_query, con=self.engine, chunksize=chunk_size)
        is_header = True
        for chunk in chunks:
            count_num += len(chunk)
            start_time = datetime.now()
            chunk.to_csv(self._file_name, mode="a", index=False, header=is_header, float_format='{:f}'.format, encoding='utf-8')
            is_header = False
            elapsed_time = datetime.now() - start_time
            # print(f'chunksize={chunk_size}: {elapsed_time.total_seconds()} seconds')
        # print("Save to '%s' success(%d)" % (self._file_name, count_num))
        self.count += count_num
        logger.info("Save to '%s' success(%d)" % (self._file_name, count_num))
        logger.info(f"Extracted: {self.count}\n---")

    def write_chk_file(self, count, date):
        if self._file_name is None:
            print("Warning: need to call method 'set_file'.")
            return

        if not os.path.exists(self._file_name):
            print(f"Warning: {self._file_name} is not exist. Will create a empty file.")
            with open(self._file_name, 'w') as f:
                pass

        file_size = os.path.getsize(self._file_name)
        with open(self._chk_file, 'w') as f:
            data = "{}|{}|{}|{}\t".format(os.path.split(self._file_name)[1], str(file_size), str(count), str(date))
            f.write(data)

class PgSqlExtractor(SqlExtractor):

    def __init__(self, engine, work_path):
        super().__init__(engine, work_path)

    def to_csv_enhance(self, sql_query, chunk_size=10000, offset=0, max_lines=None):
        """        构造 limit 子句，实现大数据的分批读取。
        :param sql_query: sql语句 不带limit 和 offset
        :param chunk_size: 每次取的行数，默认1万
        :param offset: 起始位，默认0
        :param max_lines: 最大取数, 默认一直取数; 若设置了，则打印总进度条
        :return:
        """
        if self._file_name is None:
            # print("Warning: need to call method 'set_file'.")
            logger.warning("Warning: need to call method 'set_file'.")
            return

        # print("Please wait...")
        logger.info("Please wait...")

        count_num = 0
        is_header = True
        FileSystemUtils.force_delete_file(self._file_name)

        progress_bar = tqdm(total=max_lines, unit='rows') if max_lines else None
        while True:
            try:
                # 从数据库中获取数据
                # query = f"{sql_query} LIMIT {chunk_size}  offset {offset}"
                query = f"{sql_query} OFFSET {offset} ROWS FETCH FIRST {chunk_size} ROWS ONLY;"

                logger.debug(f"Reading SQL offset: {offset}")
                df = pd.read_sql(query, self.engine)
                if df.empty:
                    logger.debug("==== Read SQL Finish. ====")
                    break

                length_df = len(df)
                count_num += length_df
                _ = progress_bar.update(length_df) if progress_bar is not None else None
                logger.debug(f"Updating csv file: {count_num}/{max_lines}")
                df.to_csv(self._file_name, index=False, header=is_header, mode='a')
                is_header = False

                offset += chunk_size
                if (max_lines is not None) and (offset >= max_lines):
                    break
            except Exception as e:
                # print("Error occurred while reading from database.")
                logger.error("Error occurred while reading from database.")
                raise e
        # print("Save to '%s' success(%d)" % (self._file_name, count_num))
        self.count += count_num
        logger.info("Save to '%s' success(%d)" % (self._file_name, count_num))
        logger.info(f"Extracted: {self.count}\n---")


class OracleSqlExtractor(SqlExtractor):

    def __init__(self, engine, work_path):
        super().__init__(engine, work_path)
        self.to_csv_enhance = self.to_csv

