from src.library.spark_manipulator.main import SparkManipulator
from src.library.logger.main import Logger
from time import sleep


jdbc_cred = {
    "url" :"jdbc:postgresql://postgresdb:5432/sicredi",
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


