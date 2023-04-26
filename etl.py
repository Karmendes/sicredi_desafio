from src.library.spark_manipulator.main import SparkManipulator
from src.library.logger.main import Logger



jdbc_cred = {
    "url" :"jdbc:postgresql://localhost:5432/sicredi",
    "driver" : "org.postgresql.Driver",
    "user" :"sicredi_user",
    "password" :"sicredi123"
}

folder_dest = "data/"

class ETLSpark:
    def __init__(self,jdbc_cred = None,folder_dest = None):
        self.creds = jdbc_cred
        self.folder_dest = folder_dest
        self.spark = SparkManipulator()

    def extract(self,table):
        Logger.emit(f"Extraindo tabela {table}")
        self.spark.read_from_jdbc(table,self.creds['url'],self.creds['user'],self.creds['password'],self.creds['driver'])
    
    def extract_all(self,list_tables):
        for table in list_tables:
            self.extract(table)
        self.transform()

    def transform(self):
        ## Step 1
        Logger.emit(f"Passo 1: Renomeando chaves primárias")
        self.spark.rename_columns("conta","id","id_conta")
        self.spark.rename_columns("cartao","id","id_cartao")
        self.spark.rename_columns("associado","id","id_associado")
        ## Step 2
        Logger.emit(f"Passo 2: Fazendo join das tabelas")
        self.spark.join_tables("cartao","conta",["id_conta"],"inner")
        self.spark.join_tables("join","associado",["id_associado"],"inner")
        self.spark.join_tables("join","movimento",["id_cartao"],"left")
        ## Step 3
        Logger.emit(f"Passo 3: Selecionando colunas")
        self.spark.select_columns("join",["vlr_transacao",
        "data_movimento","num_cartao","nom_impresso","tipo","data_criacao","nome","sobrenome","idade"])
        ## Step 4
        Logger.emit(f"Passo 3: Renomeando para colunas para nomes oficiais")
        self.spark.rename_columns('join_selected',"vlr_transacao","vlr_transacao_movimento")
        self.spark.rename_columns('join_selected',"nom_impresso","nom_impresso_cartao")
        self.spark.rename_columns('join_selected',"tipo","tipo_conta")
        self.spark.rename_columns('join_selected',"data_criacao","data_criacao_conta")
        self.spark.rename_columns('join_selected',"nome","nome_associado")
        self.spark.rename_columns('join_selected',"sobrenome","sobrenome_associado")
        self.spark.rename_columns('join_selected',"idade","idade_associado")

        self.load_partitioned("join_selected")
    def load_partitioned(self,table):
        self.spark.write_data_partitioned(table,"nome_associado",self.folder_dest)
        Logger.emit(f"Dados salvos")
    def run(self,list_tables):
        Logger.emit(f"Inicializando ETL")
        self.extract_all(list_tables)
        Logger.emit(f"Finalizando ETL")

if __name__ == "__main__":
    etl = ETLSpark(jdbc_cred,folder_dest)
    etl.run(["associado","conta","cartao","movimento"])

        













































# os.environ['PYSPARK_SUBMIT_ARGS'] = '--driver-class-path postgresql-42.6.0.jar pyspark-shell'

# # cria uma nova sessão Spark
# spark = SparkSession.builder.appName("Exemplo PySpark").config("spark.jars", "postgresql-42.2.14.jar").getOrCreate()

# # configura as informações de conexão com o banco de dados
# url = "jdbc:postgresql://localhost:5432/sicredi"
# driver = "org.postgresql.Driver"
# user = "sicredi_user"
# password = "sicredi123"

# # cria um DataFrame 
# df_associado = spark.read.jdbc(url=url, table="associado", properties={"user": user, "password": password, "driver": driver})
# df_conta = spark.read.jdbc(url=url, table="conta", properties={"user": user, "password": password, "driver": driver})
# df_cartao = spark.read.jdbc(url=url, table="cartao", properties={"user": user, "password": password, "driver": driver})
# df_movimento = spark.read.jdbc(url=url, table="movimento", properties={"user": user, "password": password, "driver": driver})

# # Substituindo os nomes dos ids
# df_conta = df_conta.withColumnRenamed('id', 'id_conta')
# df_cartao = df_cartao.withColumnRenamed('id', 'id_cartao')
# df_associado = df_associado.withColumnRenamed('id', 'id_associado')


# # Juntar os dados
# df_join = df_cartao.join(df_conta,["id_conta"],"inner")
# df_join = df_join.join(df_associado,["id_associado"],"inner")
# df_join = df_movimento.join(df_join,["id_cartao"],"left")

# # Selecionando colunas
# df_dest = df_join.select(
#     col("vlr_transacao").alias("vl_transacao_movimento"),
#     col("data_movimento"),
#     col("num_cartao"),
#     col("nom_impresso").alias("nom_impresso_cartao"),
#     col("tipo").alias("tipo_conta"),
#     col("data_criacao").alias("data_criacao_conta"),
#     col("nome").alias("nome_associado"),
#     col("sobrenome").alias("sobrenome_associado"),
#     col("idade").alias("idade_associado")
#     )

# # salva o resultado em um arquivo CSV
# df_dest.write.partitionBy('nome_associado').csv('data/')

