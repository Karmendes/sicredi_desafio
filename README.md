# Arquitetura

![](arquitetura.png)

# Como usar
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





