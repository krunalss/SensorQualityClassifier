import os
import pandas as pd
import re
import json
from sensorqualityclassifier.utils.logger import AppLogger

class DataValidationPipeline:
    """
    A pipeline for validating training data files based on various criteria including
    file name format, number of columns, and column names as specified in a JSON schema.

    Attributes:
        config (dict): Configuration settings loaded from a YAML file.
        schema (dict): Validation schema loaded from a JSON file.
        logger (AppLogger): Logger for logging information and errors.
        good_data_folder (str): Path to folder for valid files.
        bad_data_folder (str): Path to folder for invalid files.
        training_batch_files_dir (str): Directory containing the training batch files.
    """

    def __init__(self, config_path='config/config.yml', schema_path='config/schema_training.json'):
        """
        Initializes the DataValidationPipeline with paths to the configuration and schema files.

        Parameters:
            config_path (str): Path to the YAML configuration file.
            schema_path (str): Path to the JSON schema file.
        """
        self.config = self.read_yaml_file(config_path)
        self.schema = self.read_json_file(schema_path)
        self.logger = AppLogger()
        self.good_data_folder = 'artifacts/training_data/Good_Data_Folder'
        self.bad_data_folder = 'artifacts/training_data/Bad_Data_Folder'
        #self.training_batch_files_dir = self.config['unzip_dir']
        self.training_batch_files_dir = os.path.join(self.config['unzip_dir'], "Training_Batch_Files")
        self.ensure_directory(self.good_data_folder)
        self.ensure_directory(self.bad_data_folder)

    @staticmethod
    def read_yaml_file(file_path):
        """
        Reads a YAML file and returns its content.

        Parameters:
            file_path (str): Path to the YAML file.

        Returns:
            dict: Content of the YAML file.
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

    @staticmethod
    def ensure_directory(path):
        """
        Ensures that a directory exists.

        Parameters:
            path (str): Path to the directory.
        """
        os.makedirs(path, exist_ok=True)

    def validate_file_name(self, file_name):
        """
        Validates a file name against the regex pattern derived from the schema.

        Parameters:
            file_name (str): Name of the file to validate.

        Returns:
            bool: True if the file name is valid, False otherwise.
        """
        pattern = self.schema['SampleFileName']
        date_length = self.schema['LengthOfDateStampInFile']
        time_length = self.schema['LengthOfTimeStampInFile']
        regex = '[Ww]afer_' + '\d{' + str(date_length) + '}' + '_' + '\d{' + str(time_length) + '}\.csv$'
        #regex ="['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        print(f"file name={file_name} regex= {regex}")
        return bool(re.match(regex, file_name))
    
    def validate_columns(self, file_path):
        """
        Validates the number of columns in a file against the expected number.

        Parameters:
            file_path (str): Path to the file to validate.

        Returns:
            bool: True if the number of columns is valid, False otherwise.
        """
        expected_num_columns = self.schema['NumberofColumns']
        df = pd.read_csv(file_path)
        return df.shape[1] == expected_num_columns

    def move_file(self, file_path, destination_folder):
        """
        Moves a file to a specified destination folder.

        Parameters:
            file_path (str): Path to the file to move.
            destination_folder (str): Path to the destination folder.
        """
        try:
            os.rename(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
        except Exception as e:
            self.logger.log_exception(f"Error moving file {file_path} to {destination_folder}: {e}")

    def validate_and_move_files(self):
        """
        Validates files in the training batch directory and moves them to either
        the good or bad data folder based on the validation outcome.
        """
        files = os.listdir(self.training_batch_files_dir)
        for file in files:
            file_path = os.path.join(self.training_batch_files_dir, file)
            if self.validate_file_name(file):
                if self.validate_columns(file_path):
                    self.move_file(file_path, self.good_data_folder)
                    self.logger.log_info(f"File {file} moved to Good_Data_Folder.")
                else:
                    self.move_file(file_path, self.bad_data_folder)
                    self.logger.log_info(f"File {file} moved to Bad_Data_Folder due to column validation failure.")
            else:
                self.move_file(file_path, self.bad_data_folder)
                self.logger.log_info(f"File {file} moved to Bad_Data_Folder due to file name validation failure.")

# Example usage
if __name__ == "__main__":
    validator = DataValidationPipeline()
    validator.validate_and_move_files()
