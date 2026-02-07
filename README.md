# DB Grab SDK

DB Grab SDK 是一个用于内部数据源 的 SQL 数据获取/采集的工具，提供了便捷的数据库数据导出pandas csv的功能。

## 功能特性

- 基于SQLAlchemy,支持多种数据库，添加OceanBase支持
- 提供统一的数据获取接口
- 支持大数据量的分批读取和导出
- 内置日志记录功能
- 灵活的配置方式（支持.yml和.env配置文件）
- 支持从上次中断处继续采集数据
- 提供引擎管理器，统一管理多数据库连接
- 支持T+1模式、指定日期范围和迭代抽取模式

## 安装

```bash
# 从源码安装
pip install -e .

```

tips: 安装java jdk，设置JAVA_HOME, 以便采集 oceanbase 数据库

## 快速开始

### 1. 使用 ConfigGenerator 生成SQL配置的模板

```python
from dbgrab import ConfigGenerator

ENV_FILE_PATH = "/YOUR_PATH/.env"
SQL_FILE_PATH = "/YOUR_PATH/sql.yml"

# 初始化配置生成器
generator = ConfigGenerator()

# 生成env配置的模板
generator.gen_env_template(ENV_FILE_PATH)

# 生成SQL配置的模板
generator.gen_sql_template(SQL_FILE_PATH)  

```

### 4. 使用抓取器 DataBaseFetcher 采集数据

```python
from dbgrab import log
from dbgrab.dt_fetcher import DataBaseFetcher

env_file= ".env"  # generator 生成模板
sql_file= "sql.yml"  # generator 生成模板

# 设置日志（可选） - 数据量较大时建议配置，可根据日志断点，继续配置采集
log_file = "logs/your_fetcher.log"
log.to_file(log_file)

# 初始化数据库抓取器并加载配置
dbf = DataBaseFetcher(env_file, sql_file)
# Output Example:
# xxxx: SQL Tables List: dict_keys(['credible_db.fetcher_task_record', 'user.info'])
# xxxx: Engines List: dict_keys(['CREDIBLE', 'USER'])

# 方法1：使用 T+1 模式采集导出
print(dbf.with_engine("CREDIBLE").to_csv(table_name='credible_db.fetcher_task_record', T_1=True))

# 方法2：指定日期范围导出 - start_date, end_date参数，会自动替换tables.yml配置的sql
print(dbf.with_engine("CREDIBLE").to_csv(table_name='credible_db.fetcher_task_record', start_date="20250818", end_date="20251026"))

# 方法3：使用迭代方式导出大数据 - 可在时间段内，按天、月、年的模式导出，建议数据量级在千万级以上时使用
print(dbf.with_engine("CREDIBLE").to_csv_iter(table_name='credible_db.fetcher_task_record', start_date="20250818", end_date="20251026", mode="day"))
```

### 3. 使用提取器 DataExtractor 采集数据

```python
from dbgrab import DataExtractor, check_data, get_engine_manager

env_file= ".env"  # generator 生成模板

# 初始化引擎管理器
manager = get_engine_manager(env_file)

# 查看所有引擎
manager.list_engines()

# 获取指定引擎
engine = manager.get_engine("ENGINE_NAME")

# 配置SQL查询语句
sql_query = "select * from YOUR_DB.DB limit 1000"  # Mysql SQL
# sql_query = "SELECT * FROM YOUR_DB.DB t where ROWNUM <= 1000"  # OceanBase SQL

# 检查数据量
sql_query_count = sql_query.lower().replace('select * from', "select count(*) from")
max_info = check_data(engine, sql_query_count)
print("Count总数: ", max_info)

# 创建抽取器对象, 设置工作路径和引擎
dte = DataExtractor(engine, manager._config.WORK_PATH)  # manager._config 即 get_db_config返回的 DynamicDBConfig 类的实例

# 配置抽取器执行时的，输出文件文件名及SQL
dte.extractor.set_file("credible_test").to_csv(sql_query, chunk_size=20000)

```

### 配置文件

项目使用 .env 配置文件管理数据库连接信息：

```python
from dbgrab.configs import get_db_config

# 读取.env配置
config = get_db_config(".env")
print(f"数据模型配置: {config.model_config}")
print(f"数据库配置: {config.DATABASES.keys()}")
print(f"OceanBase配置: {config.OCEANBASES.keys()}")

```

### 引擎管理器

```python
from dbgrab.jaydebe import get_engine_manager

# 获取引擎管理器
manager = get_engine_manager(".env")

# 列出所有引擎信息
engines = manager.list_engines()
print("已配置的数据库引擎:")
for name, info in engines.items():
    print(f"  🔹 {name}: {info}")

# 获取指定的引擎
engine = manager.get_engine(f"{name}")

# 重新加载引擎配置
manager.reload_engines()

# 关闭所有引擎
manager.close_all_engines()
```

## 核心组件

### DataBaseFetcher
- 提供统一的数据获取接口
- 支持普通模式和迭代模式
- 自动处理数据分批和导出
- 支持 T+1 模式的数据获取
- 支持通过 `with_config` 方法加载配置
- 支持从上次中断处继续采集数据

### DataExtractor
- 提供基本的数据提取功能
- 支持通过引擎实例直接执行SQL
- 内置文件命名和路径管理
- 支持自定义 chunk_size 进行分批读取

