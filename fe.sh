spark-submit \
     --master local --deploy-mode client \
     --num-executors 1 \
     --executor-cores 1 \
     --driver-memory 1g \
     --executor-memory 1g \
     --py-files ./fespark.zip \
     --jars ./fesql-spark-0.0.1-SNAPSHOT-with-dependencies.jar \
     ./fe.py
