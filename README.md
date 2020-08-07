# SageMakerWithFEDB

make a realtime ml application on sage maker with fedb

![arch](/images/arch.png)
- [SageMakerWithFEDB](#sagemakerwithfedb)
    - [执行特征处理任务](#执行特征处理任务)
        - [方法一：创建emr集群并且登陆到master节点](#方法一创建emr集群并且登陆到master节点)
            - [提交任务](#提交任务)
            - [得到特征](#得到特征)
        - [方法二：创建emr集群并且登陆到master节点](#方法二创建emr集群并且登陆到master节点)
            - [文件准备](#文件准备)
            - [提交任务](#提交任务-1)
            - [得到特征](#得到特征-1)
    - [Notebook模型预测](#notebook模型预测)
- [入群交流](#入群交流)

## 执行特征处理任务

### 方法一：创建emr集群并且登陆到master节点

在aws上面选择Spark2.4.4集群创建，然后通过ssh登陆到集群的master节点, 如何登陆到master请参考[aws ssh 登陆到emr master节点](https://docs.amazonaws.cn/emr/latest/ManagementGuide/emr-connect-master-node-ssh.html)
emr 版本请选择`emr-6.0.0`

#### 提交任务
```
git clone https://github.com/4paradigm/SageMakerWithFEDB.git
cd SageMakerWithFEDB
# 将s3上面的包下载下来
aws s3 cp s3://xxxxx/fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar .
#下载jar包
wget https://storage.4paradigm.com/api/public/dl/euvK52oV/fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar
wget https://storage.4paradigm.com/api/public/dl/EZ55KLMS/train_data.snappy.parquet
aws s3 cp train_data.snappy.parquet {你的s3目录}
```

更新fe.py 里面`fe_input` 变量为 `train_data.snappy.parquet` 在s3上面的路径 和 更新`fe_output` 变量为你的一个s3目录，用于保存特征输出结果
```
# 通过spark-submit提交任务到yarn集群
sh fe.sh
```
#### 得到特征
执行完成后在输出s3目录看到如下文件
```
_SUCCESS
partxxxxx.csv
...
```
则表示正确产生了特征输出


### 方法二：创建emr集群并且登陆到master节点
使用Livy建立Sagemaker Notebook与EMR的联系，为了方便在 Amazon SageMaker Notebook 与 Spark EMR 集群之间建立连接，需要使用 Livy。Livy 是一个开源 REST 接口，无需 Spark 客户端便可从任何位置与 Spark 集群交互。主要涉及到的产品有：

- EMR
- EC2
- Sagemaker Notebook
- S3

官网详细步骤文档：[在 Amazon EMR 中构建由 Spark 支持的 Amazon SageMaker Notebook](https://amazonaws-china.com/cn/blogs/china/build-amazon-sagemaker-notebooks-backed-by-spark-in-amazon-emr/)，参考此文档，您可以建立 sagemaker notebook 与 EMR spark 的连接，并接下来可以通过Livy进行任务提交。

#### 文件准备
首先需要创建s3存储桶（bucket）用于保存必要文件，在aws控制台顶部服务菜单中选择s3，创建过程中需要自定义存储桶名称与权限。
获取必需文件：
- fe.py (接下来需要更改设置数据的input和output路径)
- fespark.zip
- input数据（train_data.snappy.parquet）
- jar包（fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar）

为获取以上数据并将其保存到s3中，在 已经与EMR建立连接的 Sagemaker Notebook的笔记本终端运行以下命令：
```
git clone https://github.com/4paradigm/SageMakerWithFEDB.git
cd SageMakerWithFEDB
# 下载jar包和demo数据
wget https://storage.4paradigm.com/api/public/dl/euvK52oV/fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar
wget https://storage.4paradigm.com/api/public/dl/EZ55KLMS/train_data.snappy.parquet
```
文件下载后，更新fe.py 里面`fe_input` 变量为 `train_data.snappy.parquet` 在s3上面的路径 和 更新`fe_output` 变量为你的一个s3目录，用于保存特征输出结果。
```
nano fe.py
# 编辑路径
ctrl+x
y
enter
```
并将数据转存到s3中。
```
aws s3 cp fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar {你的s3目录}
aws s3 cp train_data.snappy.parquet {你的s3目录}
aws s3 cp fe.py {你的s3目录}
aws s3 cp fespark.zip {你的s3目录}
```
至此，您上传任务所需要的文件模块已经准备好了，您同时可以在s3的服务界面中可以看到上传的文件。

#### 提交任务
```
curl -X POST --data '{"file": "s3://xxx/fe.py", "className": "com.example.SparkApp", "jars":["s3://xxx/fespark.jar"], "pyFiles": ["s3://xxx/fespark.zip"], "numExecutors":2, "executorCores":1, "executorMemory":"4G", "driverMemory":"4G"}' -H "Content-Type: application/json" <EMR 主实例私有 IP> :8998/batches
```
其中<EMR 主实例私有 IP>可以换为 http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com （在EMR集群中可找到的DNS）

![Notebook终端](/images/livy.png)

可以使用如下命令查看log信息：
```
curl <EMR 主实例私有 IP>:8998/batches | python -m json.tool
```
#### 得到特征
执行完成后在输出s3目录看到如下文件
```
_SUCCESS
partxxxxx.csv
...
```
则表示正确产生了特征输出


## Notebook模型预测
在文件夹中找到 train-linear.ipynb，再打开您在上一步中创建的笔记本实例 jupyter，点击右上侧的 upload 上传到您的笔记本实例中。进入文件，根据在Part1中数据的存储位置修改您的存储桶（bucket）和键位置（key）
```
bucket = '' # set your bucket
key = '' # set your prefix
data_loc = 's3://{}/{}'.format(bucket, key)
train_file = data_loc+'/xxx.csv' # set your train file name
output_location = 's3://{}/{}'.format(bucket, 'model')
```
点击 运行，此过程可能花费几分钟的时间，请保持耐心。在最后test阶段，如果能够输出：
```
{'predictions': [{'score': 783.171875}]}
```
则运行成功！


## 入群交流

![交流群](/images/code.png)



