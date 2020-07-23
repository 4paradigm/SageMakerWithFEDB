spark-submit \
     --master yarn --deploy-mode cluster \
     --num-executors 2 \
     --executor-cores 1 \
     --driver-memory 4g \
     --executor-memory 4g \
     --py-files ./fespark.zip \
     --jars ./fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar \
     ./fe.py

