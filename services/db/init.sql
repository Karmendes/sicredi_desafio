

CREATE TABLE associado (
  id SERIAL PRIMARY KEY,
  nome VARCHAR (100),
  sobrenome VARCHAR (100),
  idade INT,
  email VARCHAR (100) 
);

CREATE TABLE conta (
  id SERIAL PRIMARY KEY,
  tipo VARCHAR (100),
  data_criacao TIMESTAMP,
  id_associado INT REFERENCES associado(id)
);


-- Cria a tabela cartão
CREATE TABLE cartao (
  id SERIAL PRIMARY KEY,
  num_cartao BIGINT,
  nom_impresso VARCHAR(100),
  id_conta INT REFERENCES conta(id),
  id_associado INT REFERENCES associado(id)
);

-- Cria a tabela "movimento"
CREATE TABLE movimento (
  id SERIAL PRIMARY KEY,
  vlr_transacao DECIMAL(10, 2),
  data_movimento TIMESTAMP,
  id_cartao INT REFERENCES cartao(id)
);




