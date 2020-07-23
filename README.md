# SageMakerWithFEDB

make a realtime ml application on sage maker with fedb

![arch](/images/arch.png)

## 下载依赖和数据

下载jar包
```
wget https://storage.4paradigm.com/api/public/dl/euvK52oV/fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar
aws s3 cp fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar {你的s3目录}
```
这里上传的s3路径将在后面使用

## 下载例子数据上传到s3

```
wget https://storage.4paradigm.com/api/public/dl/EZ55KLMS/train_data.snappy.parquet
aws s3 cp train_data.snappy.parquet {你的s3目录}
```

## 执行特征处理任务

### 创建emr集群并且登陆到master节点

在aws上面选择Spark2.4.4集群创建，然后通过ssh登陆到集群的master节点, 如何登陆到master请参考[aws ssh 登陆到emr master节点](https://docs.amazonaws.cn/emr/latest/ManagementGuide/emr-connect-master-node-ssh.html)

### 提交任务

```
git clone https://github.com/4paradigm/SageMakerWithFEDB.git
cd SageMakerWithFEDB
# 将s3上面的包下载下来
aws s3 cp s3://xxxxx/fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar .
```

更新fe.py 里面`fe_input` 变量为 `train_data.snappy.parquet` 在s3上面的路径 和 更新`fe_output` 变量为你的一个s3目录，用于保存特征输出结果
```
# 通过spark-submit提交任务到yarn集群
sh fe.sh
```

## 入群交流

![交流群](/images/code.png)



