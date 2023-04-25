from faker import Faker
import random
import datetime

# Cria uma instância do Faker para gerar dados aleatórios

class FakerCreator:
    def __init__(self,qtd):
        self.faker = Faker()
        self.associado = []
        self.conta = []
        self.cartao = []
        self.movimentacao = []
        self.qtd = qtd

    def create_fake_data_associado(self):
        for i in range(self.qtd):
            data = {
                'nome': self.faker.first_name(),
                'sobrenome' : self.faker.last_name(),
                'idade' : random.randint(18, 80),
                'email' : self.faker.email()
            }
            self.associado.append(data)
        self.create_fake_data_conta()
    
    def create_fake_data_conta(self):
        for i in range(self.qtd):
            data = {
                'tipo': random.choice(['poupanca', 'corrente']),
                'data_criacao': self.faker.date_time_between(start_date='-5y', end_date='now'),
                'id_associado': i + 1
            }
            self.conta.append(data)
        self.create_fake_data_cartao()
    
    def create_fake_data_cartao(self):
        for i in range(self.qtd):
            data = {'num_cartao': self.faker.credit_card_number(),
               'nom_impresso': self.associado[i]['nome'] + ' ' + self.associado[i]['sobrenome'],
               'id_conta': i + 1,
               'id_associado': i + 1}
            self.cartao.append(data)
        self.create_fake_data_movimentacao()

    def create_fake_data_movimentacao(self):
        for i in range(self.qtd * 100):
            data = {
                'vlr_transacao': round(random.uniform(10.0, 500.0), 2),
                'data_movimento': self.faker.date_time_between(start_date='-1y', end_date='now'),
                'id_cartao': random.randint(1, 10)
                }
            self.movimentacao.append(data)
    
    def create_data(self):
        self.create_fake_data_associado()
    
if __name__ == "__main__":
    faker = FakerCreator(10)
    faker.create_data()
    #print(f"Faker Associados{faker.associado}")

