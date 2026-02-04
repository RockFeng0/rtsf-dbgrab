#! python3
# -*- encoding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Dict, Optional, Any
from contextlib import contextmanager

from dbgrab.configs import get_db_config, clear_config_cache
from dbgrab.dt_exceptions import EngineError
from dbgrab.extractor.dt_factory import logger
from dbgrab.jaydebe.jaydebe_engine import JayDeBeEngine


class DatabaseEngineManager:
    """数据库引擎管理器"""

    def __init__(self, env_file: Optional[str] = None):
        self._env_file = env_file
        self._config = get_db_config(env_file)
        self._engines: Dict[str, Any] = {}
        self._sessionmakers: Dict[str, Any] = {}

        self._initialize_engines()

    def get_engine(self, db_name: str) -> Any:
        """获取数据库引擎"""
        if db_name not in self._engines:
            raise EngineError(f"数据库引擎 '{db_name}' 不存在")

        return self._engines[db_name]

    @contextmanager
    def get_session(self, db_name: Optional[str]):
        """获取数据库会话的上下文管理器"""
        session_maker = self._get_sessionmaker(db_name)
        session = session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def list_engines(self) -> Dict[str, Dict[str, Any]]:
        """列出所有引擎的配置信息（隐藏敏感信息）"""
        engine_info = {}
        for name, engine in self._engines.items():
            if hasattr(engine, "dialect"):
                engine_info[name] = {
                    'url': str(engine.url).split('@')[0] + '@***',  # 隐藏密码
                    'pool_size': engine.pool.size(),
                    'echo': engine.echo,
                    'dialect': engine.dialect.name
                }
            else:
                engine_info[name] = {
                    'url': engine._jdbc_url,
                    'dialect': "oceanbase"
                }
        return engine_info

    def reload_engines(self, env_file: Optional[str] = None):
        """重新加载引擎配置"""
        logger.info("重新加载数据库引擎配置...")

        # 关闭现有引擎
        self.close_all_engines()

        # 清除缓存并重新加载配置
        clear_config_cache()
        self._env_file = env_file or self._env_file
        self._config = get_db_config(self._env_file)

        # 重新初始化引擎
        self._initialize_engines()

    def close_all_engines(self):
        """关闭所有数据库引擎"""
        for name, engine in self._engines.items():
            try:
                engine.dispose()
                logger.info(f"🔒 数据库引擎 '{name}' 已关闭")
            except Exception as e:
                logger.warning(f"⚠️ 关闭数据库引擎 '{name}' 时出错: {e}")

        self._engines.clear()
        self._sessionmakers.clear()

    def _initialize_engines(self):
        """初始化所有数据库引擎"""
        logger.info(f"开始初始化数据库引擎...")

        for db_name, db_config in self._config.DATABASES.items():
            try:
                # 创建引擎
                engine = create_engine(
                    db_config.URL,
                    pool_size=db_config.POOL_SIZE,
                    max_overflow=db_config.MAX_OVERFLOW,
                    pool_recycle=db_config.POOL_RECYCLE,
                    echo=db_config.ECHO,
                    future=True
                )

                self._engines[db_name] = engine
                self._sessionmakers[db_name] = sessionmaker(bind=engine)

                logger.info(f"✅ 数据库引擎 '{db_name}' 初始化成功")

            except Exception as e:
                logger.error(f"❌ 数据库引擎 '{db_name}' 初始化失败: {e}")
                raise EngineError(f"数据库 {db_name} 初始化失败: {e}")

        for db_name, db_config in self._config.OCEANBASES.items():
            try:
                # 创建引擎
                engine = JayDeBeEngine(
                    jdbc_driver_name=db_config.DRIVER,
                    jdbc_url=db_config.JDBC,
                    jdbc_user=db_config.USERNAME,
                    jdbc_password=db_config.PASSWORD,
                    jdbc_jar=db_config.CLIENT_JAR
                )

                self._engines[db_name] = engine
                self._sessionmakers[db_name] = sessionmaker(bind=engine)

                logger.info(f"✅ 数据库引擎 '{db_name}' 初始化成功")

            except Exception as e:
                logger.error(f"❌ 数据库引擎 '{db_name}' 初始化失败: {e}")
                raise EngineError(f"数据库 {db_name} 初始化失败: {e}")

    def _get_sessionmaker(self, db_name: str) -> Any:
        """获取会话工厂"""
        if db_name not in self._sessionmakers:
            raise EngineError(f"会话工厂 '{db_name}' 不存在")

        return self._sessionmakers[db_name]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all_engines()


# 全局引擎管理器实例
_global_engine_manager: Optional[DatabaseEngineManager] = None


def get_engine_manager(env_file: Optional[str] = None) -> DatabaseEngineManager:
    """获取全局引擎管理器"""
    global _global_engine_manager
    if _global_engine_manager is None:
        _global_engine_manager = DatabaseEngineManager(env_file)
    return _global_engine_manager


def set_global_engine_manager(env_file: Optional[str] = None):
    """设置全局引擎管理器"""
    global _global_engine_manager
    _global_engine_manager = DatabaseEngineManager(env_file)