from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
import os,sys 
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sensor.utils.utils import load_numpy_array_data , load_object , save_object
from sklearn.metrics import f1_score


class ModelTrainer:


    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact
                ):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)

   

    def fine_tune(self ,X ,y):
        try:
            logging.info("Fine-tuning XGBoost classifier")
            
            # Define hyperparameters to be tuned
            param_grid = {
                'learning_rate': [0.05, 0.1, 0.15],
                'max_depth': [3, 5, 7],
                'n_estimators': [50, 100, 150]
            }
            
            # Create Grid Search CV object
            xgb_clf = XGBClassifier()
            grid_search = GridSearchCV(xgb_clf, param_grid, cv=3, scoring='f1_macro')
            
            # Load training data
          
            
            # Fit Grid Search CV object on training data
            logging.info("Fitting Grid Search CV object")
            grid_search.fit(X, y)
            
            # Retrieve best estimator from Grid Search CV object
            best_estimator = grid_search.best_estimator_
            logging.info(f"Best estimator: {best_estimator}")


            # Print best parameters and corresponding score
            print('Best parameters:', grid_search.best_params_)
            print('Best score:', grid_search.best_score_)

            return grid_search.best_params_


            


            
        except Exception as e:
            raise SensorException(e, sys)



    def train_model(self ,X,y):
        try:
            #best_parameters = self.fine_tune(X=X,y=y)
            #MAX_DEPTH   = best_parameters[['max_depth']]
            #LEARNING_RATE = best_parameters['learning_rate']
            #ESTIMATORS = best_parameters['n_estimators']

            Xgb_clf = XGBClassifier()
         
            Xgb_clf.fit(X,y)

            return Xgb_clf
        
            

        except Exception as e:
            raise SensorException(e, sys)
        

    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifacts:
        try : 
            logging.info(f"Loading train and test array.")
            train_arr = load_numpy_array_data(file_path= self.data_transformation_artifact.transformation_train_path)
            test_arr = load_numpy_array_data(file_path= self.data_transformation_artifact.transformation_test_path)

            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            
            logging.info("train model")
            model = self.train_model(X = x_train , y =y_train)

            logging.info(f"Calculating f1 train score")
            yhat_train = model.predict(x_train)
            f1_train_score  =f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"Calculating f1 test score")
            yhat_test = model.predict(x_test)
            f1_test_score  =f1_score(y_true=y_test, y_pred=yhat_test)
            
            logging.info(f"train score:{f1_train_score} and tests score {f1_test_score}")
            #check for overfitting or underfiiting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {f1_test_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff = abs(f1_train_score-f1_test_score)

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            #save the trained model
            logging.info(f"Saving mode object")
            save_object(file_path=self.model_trainer_config.model_path, obj=model)

            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifacts(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")


            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
