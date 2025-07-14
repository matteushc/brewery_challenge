# Brewery Challenge


## Tools

* The pipeline developed here was using tools like Docker, Python, Spark and airflow as orchestrator.


## Architecture

* The architecture used in this process was Medallion architecture which is based in ELT (Extract, Load, Transform) where data is extracted from API and save in bronze layer as json file, transformed into a suitable format that was parquet (silver laywer) and partitioned by brewery location, make some aggregations and then loaded into a gold layer.


## Project Structure

* The project was defined based in airflow structure which is:

    1. config - To store the necessary airflow settings

    2. dags - where are the DAG codes that guide the pipeline 

    3. logs - where the logs are stored

    4. plugins - where external codes are stored, whether libraries, processing scripts, etc.

    5. tests - where are the unit tests.


### plugins folder:

* The plugins folder was used in this process to store the pipeline processing scripts. Three files were created: extract_data_api.py, save_silver_layer.py, and save_gold_layer.py. The idea was to structure the process into separate scripts to modularize and facilitate the maintenance of each individual step.

    - extract_data_api.py: Script responsible for extracting data from the API `https://api.openbrewerydb.org/v1/breweries` and saving a json file in the bronze layer.

    - save_silver_layer.py: Script responsible for reading the json file from the bronze layer and transforming it into a parquet file partitioned by the brewery's location, and in this case the chosen one was country and state.

    - save_gold_layer.py: Script responsible for reading the parquet file from the silver layer and aggregating it by the quantity of breweries by type and location and saving it in a file in parquet format in the gold layer.

### dags


* The DAGs folder contains the extract_brewery_data.py file, which is the pipeline's DAG. It contains the DAG's main method, run_pipeline_brewery, which contains all the pipeline steps. Within this method, there are three more: extract_data, save_silver_layer, and save_gold_layer. These methods are used as Airflow task decorators within the DAG to facilitate project development. However, in a production environment, we could add Operators to better control the flow. In the case of PySpark processes, we could add the EmrCreateJobFlowOperator to create the EMR cluster and then the EmrAddStepsOperator to run a Spark job. This would streamline the pipeline if the process needed to scale.


## Monitoring/Alerting:

* To monitor the process, Airflow already has several mechanisms to assist. The most basic is the log itself, which is available for each DAG and the processes within it. Airflow already has an easy-to-view system through the web dashboard, where we can see the DAG and which step failed in that process.
Another point to include in this process would be to create an `on_failure_callback` function within the DAG to send, for example, an email if the process encounters an error. Other mechanisms, such as operators like SlackAPIPostOperator or ExternalTaskSensor, can send a message or alert in case of process errors. For quality alerts or business rules, the same procedure could be followed, creating conditions or checks to validate the steps. The greatExpectations library could also be included to perform job quality steps.


## Execution

* This project was created to run using Amazon's S3 service to save the generated data. Therefore, it is necessary to have two authentication keys to run the process: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. These keys are generated at the following URL for your AWS account: https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials. This link contains a **Create access key** button. After generating the credentials, please download them and grab their codes, including them in the **Makefile** file according to the respective variables.



* The first step to perform in this pipeline is configuration and installation. To do this, in the root folder, simply type the following command:

```
make build

```

* The second step is prepare the environment for execution. Simply enter the following command, also in the root folder (Note: Before performing this step, configure the AWS credential keys mentioned above).:

```
make start_environment

```

* The third step is to install the dependencies to run the tests.

```
make install_dependencies

```

* To start the pipeline and prepare the process, simply run the following command (To access airflow web, username: airflow, password: airflow):

```
make start_pipeline

```

* To run the pipeline, simply run the following command:

```
make run_pipeline

```


* It is possible after the pipeline is activated, to execute it manually through the following command:

``` 
make trigger_dag_manually

```

The following command is to disable all services and clean up the environment:

```

make stop_environment

```

To run the tests, simply run the following command:

```
make run_test

```
