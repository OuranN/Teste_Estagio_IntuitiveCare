# Teste de Entrada – Intuitive Care  
**Candidato:** Cristhian Silveira  
**Stack:** Python 3.11 + PostgreSQL  

---

## Visão Geral

Este projeto implementa todas as etapas solicitadas no teste técnico da Intuitive Care, simulando um pipeline real de ingestão, tratamento, validação e análise de dados públicos da ANS.

| Etapa | Descrição |
|------|--------|
| Teste 1 | Coleta e consolidação dos dados da ANS |
| Teste 2 | Validação, enriquecimento e agregação |
| Teste 3 | Modelagem, carga e análises em banco de dados |

O foco foi criar uma solução lidando com dados governamentais inconsistentes e de grande volume.

---

# TESTE 1 – Integração com API Pública da ANS

## 1.1 Acesso à API

Foi utilizada a API pública da ANS disponível em: https://dadosabertos.ans.gov.br/FTP/PDA/

O sistema identifica automaticamente os **3 trimestres mais recentes disponíveis**.

Como os diretórios da ANS possuem estruturas variáveis, o código foi construído de forma resiliente, sem depender de nomes fixos.

---

## 1.2 Processamento dos Arquivos

Para cada trimestre:
- Todos os arquivos `.zip` são baixados
- Os arquivos são extraídos automaticamente
- Apenas arquivos contendo **Despesas com Eventos/Sinistros** são processados (pesquisando descobri que seriam os com código 41, 4 = despesa e 41 = despesa evento/sinistro)

### 1.2 – Trade-off técnico (memória vs processamento incremental)

**Decisão:** Processamento em memória.

Os três últimos trimestres somaram cerca de 380 mil registros após a extração dos CSVs. Esse volume é perfeitamente manejável em memória, o que permitiu usar DataFrames completos para filtrar, normalizar e consolidar os dados de forma simples e eficiente.

Essa abordagem reduz a complexidade do código, facilita a validação dos dados e torna o processo de consolidação mais direto, já que todos os trimestres podem ser cruzados e agregados no mesmo contexto.

Caso o volume de dados cresça significativamente no futuro, a solução pode ser facilmente adaptada para leitura incremental, sem necessidade de alterar a lógica principal do pipeline.

---

## 1.3 Consolidação e Inconsistências

Os dados foram normalizados para:

| Campo | Descrição |
|------|--------|
| CNPJ | Identificador da operadora |
| RazaoSocial | Nome da operadora |
| Ano | Ano de referência |
| Trimestre | Trimestre (1, 2 ou 3) |
| ValorDespesas | Valor financeiro |

### Tratamento de inconsistências

| Problema | Tratamento |
|--------|-----------|
CNPJs duplicados | Mantido o nome mais frequente |
Valores negativos | Mantidos, mas marcados como suspeitos |
Trimestres "1T", "2T" | Convertidos para 1, 2, 3 |

Arquivo final: *consolidado_despesas.csv*



---

# TESTE 2 – Transformação e Validação

## 2.1 Validação

Regras aplicadas:

| Campo | Regra |
|------|------|
| CNPJ | Formato e dígito verificador |
| Valor | Numérico e positivo |
| Razão Social | Não vazia |

### 2.1 – Trade-off técnico (tratamento de CNPJs inválidos)

**Decisão:** Manter os registros e marcar a validade do CNPJ.

Em vez de remover esses registros, foi adicionada a coluna `cnpj_valido` para indicar se o CNPJ é válido.

Essa abordagem preserva o volume de dados, permite auditoria e possibilita que análises posteriores filtrem apenas os registros confiáveis, sem perda de informação.

---

## 2.2 Enriquecimento

Foi realizado join com o cadastro oficial da ANS usando `CNPJ`.

Campos adicionados:
- RegistroANS
- Modalidade
- UF

| Caso | Tratamento |
|------|----------|
Sem match | Mantido com dados nulos |
Múltiplos registros | Usado o mais recente |


### 2.2 – Trade-off técnico (join com o cadastro de operadoras)

**Decisão:** Utilizar left join e manter apenas o registro mais recente por CNPJ no CADOP.

O cadastro da ANS possui CNPJs duplicados com informações históricas diferentes. Para resolver isso, foi adotada a estratégia de selecionar o registro com a data de cadastro mais recente (`Data_Registro_ANS`) para cada CNPJ, garantindo dados mais atualizados.

O join foi realizado como `left join` para preservar todas as despesas, mesmo quando não há correspondência no cadastro. Registros sem match são mantidos e marcados como `DESCONHECIDO`, evitando perda de dados e permitindo análises completas.
---

## 2.3 Agregação

Agrupamento por `RazaoSocial` e `UF`.

Métricas:
- Total
- Média trimestral
- Desvio padrão

Arquivo gerado: *despesas_agregadas.csv*

### 2.3 – Trade-off técnico (agregações estatísticas)

**Decisão:** Realizar as agregações em memória usando `groupby` do pandas.

Após a etapa de enriquecimento, o volume de dados já está significativamente reduzido (poucos milhares de linhas), o que torna viável calcular somas, médias e desvios padrão diretamente em memória.

Essa abordagem simplifica a implementação, permite maior flexibilidade analítica e facilita a validação dos resultados, já que todas as métricas são calculadas sobre o mesmo conjunto de dados consolidado.

Em cenários de grande escala, essa etapa poderia ser migrada para processamento distribuído, mas para o escopo atual ela oferece melhor custo-benefício entre simplicidade, desempenho e clareza.

# Conclusão


Este projeto implementa um pipeline realista de dados públicos, tratando:
- inconsistências
- volume elevado

A solução foi construída priorizando simplicidade.
