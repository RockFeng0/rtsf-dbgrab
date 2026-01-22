# DB Grab SDK

DB Grab SDK 是一个用于内部数据源 的 SQL 数据获取/采集的工具，提供了便捷的数据库数据导出pandas csv的功能。

## 功能特性

- 基于SQLAlchemy,支持多种数据库，添加OceanBase支持
- 提供统一的数据获取接口
- 支持大数据量的分批读取和导出
- 内置日志记录功能
- 灵活的配置方式
- 支持从上次中断处继续采集数据

## 安装

```bash
# 从源码安装
pip install -e .

```

## 快速开始

### 1. 使用 ConfigGenerator 生成配置文件

```python
from dbgrab import ConfigGenerator

# 初始化配置生成器
generator = ConfigGenerator()

# 获取数据库配置模板 
generator.get_database_template("dbconfig/database.yml")  # 保存到 dbconfig/database.yml

# 获取SQL配置模板 
generator.get_tables_template("dbconfig/tables.yml")  # 保存到 dbconfig/tables.yml

```

### 2. 检查数据库引擎配置和SQL模板

```python

from dbgrab.cons import j_conf

# 初始化数据库引擎
j_conf.init_engines(db_cfg_file="database.yml")
print(j_conf.DB_CONFIG)
print(j_conf.ENGINE_MAP)
print(j_conf.FETCH_FILE_PATH)

# 初始化SQL模板
j_conf.init_sql_template()
print(j_conf.SQL_CONFIG)

```

### 3. 使用抓取器 DataBaseFetcher 采集数据

```python
from dbgrab import DataBaseFetcher, log

# 设置日志（可选） - 数据量较大时建议配置，可根据日志断点，继续配置采集
log_file = "/root/logs/fetch.log"
log.to_file(log_file)

# 初始化数据库抓取器
dbf = DataBaseFetcher(db_alias="oracle_engine")  # db_alias参数，从database.yml配置文件中获取

# 方法1：使用 T+1 模式采集导出
print(dbf.to_csv(table_name='SCHEMA.TABLE_NAME', T_1=True))  # table_name参数，从tables.yml配置文件中获取

# 方法2：指定日期范围导出 - start_date, end_date参数，会自动替换tables.yml配置的sql
print(dbf.to_csv(table_name='SCHEMA.TABLE_NAME', start_date="20250818", end_date="20250826"))

# 方法3：使用迭代方式导出大数据 - 可在时间段内，按天、月、年的模式导出，建议数据量级在千万级以上时使用
print(dbf.to_csv_iter(table_name='SCHEMA.TABLE_NAME', start_date="20250814", end_date="20250815", index=1, mode="day"))
```

### 4. 使用提取器 DataExtractor 采集数据

```python
from dbgrab import DataExtractor, get_month_start_end_dates, check_data
from dbgrab.cons import j_conf

# 初始化引擎
config_file = "database.yml"
j_conf.init_engines(db_cfg_file=config_file)

# 获取引擎实例
ENGINE = j_conf.ENGINE_MAP.get("oracle_engine")

# 初始化提取器
dte = DataExtractor(ENGINE, j_conf.WORK_PATH)

# 准备SQL查询,使用提取器采集数据
sql_query = "select * from SCHEMA.TABLE_NAME t where to_char(t.create_date, 'yyyy-mm-dd') between '2025-08-01' and '2025-08-31'"
dte.extractor.set_file("filename").to_csv(sql_query, chunk_size=20000)

# 检查数据量
sql_query_count = sql_query.lower().replace('select * from', "select count(*) from")
max_info = check_data(ENGINE, sql_query_count)
print("Count总数: ", max_info)
```

## 核心组件

### DataBaseFetcher
- 提供统一的数据获取接口
- 支持普通模式和迭代模式
- 自动处理数据分批和导出
- 支持 T+1 模式的数据获取

