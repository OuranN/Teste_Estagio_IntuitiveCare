# Teste_Estagio_IntuitiveCare

### 1.2 – Trade-off técnico (memória vs processamento incremental)

**Decisão:** Processamento em memória.

Os três últimos trimestres somaram cerca de 380 mil registros após a extração dos CSVs. Esse volume é perfeitamente manejável em memória, o que permitiu usar DataFrames completos para filtrar, normalizar e consolidar os dados de forma simples e eficiente.

Essa abordagem reduz a complexidade do código, facilita a validação dos dados e torna o processo de consolidação mais direto, já que todos os trimestres podem ser cruzados e agregados no mesmo contexto.

Caso o volume de dados cresça significativamente no futuro, a solução pode ser facilmente adaptada para leitura incremental, sem necessidade de alterar a lógica principal do pipeline.

### 2.1 – Trade-off técnico (tratamento de CNPJs inválidos)

**Decisão:** Manter os registros e marcar a validade do CNPJ.

Em vez de remover esses registros, foi adicionada a coluna `cnpj_valido` para indicar se o CNPJ é válido.

Essa abordagem preserva o volume de dados, permite auditoria e possibilita que análises posteriores filtrem apenas os registros confiáveis, sem perda de informação.

### 2.2 – Trade-off técnico (join com o cadastro de operadoras)

**Decisão:** Utilizar left join e manter apenas o registro mais recente por CNPJ no CADOP.

O cadastro da ANS possui CNPJs duplicados com informações históricas diferentes. Para resolver isso, foi adotada a estratégia de selecionar o registro com a data de cadastro mais recente (`Data_Registro_ANS`) para cada CNPJ, garantindo dados mais atualizados.

O join foi realizado como `left join` para preservar todas as despesas, mesmo quando não há correspondência no cadastro. Registros sem match são mantidos e marcados como `DESCONHECIDO`, evitando perda de dados e permitindo análises completas.

### 2.3 – Trade-off técnico (agregações estatísticas)

**Decisão:** Realizar as agregações em memória usando `groupby` do pandas.

Após a etapa de enriquecimento, o volume de dados já está significativamente reduzido (poucos milhares de linhas), o que torna viável calcular somas, médias e desvios padrão diretamente em memória.

Essa abordagem simplifica a implementação, permite maior flexibilidade analítica e facilita a validação dos resultados, já que todas as métricas são calculadas sobre o mesmo conjunto de dados consolidado.

Em cenários de grande escala, essa etapa poderia ser migrada para processamento distribuído, mas para o escopo atual ela oferece melhor custo-benefício entre simplicidade, desempenho e clareza.