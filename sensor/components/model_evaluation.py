from sensor.predictor import ModelResolver
from sensor.exception import SensorException
from sensor.entity import config_entity , artifact_entity
from sensor.logger import logging
import os , sys 



class ModelEvaluation:
    def __init__(self , 
                 model_evaluation_config : config_entity.ModelEvaluationConfig, 
                 data_ingestion_artifacts : artifact_entity.DataIngestionArtifact, 
                 data_transformation_artifact : artifact_entity.DataTransformationArtifact, 
                 model_trainer_artifact : artifact_entity.ModelTrainerArtifacts) -> None:
        try:
            logging.info(f"{'>>'*20} Model Evaluation {'<<'*20}")
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact  =model_trainer_artifact
            self.model_resolver = ModelResolver()

        except Exception as e :
            raise SensorException(e,sys)
    

    def initiate_model_evaluation(self) -> artifact_entity.ModelEvaluationArtifacts  : 
        try:
            # if saved model folder has model then we will compare 
            # which model is best for trained or model from saved model folder
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifacts(is_model_accepted=True , 
                                                                               improved_accuracy=None)
                logging.info(f"Model Evaluation artifact :  {model_eval_artifact}")
                return model_eval_artifact


        except Exception as e :
            raise SensorException(e,sys)

