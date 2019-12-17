* 程序
```
influxd          influxdb服务器
influx           influxdb命令行客户端
influx_inspect   查看工具
influx_stress    压力测试工具
influx_tsm       数据库转换工具（将数据库从b1或bz1格式转换为tsm1格式）    
```

* 对照
```
database    : 'schema' in mysql
measurement : 'table' in mysql
points      : one row in table

point : 
   <time>   : 自动生成, 相当于 primary key
   <tags>   : 有索引, 比如'地区',   当某一行的<time>+<tags>完全相同时,新数据会覆盖旧数据
   <field>  : 无索引, 比如'温度', '湿度'

查询时,<time>, <tags>可以用来排序, <field>不可以排序
<tags>, <field>的类型,由第一条插入数据决定,之后如果类型变化,可能报错.

retention policy : 保存策略, 时间到了就定期清除旧数据
设定了保存策略之后,如果不是'缺省 保存策略',查询的时候,要在前面加上这个策略名称
比如 策略为 two-hour,不是缺省,查询时需要
select * from two-hour.measure where time > now() -10 

series      : series表示这个表里面的数据，可以在图表上画成几条线，series主要通过tags排列组合算出来。



```
* 基本命令
```
create database       db_name_1
show   databases
drop   database       db_name_1
use                   db_name_1

SHOW RETENTION POLICIES ON     db_name_1

# will get
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        true


name                  --名称
duration              --持续时间，0代表无限制
shardGroupDuration    --shardGroup的存储时间，shardGroup是InfluxDB的一个基本储存结构，应该大于这个时间的数据在查询效率上应该有所降低。
replicaN              --全称是REPLICATION，副本个数
default               --是否是默认策略?

```

```
show measurements
drop measurement "measurement_name"

insert test,host=127.0.0.1,monitor_name=test count=1

insert disk_free,hostname=server01 value=442221834240i 1435362189575692182

insert disk_free,hostname=server01,tag2=v2,tag3=v3,tag4=v4 value=1234i 1435362189575692182

# 1435362189575692182 is timestamp

insert disk_free,hostname=server01,tag2=v2,tag3=v3,tag4=v4_2 value=1234i 


InfluxDB的insert中，
表名与数据之间用逗号（,）分隔，
tag和field之间用 空格分隔，
多个tag或者多个field之间用逗号（,）分隔。

```

* 保存策略
```
新建/修改/删除 '保存策略'
CREATE RETENTION POLICY "2_hours" ON "db_name_1" DURATION 2h REPLICATION 1 DEFAULT


SHOW RETENTION POLICIES ON db_name_1
# get
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        false
2_hours 2h0m0s   1h0m0s             1        true


select * from "2_hours".disk_free limit 2


ALTER RETENTION POLICY "2_hours" ON "db_name_1" DURATION 4h DEFAULT
drop retention POLICY "2_hours" ON "db_name_1"

# 策略这个关键词“POLICY”在使用是应该大写，小写应该会出粗。
# 当一个表使用的策略不是默认策略时，在进行操作时一定要显式的指定策略名称，否则会出现错误。

```
* 连续查询(CONTINUOUS QUERY)
  * 自动启动查询
  * 包括`SELECT`与`GROUP BY`
  * 结果存在指定的表里
  * e.g. 示例在telegraf库中新建了一个名为 cq_30m 的连续查询，每三十分钟取一个used字段的平均值，加入 mem_used_30m 表中。使用的数据保留策略都是 default。

   * 将连续查询与数据存储策略一起使用会达到最好的效果。比如，
      * 将精度高的表的存储策略定为一个周，
      * 然后将精度底的表存储策略定的时间久一点，
      * 这样就可以实现高低搭配，以满足不同的工作需要。
   * 可以使用RESAMPLE FOR 关键词来指定连续查询的时间范围，比如，每次执行都对1小时内的数据进行连续查询。。。。。。这个语句每次会将1小时的数据执行连续查询，也就是说，每次执行时，会将now()到now()-30m和now()-30m到now()-60m分别做连续查询，这样我们就可以手动指定连续查询的时间范围了。
   * 可以使用RESAMPLE EVERY 关键词来指定连续查询的执行频次，比如，指定连续查询的执行频次为每15m执行一次。。。这样，连续查询会每隔15m执行一次。
   * 将RESAMPLE FOR 和 EVERY关键词同时使用，可以同时指定连续查询的范围和频次，。。。这个语句指定连续查询每15m执行一次，每次执行的范围为60m。

   * reference : 
   * https://www.linuxdaxue.com/influxdb-continuous-queries.html
   * https://www.linuxdaxue.com/influxdb-continuous-queries-senior-knowlage.html 

* 聚合函数
```
# COUNT
SELECT COUNT(<field_key>) FROM <measurement_name> [WHERE <stuff>] [GROUP BY <stuff>]

SELECT COUNT(water_level) FROM h2o_feet

SELECT COUNT(water_level) FROM h2o_feet WHERE time >= '2015-08-18T00:00:00Z' AND time < '2015-09-18T17:00:00Z' GROUP BY time(4d)


# DISTINCT
SELECT DISTINCT(<field_key>) FROM <measurement_name> [WHERE <stuff>] [GROUP BY <stuff>]

SELECT DISTINCT("level description") FROM h2o_feet


# MEAN
SELECT MEAN(<field_key>) FROM <measurement_name> [WHERE <stuff>] [GROUP BY <stuff>]

SELECT MEAN(water_level) FROM h2o_feet


# MEDIAN
SELECT MEDIAN(<field_key>) FROM <measurement_name> [WHERE <stuff>] [GROUP BY <stuff>]

SELECT MEDIAN(water_level) from h2o_feet


# SPREAD
SELECT SPREAD(<field_key>) FROM <measurement_name> [WHERE <stuff>] [GROUP BY <stuff>]

SELECT SPREAD(water_level) FROM h2o_feet

# SUM
SELECT SUM(<field_key>) FROM <measurement_name> [WHERE <stuff>] [GROUP BY <stuff>]


SELECT SUM(water_level) FROM h2o_feet

# TOP/BOTTOM/FIRST/LAST/MAX/MIN/PERCENTILE/
# reference : https://www.linuxdaxue.com/influxdb-study-influxdb-selectors-funcitons.html

# DERIVATIVE/DIFFERENCE/ELAPSED/MOVING_AVERAGE/NON_NEGATIVE_DERIVATIVE/STDDEV
# reference : https://www.linuxdaxue.com/influxdb-study-influxdb-transformations-funcitons.html


```

* 备份数据
```
# 备份 元数据(系统信息,用户信息,等)
influxd backup <path-to-backup>

# 备份 数据库
influxd backup -database <mydatabase> <path-to-backup>

# 更多参数
-retention <retention policy name>
-shard <shard ID>
-since <date>

# 远程 备份
influxd backup -database mydatabase -host 10.0.0.1:8088 /tmp/mysnapshot


# 数据恢复
influxd restore [ -metadir | -datadir ] <path-to-meta-or-data-directory> <path-to-backup>

influxd restore -database telegraf -datadir /var/lib/influxdb/data /tmp/backup                                                                         


```

* reference
   * https://www.cnblogs.com/gaoguangjun/p/8513054.html
   * https://blog.csdn.net/x541211190/article/details/82950254
* <>

* <>