### DataExtractor
- 提供基本的数据提取功能
- 支持通过引擎实例直接执行SQL
- 内置文件命名和路径管理

### ConfigGenerator
- 基于模板生成配置文件
- 支持获取模板到当前目录
- 提供灵活的配置生成选项

### 工具函数
- `check_data`：检查数据量
- `get_month_start_end_dates`：获取月份起止日期
- `get_year_start_end_dates`：获取年份起止日期
- `get_day_dates`：获取每天的日期

### 配置管理
- `j_conf`：全局配置对象
- 支持从配置文件初始化
- 管理数据库引擎实例

### 日志功能
- `log`：日志工具
- 支持输出到文件
- 提供统一的日志接口

## 配置说明

SDK 提供了灵活的配置方式，主要通过配置文件进行管理：

### 1. 配置文件结构

**database.yml** 配置文件示例：

```yaml
# 数据库引擎配置

# 基本路径配置
paths:
  work_path: /xx/xx                 # dbfetcher的工作目录，用于存储临时文件
  fetch_log_path: /xx/xx/logs       # DataBaseFetcher 采集数据日志的存储路径 - 字段已弃用
  fetch_file_path: /xx/xx/files     # DataBaseFetcher 采集数据文件的存储路径

# 数据库连接配置
databases:
  # PostgreSQL 配置1
  - alias: pg_engine1    #  引擎别名
    type: pg            #   创建引擎时，用于区分数据库类型，取值("pg", "oracle", "mysql", "sqlite", "oceanbase")
    uri: postgresql://username:password@host:port/database    #  用于SQLalchemy创建引擎实例
  
  # PostgreSQL 配置2
  - alias: pg_engine 2  
    type: pg            
    uri: postgresql://username:password@host:port/database

  # Oracle 配置
  - alias: oracle_engine
    type: oracle
    uri: oracle://username:password@host:port/?service_name=database

  # Mysql 配置
  - alias: mysql_engine
    type: mysql
    uri: mysql+pymysql://username:password@host:port/xx_database

  # SQLite 配置
  - alias: sqlite_engine
    type: sqlite
    uri: sqlite:///d:\\xxx\\xx\\xx.db

  # OceanBase Oracle模式的配置
  - alias: ob_engine    #  引擎别名
    type: oceanbase
    jdbc: ""            # jdbc URL, 如: jdbc:oceanbase://192.168.0.1:2883/TestDB?useUnicode=true&characterEncoding=UTF-8&rewriteBatchedStatements=true
    username: ""
    password: ""
    driver: ""          # 驱动名称, 如: com.oceanbase.jdbc.Driver
    jar: ""             # 驱动 JAR 文件路径, 如 /root/oceanbase-client-1.2.3.jar
```

**tables.yml** 配置文件示例：

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

### 2. 初始化配置

```python
from dbgrab.cons import j_conf

# 使用配置文件初始化
config_file = "database.yml"
j_conf.init_engines(db_cfg_file=config_file)

# 获取引擎实例
engine = j_conf.ENGINE_MAP.get("ob_engine")
```

## 注意事项

1. **配置文件准备**：使用前请确保已正确配置 database.yml 和 tables.yml 文件
2. **环境变量设置**：使用 OceanBase 时，需要确保已正确配置 JAVA_HOME 环境变量
   ```python
   import os
   os.environ["JAVA_HOME"] = "/path/to/java"
   ```
3. **大数据量处理**：对于大数据量的查询，建议使用迭代模式（to_csv_iter）和适当的 chunk_size 参数
4. **日志配置**：建议在使用前配置日志文件，以便于排查问题
   ```python
   from dbgrab import log
   log.to_file("fetch.log")
   ```
5. **OceanBase 配置**：使用 OceanBase 时，需要确保已正确配置 JDBC 驱动路径和相关参数

## 依赖

- sqlalchemy
- pandas
- jaydebeapi
- tqdm
- pyyaml

## 版本

当前版本：0.1.0
