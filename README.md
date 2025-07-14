# Brewery Challenge


## Tools

* O pipeline desenvolvido aqui foi usando ferramentas como Docker, Python, Spark e airflow com orquestrador.


## Architecture

* The architecture used in this process was Medallion architecture which is based in ELT (Extract, Load, Transform) where data is extracted from API and save in bronze layer as json file, transformed into a suitable format that was parquet (silver laywer) and partitioned by brewery location, make some aggregations and then loaded into a gold layer.


## Project Structure

* The project was defined based in airflow structure which is:

    1. config - Para armazenar as configurações necessarias do airflow

    2. dags - Onde ficam os códigos das DAGs que norteam o pipeline 

    3. logs - Onde ficam armazenados os logs.

    4. plugins - Onde ficam armazenados os códigos externos, sejam bibliotecas, sejam scripts para processamento, etc.

    5. tests - Onde ficam os tests unitários.


### plugins folder:

* A pasta plugins foi usada nesse processo para armazenar os script para processamento do pipeline. Foram construidos 3 arquivos: extract_data_api.py, save_silver_layer.py e save_gold_layer.py. A ideia foi estruturar o processo segregado em scripts diferentes para modularizar e facilitar a manutenção de cada etapa do processo indivualemente.

    - extract_data_api.py: Script responsável por extrair os dados da API `https://api.openbrewerydb.org/v1/breweries` e salvar um arquivo json na camada bronze.

    - save_silver_layer.py: Script responsável por ler o arquivo json da camada bronze e transforma-lo em arquivo parquet particionado pela localização da brewery, e que nesse caso o escolhido foi country e state.

    - save_gold_layer.py: Script responsável por ler o arquivo parquet da camada silver e agrega-lo pela quantidade de brewery pelo type and location e salvar num arquivo no formato parquet na camada gold.

### dags


* Na pasta DAGs contém o arquivo extract_brewery_data.py que é a DAG do pipeline. Nele está o metodo principal da DAG chamado run_pipeline_brewery, onde vai conter todas as etapas do pipeline. Dentro desse metodo existem mais 3, extract_data, save_silver_layer e save_gold_layer. Esses metodos estão como task decorator do airflow dentro da DAG para facilitar o desenvolvimento do projeto, porém num ambiente de produção poderiamos colocar os Operators para controlar melhor o fluxo. No caso dos processos pyspark poderiamos colocar o EmrCreateJobFlowOperator para criar o cluster EMR e depois o operator EmrAddStepsOperator para rodar um job spark. Isso facilitaria o pipeline caso precisasse escalar o processo.


## Monitoring/Alerting:

* Para monitorar o processo, o airflow ja possue varios mecanismos para auxiliar. O mais básico é o proprio log que em cada DAG e nos processos dentro dela, o airflow ja possue um sistema facil de visualizar através da painel web , onde conseguimos visualizar a DAG e qual step deu erro naquele processo.
Outro ponto para incluir nesse processo seria criar uma função `on_failure_callback` dentro da DAG para enviar, por exemplo, um email caso o processo desse erro. Existem outros mecanismos como alguns operators como SlackAPIPostOperator ou ExternalTaskSensor para enviar uma mensagem ou alertar em caso de erro no processo. No caso de alertas de qualidade ou de alguma regra de negocio o mesmo procedimento poderia ser feito, criando uma condições ou checks para validar os steps. Também poderia incluir a biblioteca greatExpectations para fazer as etapas de qualidades dos jobs.


## Execution

* Esse projeto foi criado para rodar usando o serviço do s3 da Amazon para salvar os dados gerados. Portanto é necessário ter duas chaves de autenticação para poder rodar o processo, que são elas: `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`. Essas chaves são geradas na seguinte url da sua conta na aws: https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials. Nesse link existe um botão **Create access key**. Após gerar as credenciais, favor baixa-las e pegar os codigos delas e incluir no arquivo **Makefile** de acordo com as respectivas variáveis.



* A primeira etapa pra se executar nesse pipe é a de configuração e instalação. Para isso, na pasta raiz basta digitar o seguinte comando:

```
make build

```

* A segunda etapa é preparar o ambiente para ser executado. Basta digitar o seguinte comando também na pasta raiz:

```
make start_environment

```

* A terceira etapa é instalar as dependencias para rodar os testes.

```
make install_dependencies

```

* Para iniciar o pipeline e preparar o processo basta executar o seguinte comando:

```
make start_pipeline

```

* Para rodar o pipeline basta executar o seguinte comando:

```
make run_pipeline

```

O seguinte comando é para desligar todos os serviços e limpar o ambiente:

```

make stop_environment

```

Para rodar os testes, basta executar o seguinte comando:

```
make run_test

```
