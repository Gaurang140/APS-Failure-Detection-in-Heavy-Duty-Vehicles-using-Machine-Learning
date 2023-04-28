from sensor.logger import logging
from sensor.exception import SensorException
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
import sys,os
from datetime import datetime
from sensor.entity import config_entity





if __name__=='__main__':
    try:
       craining_pipeline_config = config_entity.TrainingPipelineConfig()
       data_ingestion_comfig = config_entity.DataIngestionConfig(training_pipeline_config=craining_pipeline_config)
       print(data_ingestion_comfig.to_dict())
       data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_comfig)
       data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()

       data_validation_config =  config_entity. DataValidationConfig(training_pipeline_config=craining_pipeline_config)

       data_validation = DataValidation(data_validation_config= data_validation_config , data_ingestion_artifact=data_ingestion_artifacts)
       data_validation_artifact = data_validation.initiate_data_validation()
  
    except Exception as e:
        print(e)


