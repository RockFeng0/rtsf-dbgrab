#! python3
# -*- encoding: utf-8 -*-

import os
from rtsf.p_common import FileUtils
from dbgrab import logger
from dbgrab.jaydebe.engine_mapping import get_engine_manager


class Config(object):
    SQL_CONFIG = {}  # 数据采集模板
    ENGINE_MANAGER = None  # 数据库引擎管理器
    
    # 保持向后兼容的属性
    DB_CONFIG = {}  # 数据引擎配置
    WORK_PATH = ""  # 工作路径
    FETCH_LOG_PATH = ""  # 抓取器日志路径
    FETCH_FILE_PATH = ""  # 抓取器文件存储路径


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
    def init_engines(cls, env_file=None):
        """ 初始化数据库引擎配置        
        Args:
            env_file (str, optional): 环境配置文件路径.
        """
        # 初始化引擎管理器
        cls.ENGINE_MANAGER = get_engine_manager(env_file)

        cls.WORK_PATH = cls.ENGINE_MANAGER._config.WORK_PATH
        logger.info(f"Init WORK_PATH: {cls.WORK_PATH}")

        cls.FETCH_LOG_PATH = cls.ENGINE_MANAGER._config.LOG_PATH
        logger.info(f"Init LOG_PATH: {cls.FETCH_LOG_PATH}")

        cls.FETCH_FILE_PATH = cls.ENGINE_MANAGER._config.FILE_PATH
        logger.info(f"Init FILE_PATH: {cls.FETCH_FILE_PATH}")

        # 打印引擎信息
        engines = cls.ENGINE_MANAGER.list_engines()
        logger.info(f"Init ENGINE_MANAGER: {engines.keys()}")

# 使用配置类
config = JayDeBeConfig

# 保持向后兼容
j_conf = config

