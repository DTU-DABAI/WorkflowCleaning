from unittest import TestCase
from sample.ExecuteWorkflow import ExecuteWorkflow
from unittest.mock import MagicMock
import findspark
import logging

findspark.init()
from pyspark.ml.pipeline import Pipeline
from pyspark.context import SparkContext
from pyspark import Row
import numpy as np

TEST_DICT = {'features': ('AarsVaerk_1', 'AarsVaerk_2', 'AarsVaerk_3', 'AarsVaerk_4', 'AarsVaerk_5', 'AarsVaerk_6', 'AarsVaerk_7', 'AarsVaerk_8', 'AarsVaerk_9', 'AarsVaerk_10', 'AarsVaerk_11', 'AarsVaerk_12', 'AarsVaerk_13', 'AarsVaerk_14', 'AarsVaerk_15', 'medArb_1', 'medArb_2', 'medArb_3', 'medArb_4', 'medArb_5', 'medArb_6', 'medArb_7', 'medArb_8', 'medArb_9', 'medArb_10', 'medArb_11', 'medArb_12', 'medArb_13', 'medArb_14', 'medArb_15', 'avgVarighed', 'totalAabneEnheder', 'totalLukketEnheder', 'rank_1', 'rank_2', 'rank_3', 'rank_4', 'rank_5', 'rank_6', 'rank_7', 'reklamebeskyttet'),
             'initialstep': 43,
             'standardize': True,
             'clusters': 24,
             'model': 'KMeans',
             'initialmode': 'random',
             'prediction': 'predict',
             'iterations': 27
             }


class TestExecuteWorkflow(TestCase):

    def setUp(self):
        self.workflow = ExecuteWorkflow()
        self.sc = SparkContext.getOrCreate()

    def tearDown(self):
        self.sc.stop()

    def test_params(self):
        parameters = {"model": "KMeans", "type": "random", "standardize": True}
        self.workflow.params = parameters
        self.assertDictEqual(self.workflow.params, parameters)

    def test_construct_pipeline(self):
        pipeline_mock = MagicMock()
        df_test = [Row(cvrNummer=12966407,)]

    def test_gen_cluster_center(self):

        dummy_cluster = [np.array([0,1]), np.array([100,1])]
        self.output_dict = self.workflow.gen_cluster_center(2,dummy_cluster)
        self.mock_dict = {0:np.array([0,1]),1:np.array([100,1])}

        self.assertListEqual(list(self.mock_dict[0]),list(self.output_dict[0]))

        self.assertIsInstance(self.output_dict,dict)


    #def test_run(self):
    #    self.fail()
