# SageMakerWithFEDB

make a realtime ml application on sage maker with fedb

## 下载依赖和数据

下载jar包
```
cd Sagemakerwithfedb
wget https://storage.4paradigm.com/api/public/dl/euvK52oV/fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar
```

## 下载例子数据上传到s3

```
wget https://storage.4paradigm.com/api/public/dl/EZ55KLMS/train_data.snappy.parquet
aws s3 cp train_data.snappy.parquet {你的s3目录}
```
更新fe.py 里面`fe_input` 变量为 `train_data.snappy.parquet` 在s3上面的路径





