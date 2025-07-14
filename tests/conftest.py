# """ pytest fixtures that can be resued across tests. the filename needs to be conftest.py
# """

# import logging
# import pytest

# from pyspark import SparkConf
# from pyspark.sql import SparkSession


# def quiet_py4j():
#     """ turn down spark logging for the test context """
#     logger = logging.getLogger('py4j')
#     logger.setLevel(logging.WARN)


# @pytest.fixture(scope="session")
# def spark_session(request):
#     """ fixture for creating a spark context
#     Args:
#         request: pytest.FixtureRequest object
#     """
#     conf = (SparkConf().setMaster("local[2]").setAppName("pytest-pyspark-local-testing"))
#     spark = SparkSession.builder.config(conf=conf) \
#             .enableHiveSupport().getOrCreate()

#     quiet_py4j()
#     return spark
