from sensor.entity import artifact_entity , config_entity
from sensor.utils.utils import*
from sensor.exception import SensorException
from sensor.logger import logging
import numpy as np 
from typing import Optional
import pandas as pd 
import os,sys
from sklearn.pipeline import Pipeline
import pandas as pd
from sensor import utils
import numpy as np
from sklearn.preprocessing import LabelEncoder
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sensor.config import TARGET_COLUMN



class DataTransformation():
    def __init__(self , 
                data_transformation_config:config_entity.DataTransformationConfig ,
                data_ingestion_config : artifact_entity.DataIngestionArtifact) -> None:
        try: 
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_tramsformation_config = data_transformation_config
            self.data_ingestion_artifacts = data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)

    @classmethod
    def get_data_transformation_objects(cls)->Pipeline:
        try: 

            simple_imputer = SimpleImputer(strategy="constant" ,fill_value=0 )
            robust_scaler = RobustScaler()

            pipeline_transformation = Pipeline(steps=[
                ('Imputer' , simple_imputer ),
                ('Robust_sclaer'  ,robust_scaler) 

            ])
            return pipeline_transformation
        except Exception as e:
            raise SensorException(e,sys)
    
    def data_transformation_initiate (self)->artifact_entity.DataTransformationArtifact:
        try: 

            logging.info("Reading Train data frame")
            train_df = pd.read_csv(self.data_ingestion_artifacts.train_file_path)
            logging.info("Reading Test data frame")
            test_df = pd.read_csv(self.data_ingestion_artifacts.test_file_path)

            logging.info('Removing target columns')
            input_feature_train_df = train_df.drop(TARGET_COLUMN , axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN , axis=1)

         
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df  = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            # label encoder transformation 

            target_feature_train_df_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_df_arr = label_encoder.transform(target_feature_test_df)

            transformation_pipeline = DataTransformation.get_data_transformation_objects()
            input_feature_train_arr = transformation_pipeline.fit(input_feature_train_df)

            # transforming input features
            input_feature_train_arr =transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr =transformation_pipeline.transform(input_feature_test_df)


            #sampling 

            smt = SMOTETomek(sampling_strategy="minority" , random_state=42)
            logging.info(f"Before resampling in training set input :  {input_feature_train_arr.shape} Target : {target_feature_train_df_arr.shape}")
            input_feature_train_arr , target_feature_train_df_arr=smt.fit_resample(input_feature_train_arr , target_feature_train_df_arr)
            logging.info(f"After resampling in training set input :  {input_feature_train_arr.shape} Target : {target_feature_train_df_arr.shape}")
            
            logging.info(f"Before resampling in test set input :  {input_feature_test_arr.shape} Target : {target_feature_test_df_arr.shape}")
            input_feature_test_arr , target_feature_test_df_arr=  smt.fit_resample(input_feature_test_arr , target_feature_test_df_arr)
            logging.info(f"After resampling in test set input :  {input_feature_test_arr.shape} Target : {target_feature_test_df_arr.shape}")

            #target encoder
            #target encoder
            train_arr = np.c_[input_feature_train_arr, target_feature_train_df_arr ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_df_arr]


            
            #save numpy array
            save_numpy_array_data(file_path=self.data_tramsformation_config.transformed_train_path,
                                        array=train_arr)

            save_numpy_array_data(file_path=self.data_tramsformation_config.transformed_test_path,
                                        array=test_arr)


            save_object(file_path=self.data_tramsformation_config.transformation_object_path,
             obj=transformation_pipeline)

            save_object(file_path=self.data_tramsformation_config.target_encoder_path,obj=label_encoder)



            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transformation_object_path=self.data_tramsformation_config.transformation_object_path,
                transformation_train_path = self.data_tramsformation_config.transformed_train_path,
                transformation_test_path = self.data_tramsformation_config.transformed_test_path,
                target_encoder_path = self.data_tramsformation_config.target_encoder_path

            )

            logging.info(f"Data transformation artifact {data_transformation_artifact}")

            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e,sys)
       
