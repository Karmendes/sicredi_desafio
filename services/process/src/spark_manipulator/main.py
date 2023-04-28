from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--driver-class-path driver/postgresql-42.6.0.jar pyspark-shell'


class SparkManipulator:
    def __init__(self,app_name = "default"):
        # cria uma nova sessão Spark
        self.spark = SparkSession.builder.appName(app_name).config("spark.jars", "driver/postgresql-42.6.0.jar").getOrCreate()
        self.data = {}

        self.spark.sparkContext.setLogLevel("ERROR")
    
    def read_from_jdbc(self,table,url,user,pwd,driver):
        self.data[table] = self.spark.read.jdbc(url=url, table=table, properties={"user": user, "password": pwd, "driver": driver})
    
    def rename_columns(self,table,old_name,new_name):
        self.data[table] = self.data[table].withColumnRenamed(old_name, new_name)
    def join_tables(self,table_1,table_2,on,how):
        self.data['join'] = self.data[table_1].join(self.data[table_2],on,how)
    def select_columns(self,table,list_columns):
        self.data[f'{table}_selected'] = self.data[table][list_columns]
    def write_data_partitioned(self,table,column_partition,dest_name,ext = "csv"):
        if ext == "csv":
            self.data[table].write.partitionBy(column_partition).mode("append").csv(dest_name)

    

