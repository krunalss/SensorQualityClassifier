import os
import pandas as pd
from dotenv import load_dotenv
import hopsworks
import hsfs
from hsml.schema import Schema
from hsml.model_schema import ModelSchema
from sklearn import metrics
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score
import joblib
from sensorqualityclassifier.utils.logger import AppLogger

class ModelTrainingPipeline:
    """
    A pipeline for training an XGBoost model using data from Hopsworks' feature store,
    with functionalities to preprocess data, train the model, evaluate its performance,
    and save the model both locally and in Hopsworks.
    """

    def __init__(self, config_path='config/config.yml', env_path='config/.env'):
        """
        Initializes the pipeline, loads configurations and Hopsworks credentials.
        """
        self.logger = AppLogger()
        load_dotenv(dotenv_path=env_path)
        self.config = self.read_yaml_file(config_path)
        self.connect_to_hopsworks()

    def read_yaml_file(self, file_path):
        """
        Reads configuration settings from a YAML file.
        """
        import yaml
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def connect_to_hopsworks(self):
        """
        Establishes a connection to the Hopsworks feature store.
        """
        try:
            self.project = hopsworks.login(
                api_key_value=os.getenv('FS_API_KEY'),
                project=os.getenv('FS_PROJECT_NAME')
            )
            self.fs = self.project.get_feature_store()
            self.logger.log_info("Connected to Hopsworks feature store.")
        except Exception as e:
            self.logger.log_exception("Failed to connect to Hopsworks: {}".format(e))
            raise

    def fetch_data_from_feature_store(self):
        """
        Fetches training data from the feature store.
        """
        try:
            feature_group = self.fs.get_feature_group('wafer_project', version=1)
            query = feature_group.select_all()
            feature_dataframe = query.read()
            self.logger.log_info("Data fetched from feature store.")
            return feature_dataframe
        except Exception as e:
            self.logger.log_exception("Failed to fetch data from feature store: {}".format(e))
            raise

    
    def train_and_evaluate_model(self, X, y):
        """
        Trains an XGBoost classifier and evaluates its performance.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        self.logger.log_info(f"========X_train=\n{X_train.head()}")
        self.logger.log_info(f"========X_test=\n{X_test.head()}")
        self.logger.log_info(f"========y_train=\n{y_train.head()}")
        self.logger.log_info(f"========y_test=\n{y_test.head()}")


        clf = xgb.XGBClassifier(objective='binary:logistic', n_estimators=100, learning_rate=0.1, max_depth=3, eval_metric='logloss')
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        formatted_accuracy = "{:.2f}".format(accuracy * 100)
        f1 = f1_score(y_test, y_pred)
        
        metrics = {
                "accuracy" : formatted_accuracy 
        }
        #metrics=str(metrics)
        #self.logger.log_info(f"Model trained. Accuracy: {accuracy:.4f}, F1 Score: {f1:.4f}")
        self.logger.log_info(f"metrics========={metrics} type========={type(metrics)}")

        return clf,metrics

    def save_model(self, model,metrics,X_train,y_train):
        """
        Saves the trained model locally and registers it in Hopsworks.
        """
        self.logger.log_info(f"<<<<<<<save_model method>>>>> metrics{type(metrics)}")
        model_dir = self.config['saved_model']
        if not os.path.isdir(model_dir):
            os.makedirs(model_dir)
        model_path = os.path.join(model_dir, 'xgboost_model.pkl')
        joblib.dump(model, model_path)
        self.logger.log_info(f"Model saved locally at {model_path}")

        # Model registration in Hopsworks is handled separately
        self.register_model_in_hopsworks(model_dir,metrics,X_train,y_train)

    def register_model_in_hopsworks(self, model_dir,metrics,X_train,y_train):
        """
        Registers the trained model in Hopsworks' model registry.
        """
        try:
            # Model Schema creation and registration steps...
            self.logger.log_info(f"<<<<<<<hopsworks_save_model method>>>>> metrics{type(metrics)}")

            # Create a Schema for the input features using the values of X_train
            input_schema = Schema(X_train.values)

            # Create a Schema for the output using y_train
            output_schema = Schema(y_train)

            # Create a ModelSchema using the defined input and output schemas
            model_schema = ModelSchema(input_schema=input_schema, output_schema=output_schema)

            # Convert the model schema to a dictionary for inspection
            model_schema.to_dict()

            # Get the model registry
            mr = self.project.get_model_registry()

            # Create a Python model named "sensor" in the model registry
            sensor_model = mr.python.create_model(
            name="sensor", 
            metrics=metrics,             # Specify the metrics used to evaluate the model
            model_schema=model_schema,   # Use the previously defined model schema
            # input_example=[4700702588013561],  # Provide an input example for testing deployments
            description="detection of sensor's wafer condition whether it is good or bad",  # Add a description for the model
            )

            # Save the model to the specified directory
            sensor_model.save(model_dir)
            
            self.logger.log_info("Model registered in Hopsworks.")

        except Exception as e:
            self.logger.log_exception(f"Failed to register model in Hopsworks: {e}")

    def run_pipeline(self):
        """
        Executes the model training pipeline.
        """
        try:
            df = self.fetch_data_from_feature_store()
            columns_to_drop = ['good_bad', 'wafer_num']
            X = df.drop(columns=columns_to_drop)
            y = df['good_bad']

            self.logger.log_info(f"========X=\n{X.head()}")
            self.logger.log_info(f"========y=\n{y.head()}")
            model,metrics= self.train_and_evaluate_model(X, y)
            self.logger.log_info(f"model type={type(model)}=========<>metrics type={type(metrics)}")
            self.save_model(model,metrics,X,y)
        except Exception as e:
            self.logger.log_exception("Pipeline execution failed: {}".format(e))

if __name__ == "__main__":
    pipeline = ModelTrainingPipeline()
    pipeline.run_pipeline()
