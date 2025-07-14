# import pytest

# import sys
# sys.path.insert(0, "")

# from pyspark.sql import Row
# from scripts.save_silver_layer import SaveSilverLayer

# # this allows using the fixture in all tests in this module
# pytestmark = pytest.mark.usefixtures("spark_session")

# #@pytest.mark.usefixtures("spark_session")
# def test_save_layer(spark_session):
#     """ test that a single event is parsed correctly
#     Args:
#         spark_context: test fixture SparkContext
#         hive_context: test fixture HiveContext
#     """

#     test_input = [
#         ' hello spark ',
#         ' hello again spark spark'
#     ]

#     input_rdd = spark_session.sparkContext.parallelize(test_input, 1)
    
#     expected_results = {'hello':2, 'spark':3, 'again':1}  
#     assert expected_results


# #@pytest.mark.usefixtures("spark_session")
# def test_extract_data(spark_session):
#     """ test that a single event is parsed correctly
#     Args:
#         spark_context: test fixture SparkContext
#         hive_context: test fixture HiveContext
#     """

#     local_records = [
#         Row(id=1, first_name='Dan Germain', steps_to_desk=21, uuid='a6ea18bb48e4385603d2fd060a884e2c6572d130'),
#         Row(id=2, first_name='Dan Sommerville', steps_to_desk=21, uuid='74d47f295b0bd5cb51c508f8cae9575c7a9004b7'),
#         Row(id=3, first_name='Alex Ioannides', steps_to_desk=42, uuid='4b1701b5937b99188345a7904bee4365e5197051'),
#         Row(id=4, first_name='Ken Lai', steps_to_desk=42, uuid='24cd3dd773d2927be5abfbb1bcc76442a2654d57'),
#         Row(id=5, first_name='Stu White', steps_to_desk=63, uuid='e1c3d6a40c76266f838ac51bb8bcb3570f52ea77'),
#         Row(id=6, first_name='Mark Sweeting', steps_to_desk=63, uuid='4dd0331b08811c48ecbbc623f0bbe22b4e253a21'),
#         Row(id=7, first_name='Phil Bird', steps_to_desk=84, uuid='a171a7c167a5b4b65255bb51fbd22d6354169f7f'),
#         Row(id=8, first_name='Kim Suter', steps_to_desk=84, uuid='79ef50b1c91024162480d414646424076de162e9')
#     ]

#     df_test = spark_session.createDataFrame(local_records)
#     expected_results = df_test.collect()

#     df = None
#     result = df.collect()

#     assert expected_results == result
