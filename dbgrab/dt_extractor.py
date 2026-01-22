#! python3
# -*- encoding: utf-8 -*-
from functools import wraps
from dbgrab.dt_factory import PgSqlExtractor, OracleSqlExtractor


class DataExtractor(object):
    """
    数据提取器，基于数据库引擎实例对象，初始化数据提取器
    """

    def __init__(self, engine, fp):
        """
        Args:
            engine: 数据库引擎实例，如 SQLAlchemy 或 JayDeBeEngine 实例
            fp: 数据提取工作目录路径
        """
        self._engine = engine
        self.extractor = self._init_extractor(fp)

    def _init_extractor(self, fp):
        if "postgresql:" in str(self._engine):
            extractor = PgSqlExtractor(self._engine, fp)

        elif "oracle:" in str(self._engine):
            extractor = OracleSqlExtractor(self._engine, fp)

        elif "oceanbase:" in str(self._engine):
            conn = self._engine.connect()
            extractor = OracleSqlExtractor(conn, fp)

        else:
            raise ValueError("Unknown database type")
        return extractor

    def fetch_db_iter(self, chunk_size):
        _extractor = self.extractor
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                files = []
                _extractor.count = 0
                for file_name, end_date, fetch_sql, count in func(*args, **kwargs):

                    db_args = [fetch_sql]
                    db_kwargs = {
                        "chunk_size": chunk_size,
                        "max_lines": count,
                    }
                    if "oracle:" in str(self._engine ) or "oceanbase:" in str(self._engine ):
                        db_kwargs.pop("max_lines")

                    _extractor.set_file(file_name).to_csv_enhance(*db_args, **db_kwargs)
                    _extractor.write_chk_file(count, end_date)
                    files.append((file_name + '.csv', file_name + '.chk'))
                return files, _extractor.count
            return wrapper
        return decorate
