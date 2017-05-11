# This class should execute the kmeans model on the recived data.
import pyspark.ml.clustering as models
import pyspark.ml.feature as features
from pydoc import locate
from pyspark.ml import Pipeline
from shared.ConvertAllToVecToMl import ConvertAllToVecToMl


### SPARK_HOME = "/usr/local/share/spark/python/"

class ExecuteWorkflow(object):
    '''
    
    '''

    # print(models.__all__)

    def __init__(self):
        # , data=None, model="kmeans", params={}
        self._params = None  # dict of parameters including model, mode and so on
        # self._data = None #Perhaps it is needed

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, dic):
        assert isinstance(dic, dict)
        self._params = dic

    def construct_pipeline(self):

        vectorized_features = features.VectorAssembler(inputCols = self._params["features"], outputCol = "features")  # vectorization

        caster = ConvertAllToVecToMl(inputCol=vectorized_features.getOutputCol(),
                                     outputCol="casted_features")  # does the double and ml.densevector cast

        if self._params["standardize"]:
            scaling_model = features.StandardScaler(
                inputCol = caster.getOutputCol(),
                outputCol = "scaled_features",
                withMean = True,
                withStd = True
            )
        else:
            scaling_model = features.StandardScaler(
                inputCol = vectorized_features.getOutputCol(),
                outputCol = "scaled_features",
                withMean = False,
                withStd = False
            )


        cluster_model = getattr(models, self._params["model"])  # Clustering method
        if self._params["model"] == "KMeans":
            cluster_object = cluster_model(
                featuresCol = scaling_model.getOutputCol(),
                predictionCol ="prediction",#  self._params["prediction"],
                k = self._params["iterations"],
                initMode = self._params["initialmode"],
                initSteps = self._params["initialstep"],
                tol = 1e-4,
                maxIter = self._params["iterations"],
                seed = None
            )
        else:
            raise NotImplementedError(str(self._params["model"])+" is not implemented")

        stages = [vectorized_features, caster, scaling_model]#, cluster_object]

        return Pipeline(stages = stages)

    def run(self, data):
        '''
        A pyspark.ml.clustering model
        :param self: 
        :param data: A pyspark data frame with the relevant data
        :return: A fitted model in the pipeline
        '''

        pipeline = self.construct_pipeline()
        return pipeline.fit(data)



