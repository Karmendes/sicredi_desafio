# Arquitetura

![](arquitetura.png)

# Requisitos
Docker

Docker-compose

Python >=3.10

# Como usar


## Projeto

Certifique - se que você está na raiz do projeto. O processo pode demorar 5 minutos, para buildar e rodar.



```
docker-compose up
```
**Disclaimer**: Talvez algum processo quebre no run, porém rodando de novo irá gerar os dados. Não consegui identificar a causa ainda.

Este comando irá instanciar três serviços: 
- **postgresdb**: banco de dados que irá conter os dados fictícios. 
- **python**: Processo que carrega os dados fake para dentro do banco
- **spark**: Processo que faz o ETL dos dados.

O final do processo irá gerar os dados na pasta **data** com formato csv, que está no caminho: **services/process/data/** particionado pelo nome do cliente.


## Testes

Certifique - se que você está na raiz do projeto.

```
python tests/test_core.py
```

# Melhorias

## Dados Fakes
Decidi pela simplicidade na criação dos dados, ou seja, cada cliente tem somente uma conta e um cartão associado. E os IDs dos mesmos foram contruidos de forma sequencial para que não ocorresse nenhum descasamento. Com mais tempo criaria outros métodos para criar relações N X N.

## CI/CD
Usando actions do github, poderiamos colocar uma action para toda vez que ocorre - se um push na main, tivessemos um build da imagem para posterior deploy.

## Imagem menor
Tentaria usar alguma imagem menor para a base que usei nos processos do spark e python.





