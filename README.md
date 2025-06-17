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

## Como rodar:

Utilize o ambiente virtual do python e rode o arquivo run_all_tests.py como administrador do sistema na root do repositorio.
Programas necessários para rodar:
- postgres 17
- Docker

Tome cuidado com qual porta, nome de usuario, senha e tipo de host que está utilizando. Tens de colocar na mão ali no código (muito provavel só é necessário mudar a senha). O código vai ter funcionado se os arquivos .csv tiverem atualizado. Após isso podes gerar as imagens indo na pasta scripts e rodando o generate_graph.py.
