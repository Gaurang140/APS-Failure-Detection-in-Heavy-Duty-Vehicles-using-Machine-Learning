from sensor.pipeline.training_pipeline import start_training_pipline
from sensor.pipeline.batch_prediction import start_batch_prediction
from sensor.exception import SensorException
import sys

input_dir = "aps_failure_training_set1.csv"
print(__name__)

if __name__ == "__main__":
    try:
        start_training_pipline()
        output = start_batch_prediction(input_file_path=input_dir)
        print(output)
    except Exception as e:
        raise SensorException(e , sys)