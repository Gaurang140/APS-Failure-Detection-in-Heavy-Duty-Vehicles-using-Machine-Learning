from sensor.logger import logging
from sensor.exception import SensorException
from sensor.components.data_ingestion import DataIngestion
import sys,os
from datetime import datetime
from sensor.entity import config_entity





if __name__=='__main__':
    try:
       craining_pipeline_config = config_entity.TrainingPipelineConfig()
       data_ingestion_comfig = config_entity.DataIngestionConfig(training_pipeline_config=craining_pipeline_config)
       print(data_ingestion_comfig.to_dict())
       data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_comfig)
       print(data_ingestion.initiate_data_ingestion())
  
    except Exception as e:
        print(e)


