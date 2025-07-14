import pytest

import os
#sys.path.insert(0, "")

from pyspark.sql import Row
from plugins.save_silver_layer import SaveSilverLayer

# this allows using the fixture in all tests in this module
#pytestmark = pytest.mark.usefixtures("spark_session")

@pytest.fixture(scope="session")
def project_root(pytestconfig):
    """
    Fixture to provide the pytest root directory.
    """
    return pytestconfig.rootpath


@pytest.mark.usefixtures("spark_session")
def test_save_layer(spark_session, project_root):
    """ test that a single event is parsed correctly
    Args:
        spark_context: test fixture SparkContext
        hive_context: test fixture HiveContext
    """

    silber_layer = SaveSilverLayer(spark_session)
    silber_layer.process(prefix="tests/data/")
    
    assert os.path.isdir(f"{project_root}/tests/data/airflow-brewery-list/silver/brewery.parquet")
