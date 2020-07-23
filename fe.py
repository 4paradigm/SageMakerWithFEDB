#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
from fespark.sql import SparkSession

fe_input="s3://"
fe_output=""
spark = SparkSession.builder.appName("Dataframe demo").getOrCreate()
train = spark.read.parquet(fe_input)
train.createOrReplaceTempView("t1")
sql_tpl = """select trip_duration, passenger_count,
sum(pickup_latitude) over w as vendor_sum_pl,
max(pickup_latitude) over w as vendor_max_pl,
min(pickup_latitude) over w as vendor_min_pl,
avg(pickup_latitude) over w as vendor_avg_pl,
sum(pickup_latitude) over w2 as pc_sum_pl,
max(pickup_latitude) over w2 as pc_max_pl,
min(pickup_latitude) over w2 as pc_min_pl,
avg(pickup_latitude) over w2 as pc_avg_pl ,
count(vendor_id) over w2 as pc_cnt,
count(vendor_id) over w as vendor_cnt
from {}
window w as (partition by vendor_id order by pickup_datetime ROWS_RANGE BETWEEN 1d PRECEDING AND CURRENT ROW),
w2 as (partition by passenger_count order by pickup_datetime ROWS_RANGE BETWEEN 1d PRECEDING AND CURRENT ROW)"""
train_sql = sql_tpl.format('t1')
train_df = spark.sql(train_sql)
train_df.write.csv(fe_output)

