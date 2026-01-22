#! python3
# -*- encoding: utf-8 -*-

import sys, os
from rtsf.p_common import FileUtils
from sqlalchemy import create_engine
from dbgrab import logger
from dbgrab.jaydebe.jaydebe_engine import JayDeBeEngine


class Config(object):
    DB_CONFIG = {}  # 数据引擎配置
    SQL_CONFIG = {}  # 数据采集模板

    WORK_PATH = ""  # 工作路径
    FETCH_LOG_PATH = ""  # 抓取器日志路径
    FETCH_FILE_PATH = ""  # 抓取器文件存储路径
    ENGINE_MAP = {}  # 数据库引擎映射


class JayDeBeConfig(Config):

    @classmethod
    def init_sql_template(cls, sql_cfg_file='tables.yml'):
        """ 初始化SQL模板配置        
        Args:
            sql_cfg_file (str, optional): SQL模板配置文件路径. 默认值为 'tables.yml'.
        """
        cls.SQL_CONFIG = FileUtils.load_file(sql_cfg_file)
        logger.info(f"Init SQL_CONFIG: {cls.SQL_CONFIG['tables'].keys()}")

    @classmethod
    def init_engines(cls, db_cfg_file='database.yml'):
        """ 初始化数据库引擎配置        
        Args:
            db_cfg_file (str, optional): 数据库引擎配置文件路径. 默认值为 'database.yml'.
        """
        cls.DB_CONFIG = FileUtils.load_file(db_cfg_file)

        cls.WORK_PATH = cls.DB_CONFIG["paths"]["work_path"]
        logger.info(f"Init WORK_PATH: {cls.WORK_PATH }")

        cls.FETCH_LOG_PATH = cls.DB_CONFIG["paths"]["fetch_log_path"]
        logger.info(f"Init FETCH_LOG_PATH: {cls.FETCH_LOG_PATH }")

        cls.FETCH_FILE_PATH = cls.DB_CONFIG["paths"]["fetch_file_path"]
        logger.info(f"Init FETCH_FILE_PATH: {cls.FETCH_FILE_PATH }")

        for database in cls.DB_CONFIG["databases"]:
            if database["type"] in ("pg", "oracle", "mysql", "sqlite"):
                engine = create_engine(database["uri"])
            elif database["type"] == "oceanbase":
                # OceanBase SQL - Oracle Mode
                engine = JayDeBeEngine(
                    jdbc_driver_name=database["driver"],
                    jdbc_url=database["jdbc"],
                    jdbc_user=database["username"],
                    jdbc_password=database["password"],
                    jdbc_jar=database["jar"]
                )
            else:
                raise Exception("Unknown database type: '%s' from database.yaml" % database["type"])
            # setattr(cls, database['alias'].upper(), engine)
            cls.ENGINE_MAP[database['alias']] = engine
        logger.info(f"Init ENGINE_MAP: {cls.ENGINE_MAP }")


j_conf = JayDeBeConfig

# 保持向后兼容，加载默认配置
# 如果需要默认配置，可以在YAML文件中定义
