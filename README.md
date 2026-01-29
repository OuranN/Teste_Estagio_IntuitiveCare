# Teste_Estagio_IntuitiveCare

### 1.2 – Trade-off técnico (memória vs processamento incremental)

**Decisão:** Processamento em memória.

Os três últimos trimestres somaram cerca de 380 mil registros após a extração dos CSVs. Esse volume é perfeitamente manejável em memória, o que permitiu usar DataFrames completos para filtrar, normalizar e consolidar os dados de forma simples e eficiente.

Essa abordagem reduz a complexidade do código, facilita a validação dos dados e torna o processo de consolidação mais direto, já que todos os trimestres podem ser cruzados e agregados no mesmo contexto.

Caso o volume de dados cresça significativamente no futuro, a solução pode ser facilmente adaptada para leitura incremental, sem necessidade de alterar a lógica principal do pipeline.