### ConfigGenerator
- 基于模板生成配置文件
- 支持获取模板到当前目录
- 提供灵活的配置生成选项

### 引擎管理器
- `get_engine_manager`：获取引擎管理器实例
- 支持从 .env 文件加载配置
- 统一管理多数据库连接
- 提供 `list_engines`、`get_engine`、`get_session` 等方法
- 支持自动关闭所有引擎

### 配置管理
- `get_db_config`：从 .env 文件获取配置
- 支持管理多个数据库配置
- 支持管理 OceanBase 数据库配置

### 工具函数
- `check_data`：检查数据量
- `get_month_start_end_dates`：获取月份起止日期
- `get_year_start_end_dates`：获取年份起止日期
- `get_day_dates`：获取每天的日期

### 日志功能
- `log`：日志工具
- 支持输出到文件
- 提供统一的日志接口

## 配置说明

SDK 提供了灵活的配置方式，支持使用 .yml 文件和 .env 文件进行管理：

### 1. 使用 .env 配置文件

- ENV配置文件，**使用大写字母进行配置**

示例 .env 文件：

```dotenv
# 数据库配置
DB_ENGINE_DATABASES__MAIN__NAME=main
DB_ENGINE_DATABASES__MAIN__URL=mysql+pymysql://user:password@localhost:3306/main_db

# 日志数据库 (SQLite)
DB_ENGINE_DATABASES__LOG__NAME=log
DB_ENGINE_DATABASES__LOG__URL=sqlite:///./logs.db
DB_ENGINE_DATABASES__LOG__ECHO=false

# Ocean Base oracle模式
DB_ENGINE_OCEANBASES__USER__JDBC=jdbc:oceanbase://localhost:2883/OCEANBASE_DB?useUnicode=true&characterEncoding=UTF-8&rewriteBatchedStatements=true
DB_ENGINE_OCEANBASES__USER__USERNAME=user
DB_ENGINE_OCEANBASES__USER__PASSWORD=password
DB_ENGINE_OCEANBASES__USER__DRIVER=com.oceanbase.jdbc.Driver
DB_ENGINE_OCEANBASES__USER__CLIENT_JAR=/soft/oceanbase/oceanbase-client-2.4.9.jar

# 配置工作路径
DB_ENGINE_WORK_PATH=/opt/db_grab
DB_ENGINE_LOG_PATH=/opt/db_grab/logs
DB_ENGINE_FILE_PATH=/opt/db_grab/files
DB_ENGINE_DEBUG=false
```

- **配置使用前缀 `DB_ENGINE_` 用于区分不同的配置项**，避免与其他环境变量冲突。

如：`DB_ENGINE_DATABASES__MAIN__*` 为嵌套结构，会被解析为 MAIN数据库的配置

**配置文件，示例结构：**

```
DATABASES: {
  'MAIN': DatabaseConfig(NAME='main', URL='mysql+pymysql://user:password@localhost:3306/main_db', ...), 
  'LOG': DatabaseConfig(NAME='log', URL='sqlite:///./logs.db', DRIVER=None, POOL_SIZE=5, MAX_OVERFLOW=10, POOL_RECYCLE=3600, ECHO=False)
}，
OCEANBASES: {
  'USER': OceanbaseConfig(JDBC='jdbc:oceanbase://localhost:2883/OCEANBASE_DB?useUnicode=true&characterEncoding=UTF-8&rewriteBatchedStatements=true', ...), 
}，
'DEBUG': False,
'FILE_PATH': '/opt/db_grab/files',
'LOG_PATH': '/opt/db_grab/logs',
...
```

### 2. 使用 .yml 配置文件

**sql_file 配置文件结构：**

```yaml
# 表配置

tables:                             # 固定的字段
  SCHEMA.TABLE_NAME:                # 业务表名    
    db_alias: "oracle_engine"       # 字段已弃用
    desc: "表描述"                   # 业务表的描述
    filter: "过滤字段"               # 字段已弃用
    sql: |                          # SQL语句  - {start_date} 和 {end_date} 固定格式， DataBaseFetcher会自动替换
      SELECT  column1 AS column1
             ,column2 AS column2
      FROM SCHEMA.TABLE_NAME
      WHERE {filter} >= '{start_date}'
      AND {filter} <= '{end_date}'
      order by column1
```


### 3. 使用 JayDeBeConfig 加载配置
```python
from dbgrab.cons import JayDeBeConfig

j_conf = JayDeBeConfig(env_file=env_file, sql_file=sql_file)
print(f"SQL配置： {j_conf.sql_config}")
print(f"引擎管理器： {j_conf.manager}")
print(f"ENV配置： {[i for i in dir(j_conf.db_config) if i.isupper()]}")
```

## 注意事项

1. **配置文件准备**：使用前请确保已正确配置，可以使用ConfigGenerator 生成 env 和 yaml 文件配置模板
2. **环境变量设置**：使用 OceanBase 时，需要确保已正确配置 JAVA_HOME 环境变量
3. **大数据量处理**：对于大数据量的查询，建议使用迭代模式（to_csv_iter）和适当的 chunk_size 参数
4. **日志配置**：建议在使用前配置日志文件，以便于排查问题
5. **OceanBase 配置**：使用 OceanBase 时，需要确保已正确配置 JDBC 驱动路径和相关参数
6. **路径设置**：确保工作目录（如 temp 目录）存在，以便存储日志和导出的 CSV 文件

