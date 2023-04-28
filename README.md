# Arquitetura

![](arquitetura.png)

# Como usar

A estrutura do projeto consiste em duas partes. Dentro da pasta services, há duas outras pastas que tem a divisão entre o banco de dados e os processos. Na raíz ainda, também temos o docker-compose que levanta os serviços.

Na pasta de banco de dados, há o dockerfile de inicialização de um postgres e um arquivo sql com a criação do banco e do formato das tabelas.

Já na pasta process, há dois arquivos, **populate_db.py** que contém a lógica de carregamento dos dados fakes para o banco e também temos o arquivo **etl.py**, que contém a lógica para o processamento desses dados. Ambos são suportados pelas classes que estão no caminho **src/library**, que contém as classes para o projeto. Há também na pasta **process**, o dockerfile que monta a imagem base para que os dois processos rodem.

Certifique - se que você possua o docker e o docker compose instalado na sua máquina. Também certifique que você esteja na raíz do projeto

```

docker-compose up

```

Este comando irá instanciar três serviços: 
- **postgresdb**: banco de dados que irá conter os dados fictícios. 
- **python**: Processo que carrega os dados fake para dentro do banco
- **spark**: Processo que faz o ETL dos dados.

O final do processo irá gerar os dados na pasta **data** com formato csv, que está no caminho sicredi_desafio/services/process/data/ particionado pelo nome do cliente.



# Melhorias

## Dados Fakes
Decidi pela simplicidade na criação dos dados, ou seja, cada cliente tem somente uma conta e um cartão associado. E os IDs dos mesmos foram contruidos de forma sequencial para que não ocorresse nenhum descasamento. Com mais tempo criaria outros métodos para criar relações N X N.

## CI/CD
Usando actions do github, poderiamos colocar uma action para toda vez que ocorre - se um push na main, tivessemos um build da imagem para posterior deploy.

## Imagem menor
Tentaria usar alguma imagem menor para a base que usei nos processos do spark e python.





