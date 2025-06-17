# docker_gb

## Este repositório contém um conjunto de scripts para comparar o desempenho do PostgreSQL rodando em ambiente Docker versus ambiente nativo (local). Os testes realizados incluem:

- Tempo de inicialização do banco de dados
- Consumo de memória
- Uso de CPU
- I/O de disco
- Latência de consultas
- Densidade (quantidade de instâncias simultâneas suportadas)

Os resultados dos testes são salvos em arquivos CSV na pasta results e podem ser visualizados por meio de gráficos gerados automaticamente. O repositório inclui scripts para execução dos testes, coleta de métricas e geração de gráficos comparativos, além de um exemplo de configuração Docker Compose para o PostgreSQL.

Ideal para quem deseja analisar o impacto do uso de containers Docker no desempenho de bancos de dados em comparação ao ambiente nativo.