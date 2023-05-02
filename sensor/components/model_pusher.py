from sensor.predictor import ModelResolver
from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import DataTransformationArtifact , ModelTrainerArtifacts , ModelPusherArtifacts
from sensor.exception import SensorException 
from sensor.logger import logging 
from sensor.utils.utils import load_object , save_object 
import os , sys 


class ModelPusher:
    
    def __init__(self, mode_pusher_config : ModelPusherConfig , 
                 data_transformation_artifacts : DataTransformationArtifact, 
                 model_trainer_artifact : ModelTrainerArtifacts):
        try:
            self.mode_pusher_config = mode_pusher_config
            self.data_transformation_artifacts = data_transformation_artifacts
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.mode_pusher_config.outside_saved_model_dir)
        except Exception as e: 
            raise SensorException(e, sys)
        
    def initiate_model_pusher(self, )->ModelPusherArtifacts:
        try:
            #load objects 
            logging.info("Loading transformer model and targer encoder")
            transformer = load_object(file_path= self.data_transformation_artifacts.transformation_object_path)
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path=self.data_transformation_artifacts.target_encoder_path)



            # model pusher dir

            logging.info("saving  models in pusher directory")
            tra_path = self.mode_pusher_config.pusher_transformer_path
            m_path = self.mode_pusher_config.pusher_model_path 
            encd_path = self.mode_pusher_config.pusher_target_encoder_path
            
            save_object(file_path=tra_path , obj= transformer)
            save_object(file_path=m_path, obj= model)
            save_object(file_path= encd_path, obj= target_encoder)
                

            #saved model dir 
            logging.info("saving the model in saved model dir")
            transformer_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()

            save_object(file_path= transformer_path, obj= transformer)
            save_object(file_path= model_path, obj= model)
            save_object(file_path= target_encoder_path, obj= target_encoder)




            model_pusher_config = ModelPusher(mode_pusher_config=self.mode_pusher_config , 
                                              data_transformation_artifacts=self.data_transformation_artifacts, 
                                              model_trainer_artifact=self.model_trainer_artifact)






        except Exception as e: 
            raise SensorException(e, sys)

