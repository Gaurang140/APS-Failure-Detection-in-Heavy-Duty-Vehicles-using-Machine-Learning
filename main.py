from sensor.logger import logging
from sensor.exception import SensorException
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.data_transformation import DataTransformation
import sys,os
from datetime import datetime
from sensor.entity import config_entity





if __name__=='__main__':
    try:
       
       #data ingestgion
       craining_pipeline_config = config_entity.TrainingPipelineConfig()
       data_ingestion_comfig = config_entity.DataIngestionConfig(training_pipeline_config=craining_pipeline_config)
       print(data_ingestion_comfig.to_dict())
       data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_comfig)
       data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()

       # data validation 
       data_validation_config =  config_entity. DataValidationConfig(training_pipeline_config=craining_pipeline_config)

       data_validation = DataValidation(data_validation_config= data_validation_config , data_ingestion_artifact=data_ingestion_artifacts)
       data_validation_artifact = data_validation.initiate_data_validation()

       #data_transformation

       data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=craining_pipeline_config)
       data_transfromation = DataTransformation(data_transformation_config=data_transformation_config  , data_ingestion_config=data_ingestion_comfig)
       data_transformation_artifacts = data_transfromation.data_transformation_initiate()


       #model_trainer 

       model_trainer_config= config_entity.ModelTrainerConfig(training_pipeline_config=craining_pipeline_config)
       model_trainer = ModelTrainer(model_trainer_config=model_trainer_config  , data_transformation_artifact=data_transformation_artifacts)
       model_trainer_artifacts = model_trainer.initiate_model_trainer()
  
    except Exception as e:
        raise SensorException(e ,sys)


