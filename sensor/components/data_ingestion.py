
from sensor.utils import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.config import TARGET_COLUMN
import os,sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


class DataIngestion:


    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig) -> None:
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e :
            raise(e, sys)


    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exploring collection data as pandas dataframes")
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name)

          

            #replcae na with Nan
            
            df.replace(to_replace='na' , value=np.NAN , inplace=True)



            # save data in featue store 

            logging.info('Save data in feature store')

            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir ,exist_ok=True)
            logging.info('save df to feature store')
            #save data frame in feature store folder 
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path , index=False, header=True)
            
            logging.info('Split data set into train test set')
            #Split the dataset

            train_df,test_df = train_test_split(df , test_size=self.data_ingestion_config.test_size , random_state=42 , stratify=df[TARGET_COLUMN])


            logging.info('create_dataset directory if not available')

            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)

            #create a folder if its not available
            os.makedirs(dataset_dir , exist_ok=True)

            logging.info("Save Dataframe to feature store folder")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            

            #Preparing artifacts

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(

                feature_store_file_path = self.data_ingestion_config.feature_store_file_path , 
                train_file_path= self.data_ingestion_config.train_file_path , 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data_ingestion artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(error_message=e , error_detail=sys)
