.EXPORT_ALL_VARIABLES:

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

build:
	docker build -t apache/airflow:3.0.1 .

start_environment:
	mkdir ./dags ./logs ./plugins
	echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

	docker compose run airflow-cli airflow config list

	docker compose up airflow-init

	virtualenv -p python3 .venv
	source .venv/bin/activate
	pip install -r requirements.txt

start_pipeline:
	docker compose up -d
	
run_pipeline:

	docker exec -it airflow-scheduler airflow dags trigger extract_brewery_data

stop_environment:
	docker compose down --volumes --rmi all