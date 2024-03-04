import os
from re import A
from sre_constants import SUCCESS
import pandas as pd
from dotenv import load_dotenv
from sensorqualityclassifier.utils.logger import AppLogger
from sensorqualityclassifier.pipeline.data_transform_and_loading_pipeline import DataLoadingPipeline
from sensorqualityclassifier.pipeline.data_validation_pipeline import DataValidationPipeline
import json
import joblib

class InferencePipeline:
    """
    A pipeline to load data from CSV files in prediction_dir, preprocess it,
    and predict the result.
    """

    def __init__(self, config_path='config/config.yml',schema_path='config/schema_training.json'):
        self.logger = AppLogger()
        self.config = self.read_yaml_file(config_path)      
        self.schema = self.read_json_file(schema_path)
        self.prediction_dir = self.config['prediction_dir']
        self.output_dir= self.config['output_dir']
        self.model_path=self.config['load_model']
        self.ensure_directory(self.config['output_dir'])

    @staticmethod
    def ensure_directory(path):
        """
        Ensures the specified directory exists. Creates it if it does not.
        """
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def read_yaml_file(file_path):
        """
        Reads a YAML configuration file.
        """
        import yaml
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
        
    @staticmethod
    def read_json_file(file_path):
        """
        Reads a JSON file and returns its content.

        Parameters:
            file_path (str): Path to the JSON file.

        Returns:
            dict: Content of the JSON file.
        """
        with open(file_path, 'r') as file:
            return json.load(file)
        
    def validate_columns(self, file_path):
        """
        Validates the number of columns in a file against the expected number.

        Parameters:
            file_path (str): Path to the file to validate.

        Returns:
            bool: True if the number of columns is valid, False otherwise.
        """
        self.logger.log_info("-----------inside validation-----------")
        expected_num_columns = self.schema['NumberofColumns'] -1
        df = pd.read_csv(file_path)
        self.logger.log_info(f"========file column size{df.shape[1]}")
        self.logger.log_info(f"========exp no. of columns{expected_num_columns}")
        return df.shape[1] == expected_num_columns
    

    def run_inference(self):
        
        try:
            dfs = []
            column_name = 'good_bad'
            files = os.listdir(self.prediction_dir)
            for file in files:
                file_path = os.path.join(self.prediction_dir, file)
                if self.validate_columns(file_path):
                    df = pd.read_csv(file_path)
                    df = df.drop(df.columns[0], axis=1)
                    has_nan = df.isna().any().any()
                    if has_nan:
                        self.logger.log_info("There are NaN values in the DataFrame.")
                    else:
                         self.logger.log_info("No NaN values found in the DataFrame.")
                    
                    df.fillna(0, inplace=True)
                    has_nan = df.isna().any().any()
                    
                    if has_nan:
                        self.logger.log_info("\n2 There are NaN values in the DataFrame.")
                    else:
                         self.logger.log_info("\n2 No NaN values found in the DataFrame.")
                    #self.logger.log_info(df.head())
                    df.columns = [col.replace('-', '_').replace('/', '_').lower() for col in df.columns]
                    #df.to_csv('dfoutput.csv', index=False)
                    
                    
                    # Load the model
                    model = joblib.load(self.model_path)
                    #self.logger.log_info(f"========dir====={dir(model)}")

                    #self.logger.log_info(f"========vars====={vars(model)}")
                    """
                    first_row = df.iloc[[0]].values  # Extracting the first row
                    columns_names = df.columns  # Extracting column names
                    another_df = pd.DataFrame([first_row[0]],columns=columns_names) # Creating another DataFrame with the first row data
                    self.logger.log_info(f"==========another_df=====\n{another_df.head}")
                    another_df.to_csv('Myoutput.csv', index=False)
                    """

                    # Make predictions
                    good_bad = model.predict(df)
                    self.logger.log_info(f"============good_bad=========\n{good_bad}")
                    results = pd.DataFrame(good_bad)
                    dfs.append(results)
                
            # Save results
            # Concatenate all DataFrames into one
            final_df = pd.concat(dfs, ignore_index=True)
            final_df.columns = [column_name]
            output_file = os.path.join(self.output_dir, "inference_results.csv")
                
            final_df.to_csv(output_file, index=False)
            
            # Assuming 'df' is your DataFrame containing values 1 and -1
            counts = final_df[column_name].value_counts()

            # Access counts for 1 and -1
            count_of_1 = counts.get(1, 0)
            count_of_minus_1 = counts.get(-1, 0)

            self.logger.log_info(f"Count of 1:{count_of_1}")
            self.logger.log_info(f"Count of -1:{count_of_minus_1}")
            
                

            #Delete the input CSV file
            #os.remove(self.config["prediction_dir"])

            return count_of_1,count_of_minus_1
                    
        except Exception as e:
            self.logger.log_exception("Pipeline execution failed: {}".format(e))
            
            
        

            
if __name__ == "__main__":
    inference_runner = InferencePipeline()
    good,bad=inference_runner.run_inference()
    print(f"goood={good}, bad={bad}")

    
