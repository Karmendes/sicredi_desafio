import psycopg2

class ConnectDB:
    def __init__(self,user,pwd,database,host= 'postgresdb',port = 5432):
        print(f"{host}")
        self.engine = psycopg2.connect(f'postgresql://{user}:{pwd}@{host}:{port}/{database}')    
        try:
            self.connection = self.engine.cursor()
        except Exception as ex:
            raise ConnectionError(f"Unable to stablish connection on {host}")
    def send_data_from_list_dicts(self,table,data):
        # Extrai as chaves de cada dicionário da lista de dados
        columns = list(data[0].keys())
        # Concatena as chaves separadas por vírgulas para a cláusula INSERT INTO
        columns_str = ', '.join(columns)
        # Constrói a cláusula VALUES dinamicamente com o número de elementos na lista de dados
        values_str = ', '.join(['%s'] * len(columns))
        # Concatena a cláusula INSERT INTO com a cláusula VALUES
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"
        # Cria uma lista de tuplas contendo os valores de cada linha
        values_list = [tuple(d.values()) for d in data]
        # Executa a query com os parâmetros recebidos
        self.connection.executemany(query, values_list)
        self.engine.commit()
