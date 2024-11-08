import findspark
findspark.init()

from pyspark.sql import SparkSession

spark = sparkSession\
    .builder\
    .config('spark.app.name','learning_spark_sql')\
    .getOrCreate()

mh3_df = SparkSession.read\
.option('header',True)\
.option('inferSchema',True)\
.csv('merged_mh3_file_updated.csv')

mh3_df.show(20)