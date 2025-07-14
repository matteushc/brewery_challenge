.EXPORT_ALL_VARIABLES:

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

build:
	docker build -t apache/airflow:3.0.1 .

start_environment:
	mkdir -p ./dags ./logs ./plugins ./config

	chmod -R 777 ./dags ./logs ./plugins ./config

	@echo "AIRFLOW_UID=$$(id -u)\nAIRFLOW_GID=0" > .env

	@echo "AWS_ACCESS_KEY_ID=$$(AWS_ACCESS_KEY_ID)" >> .env
	@echo "AWS_SECRET_ACCESS_KEY=$$(AWS_SECRET_ACCESS_KEY)" >> .env

	docker compose run airflow-cli airflow config list

	docker compose up airflow-init

	virtualenv -p python3 .venv

install_dependencies:
	. .venv/bin/activate

	pip install -r requirements.txt

start_pipeline:
	docker compose --env-file .env up -d
	
run_pipeline:
	docker exec -it brewery_challenge-airflow-scheduler-1 airflow dags unpause run_pipeline_brewery
	docker exec -it brewery_challenge-airflow-scheduler-1 airflow dags trigger run_pipeline_brewery

stop_environment:
	docker compose down --volumes --rmi all

run_test:
	. .venv/bin/activate
	pytest tests/save_layer_test.py
	python3 tests/extract_data_api_test.py TestExtractDataAPI.test_fetch_data
	python3 tests/extract_data_api_test.py TestExtractDataAPI.test_save_data_to_file
