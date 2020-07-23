spark-submit \
     --master yarn --deploy-mode cluster \
     --num-executors 1 \
     --executor-cores 2 \
     --driver-memory 2g \
     --executor-memory 2g \
     --py-files ./fespark.zip \
     --jars ./fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar \
     ./fe.py

