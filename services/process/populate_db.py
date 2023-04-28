from src.db_connection.connect_db import ConnectDB
from src.faker.faker_data import FakerCreator
from src.logger.main import Logger
from src.utils.main import load_json


# Importar credenciais
creds = load_json('credentials/creds.json')

# Instanciado
Logger.emit('Iniciando carregamento')
faker = FakerCreator(10)
connector = ConnectDB(creds['user'],creds["password"],creds['db'])



# Fazendo
Logger.emit('Criando os dados')
faker.create_data()
connector.send_data_from_list_dicts("associado",faker.associado)
Logger.emit('Dados de Associados carregados')
connector.send_data_from_list_dicts("conta",faker.conta)
Logger.emit('Dados de Conta carregados')
connector.send_data_from_list_dicts("cartao",faker.cartao)
Logger.emit('Dados de Cartão carregados')
connector.send_data_from_list_dicts("movimento",faker.movimentacao)
Logger.emit('Dados de Movimento carregados')

Logger.emit('Fim do carregamento')

