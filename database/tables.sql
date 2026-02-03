CREATE TABLE operadoras (
    cnpj VARCHAR(14) PRIMARY KEY,
    razao_social TEXT NOT NULL,
    registro_ans VARCHAR(20),
    modalidade TEXT,
    uf CHAR(2)
);

CREATE TABLE despesas_consolidadas (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(14) REFERENCES operadoras(cnpj),
    ano INT NOT NULL,
    trimestre INT NOT NULL,
    valor_despesas DECIMAL(15,2) NOT NULL
);

CREATE INDEX idx_despesas_cnpj ON despesas_consolidadas(cnpj);
CREATE INDEX idx_despesas_periodo ON despesas_consolidadas(ano, trimestre);

CREATE TABLE despesas_agregadas (
    cnpj VARCHAR(14),
    uf CHAR(2),
    total_despesas DECIMAL(15,2),
    media_trimestral DECIMAL(15,2),
    desvio_padrao DECIMAL(15,2)
);