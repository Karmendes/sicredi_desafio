from src.library.db_connection.connect_db import ConnectDB
from src.library.faker.faker_data import FakerCreator

# Instanciado 
faker = FakerCreator(10)
connector = ConnectDB("sicredi_user","sicredi123","sicredi")

# Fazendo
faker.create_data()
connector.send_data_from_list_dicts("associado",faker.associado)
connector.send_data_from_list_dicts("conta",faker.conta)
connector.send_data_from_list_dicts("cartao",faker.cartao)
connector.send_data_from_list_dicts("movimento",faker.movimentacao)

