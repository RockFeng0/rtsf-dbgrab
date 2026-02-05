#! python3
# -*- encoding: utf-8 -*-

from typing import Dict, Optional, Any
from rtsf.p_common import FileUtils
from dbgrab import logger
from dbgrab import get_engine_manager


class JayDeBeConfig(object):

    def __init__(self, env_file=".env", sql_file="sql.yml"):
        """
            :param env_file: 环境配置文件路径
            :param sql_file: SQL模板配置文件
            :return:
        """
        self.sql_config: Dict[str, Any] = {}
        self.manager = None
        self.db_config = None

        self._load_sql(sql_file)
        self._init_engine_manager(env_file)

    def _load_sql(self, sql_file):
        """ 初始化SQL模板配置
        Args:
            sql_file (str, optional): SQL模板配置文件路径. 默认值为 'tables.yml'.
        """
        self.sql_config = FileUtils.load_file(sql_file)
        logger.info(f"Load SQL template: {self.sql_config['tables'].keys()}")

    def _init_engine_manager(self, env_file):
        """ 初始化数据库引擎管理器
        Args:
            env_file (str, optional): 环境配置文件路径.
        """
        # 初始化引擎管理器
        self.manager = get_engine_manager(env_file)
        self.db_config = self.manager._config

        # 打印引擎信息
        engines = self.manager.list_engines()
        logger.info(f"Init engines: {engines.keys()}")


