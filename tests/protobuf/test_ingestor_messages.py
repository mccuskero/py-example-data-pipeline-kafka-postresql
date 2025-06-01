import sys
import os
from loguru import logger
from pytest import approx

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from iris_features_pb.iris_features_pb2 import IrisFeatures, IrisFeaturesList
#from settings import *


# from iris_features_pb.iris_features_pb2 import IrisFeatures, IrisFeaturesList


def test_iris_features():
    iris_features = IrisFeatures(sepal_length=float(5.1), sepal_width=float(3.5), petal_length=float(1.4), petal_width=float(0.2))
    logger.info(f"sepal_length: {iris_features.sepal_length}")
    logger.info(f"sepal_width: {iris_features.sepal_width}")
    logger.info(f"petal_length: {iris_features.petal_length}")
    logger.info(f"petal_width: {iris_features.petal_width}")
    assert iris_features.sepal_length == approx(5.1)
    assert iris_features.sepal_width == approx(3.5)
    assert iris_features.petal_length == approx(1.4)
    assert iris_features.petal_width == approx(0.2)
    logger.info("test_iris_features")
    

def test_iris_features_list():
    iris_features_list = IrisFeaturesList( iris_features_list=[IrisFeatures(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), IrisFeatures(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)])
    assert iris_features_list. iris_features_list[0].sepal_length == approx(5.1)
    assert iris_features_list. iris_features_list[0].sepal_width == approx(3.5)
    assert iris_features_list. iris_features_list[0].petal_length == approx(1.4)
    assert iris_features_list. iris_features_list[0].petal_width == approx(0.2)
    logger.info("test_iris_features_list")

if __name__ == "__main__":
    test_iris_features()
    test_iris_features_list()