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

# Substituindo os nomes dos ids
df_conta = df_conta.withColumnRenamed('id', 'id_conta')
df_cartao = df_cartao.withColumnRenamed('id', 'id_cartao')
df_associado = df_associado.withColumnRenamed('id', 'id_associado')


# Juntar os dados
df_join = df_cartao.join(df_conta,["id_conta"],"inner")
df_join = df_join.join(df_associado,["id_associado"],"inner")
df_join = df_movimento.join(df_join,["id_cartao"],"left")

# Selecionando colunas
df_dest = df_join.select(
    col("vlr_transacao").alias("vl_transacao_movimento"),
    col("data_movimento"),
    col("num_cartao"),
    col("nom_impresso").alias("nom_impresso_cartao"),
    col("tipo").alias("tipo_conta"),
    col("data_criacao").alias("data_criacao_conta"),
    col("nome").alias("nome_associado"),
    col("sobrenome").alias("sobrenome_associado"),
    col("idade").alias("idade_associado")
    )

# salva o resultado em um arquivo CSV
df_dest.write.partitionBy('nome_associado').csv('data/')

