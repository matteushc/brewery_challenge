# Code Challenge

O pipeline desenvolvido aqui foi usando ferramentas como Docker, Python, Spark e airflow com orquestrador.

The architecture used in this process was Medallion architecture which is based in ELT (Extract, Load, Transform) where data is extracted from API and save in bronze layer as json file, transformed into a suitable format that was parquet (silver laywer) and partitioned by brewery location, make some aggregations and then loaded into a gold layer.

The project was defined based in airflow structure which is:

    1. config - Para armazenar as configurações necessarias do airflow

    2. dags - Onde ficam os códigos das DAGs que norteam o pipeline 

    3. logs - Onde ficam armazenados os logs.

    4. plugins - Onde ficam armazenados os códigos externos, sejam bibliotecas, sejam scripts para processamento, etc.



A primeira etapa pra se executar nesse pipe é a de configuração e instalação. Para isso, na pasta raiz basta digitar o seguinte comando:

```
make build

```

A segunda etapa é preparar o ambiente para ser executado. Basta digitar o seguinte comando também na pasta raiz:

```
make start_environment

```

A terceira etapa é escolher que tipo de pipe vai rodar, pipe completo ou por dia. Existe o por dia que pode ser executado da seguinte maneira:

```
make run_pipeline_date DATA=19980504

```

O completo basta digitar o seguinte comando:

```
make run_pipeline

```

O seguinte comando é para para todos os serviços:

```

make stop_environment

```


O Resutado será uma pasta chamada tables dentro da pasta data e outra chamada result_data.csv que tem o resultado final num arquivo csv.


** Obs: Um ponto importante é que para otmizar a leitura e escrita da tabela ORDERS foi utilizado a estratégia de particionar tanto na leitura quanto na escrita o que reduz bastante o volume de dados necessário pra rodar numa maquina. Nada impede que possa ser carregada por pedaços maiores caso haja um cluster com maior capacidade.
