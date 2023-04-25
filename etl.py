# TO DO: Fazer junções
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os


os.environ['PYSPARK_SUBMIT_ARGS'] = '--driver-class-path postgresql-42.6.0.jar pyspark-shell'

# cria uma nova sessão Spark
spark = SparkSession.builder.appName("Exemplo PySpark").config("spark.jars", "postgresql-42.2.14.jar").getOrCreate()

# configura as informações de conexão com o banco de dados
url = "jdbc:postgresql://localhost:5432/sicredi"
driver = "org.postgresql.Driver"
user = "sicredi_user"
password = "sicredi123"

# cria um DataFrame 
df_associado = spark.read.jdbc(url=url, table="associado", properties={"user": user, "password": password, "driver": driver})
df_conta = spark.read.jdbc(url=url, table="conta", properties={"user": user, "password": password, "driver": driver})
df_cartao = spark.read.jdbc(url=url, table="cartao", properties={"user": user, "password": password, "driver": driver})
df_movimento = spark.read.jdbc(url=url, table="movimento", properties={"user": user, "password": password, "driver": driver})

# Juntar os dados
df_join = df_cartao.join(df_conta,col("id_conta") == col("id"),"inner").join(df_associado)
df_join = df_join.join(df_cartao,col("id") == col("id_conta"),"inner")
df_join = df_movimento.join(df_join,col("id") == col("id_cartao"),"left")


# salva o resultado em um arquivo CSV
#df.write.csv("arquivo.csv", header=True, mode="overwrite")
