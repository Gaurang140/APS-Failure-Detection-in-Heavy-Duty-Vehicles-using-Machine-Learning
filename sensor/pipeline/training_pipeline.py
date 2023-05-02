from sensor.logger import logging
from sensor.exception import SensorException
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher
import sys,os
from datetime import datetime
from sensor.entity import config_entity





def start_training_pipline():
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

       # model evaluation 
       model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=craining_pipeline_config)
       model_evaluator = ModelEvaluation(model_evaluation_config=model_eval_config , 
                                          data_ingestion_artifacts=data_ingestion_artifacts,
                                          data_transformation_artifact=data_transformation_artifacts , 
                                          model_trainer_artifact=model_trainer_artifacts)
       model_eval_artifact = model_evaluator.initiate_model_evaluation()

        #model pusher
       model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=craining_pipeline_config)
       model_pusher = ModelPusher(mode_pusher_config=model_pusher_config ,
                                  data_transformation_artifacts=data_transformation_artifacts,
                                  model_trainer_artifact=model_trainer_artifacts)
       model_pusher_artifact = model_pusher.initiate_model_pusher()
  
    except Exception as e:
        raise SensorException(e ,sys)


