from sensor.predictor import ModelResolver
from sensor.exception import SensorException
from sensor.entity import config_entity , artifact_entity
from sensor.logger import logging
from sensor.utils.utils import load_object
from sklearn.metrics import f1_score
from sensor.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
import sklearn
import pandas as pd
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


            logging.info("saved model folder has model then we will compare "
                         "which model is best for trained or model from saved model folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifacts(is_model_accepted=True , 
                                                                               improved_accuracy=None)
                

            
                
                logging.info(f"Model Evaluation artifact :  {model_eval_artifact}")
                return model_eval_artifact

            #findidng the location of transformer model and target encoder
            logging.info("findidng the location of transformer model and target encoder")

            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            #previously trained loading the objects
            logging.info("previously trained loading the objects")

            transformer =load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=target_encoder_path) 


            #currently trained model object 
            logging.info("currently trained object")
            current_trasformers = load_object(file_path=self.data_transformation_artifact.transformation_object_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)


            test_df = pd.read_csv(self.data_ingestion_artifacts.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_encoder.transform(target_df)

            # accuracy using previously trained model #
            logging.info('accuracy using previously trained model')
            input_feature_name = list(transformer.feature_names_in_)
            input_arr =transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            target_encoder.inverse_transform(y_pred[:5])
            

            logging.info(f"Prediction using previous model : {target_encoder.inverse_transform(y_pred[:5])}")

            previous_model_score = f1_score(y_true=y_true , y_pred=y_pred)

            logging.info(f"f1 score of previous model : {previous_model_score}")




            # current trained model f1 score and accuracy 
            logging.info('accuracy using current trained model')
            input_feature_name_cr = list(current_trasformers.feature_names_in_)
            input_arr_current = current_trasformers.transform(test_df[input_feature_name_cr])
            y_pred_current = current_model.predict(input_arr_current)
            current_target_encoder.inverse_transform(y_pred[:5])
            logging.info(f"Prediction using current_model : {current_target_encoder.inverse_transform(y_pred_current[:5])}")

            current_model_score = f1_score(y_true=y_true , y_pred= y_pred_current)


            logging.info(f"f1 score of current model : {current_model_score}")

            if current_model_score < previous_model_score:
                raise Exception("current trained model is not better than previous model")
            
            
            model_eval_artifact = artifact_entity.ModelEvaluationArtifacts(is_model_accepted=True , 
                                                    improved_accuracy=current_model_score-previous_model_score)
            


            logging.info(f"Model evaluation artifact : {model_eval_artifact}")


            return model_eval_artifact
            



            




            # will compare this model on test dataset 



        except Exception as e :
            raise SensorException(e,sys)

