import os
import pandas as pd
from dotenv import load_dotenv
import hopsworks
from sensorqualityclassifier.utils.logger import AppLogger

class DataLoadingPipeline:
    """
    A pipeline to load data from CSV files in the good_data_folder, preprocess it,
    and push it to Hopsworks feature store.
    """
    
    def __init__(self, config_path='config/config.yml', env_path='config/.env'):
        self.logger = AppLogger()
        self.config = self.read_yaml_file(config_path)
        load_dotenv(dotenv_path=env_path)
        
        # Hopsworks credentials
        self.fs_api_key = os.getenv('FS_API_KEY')
        self.fs_project_name = os.getenv('FS_PROJECT_NAME')
        
        self.good_data_folder = self.config['good_data_folder']

    @staticmethod
    def read_yaml_file(file_path):
        """
        Reads a YAML configuration file.
        """
        import yaml
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def preprocess_data(self, df):
        """
         Preprocesses the DataFrame before pushing to Hopsworks:
        - Renames the first column to 'wafer_num'.
        - Replaces '-' and '/' with '_' in column names and converts them to lowercase.
        - Converts all column data types to double except for 'good_bad', which is converted to int.

        Parameters:
        df (pd.DataFrame): The DataFrame to preprocess.

        Returns:
        pd.DataFrame: The preprocessed DataFrame.
        """

        new_columns = df.columns.tolist()
        new_columns[0] = 'wafer_num'
        df.columns = new_columns
        df.columns = [col.replace('-', '_').replace('/', '_').lower() for col in df.columns]

        return df

    def push_data_to_hopsworks(self, df):
        """
        Pushes preprocessed DataFrame to Hopsworks feature store.
        """
        try:
            self.logger.log_info(f"push_data_to_hopsworks_shape={df.shape}")
            self.logger.log_info(f"push_data_to_hopsworks_head={df.head()}")
            project = hopsworks.login(api_key_value=self.fs_api_key, project=self.fs_project_name)
            fs = project.get_feature_store() 

            wafer_fg = fs.get_or_create_feature_group(
                name="wafer_project",
                version=1,
                description="good_training_data",
                primary_key=["wafer_num"],
            )
            wafer_fg.insert(df)
            return True
        except Exception as e:
            self.logger.log_exception(f"Failed to push data to Hopsworks: {e}")
            return False

    def load_and_push_data(self):
        """
        Loads data from all CSV files in good_data_folder, aggregates it into a single DataFrame,
        preprocesses, and pushes it to Hopswork
        """
        all_data_frames = []  # List to store individual data frames for each file
        
        for filename in os.listdir(self.good_data_folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(self.good_data_folder, filename)
                try:
                    df = pd.read_csv(file_path)
                    all_data_frames.append(df)
                    self.logger.log_info(f"Successfully loaded {filename} for preprocessing.")
                except Exception as e:
                    self.logger.log_exception(f"Error loading {filename}: {e}")

        # Concatenate all data frames if not empty
        if all_data_frames:
            combined_df = pd.concat(all_data_frames, ignore_index=True)
            combined_df = self.preprocess_data(combined_df)  # Preprocess the combined data frame

            # Convert all column data types except 'good_bad'
            for col in combined_df.columns:
                if col== 'wafer_num':
                    combined_df[col] = combined_df[col].astype(str)
                elif col == 'good_bad':
                    combined_df[col] = combined_df[col].astype(int)
                else:
                    combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce').astype('float64')
            self.logger.log_info(combined_df.head())
            self.logger.log_info(combined_df.shape)
            if self.push_data_to_hopsworks(combined_df):
                self.logger.log_info("All data successfully pushed to Hopsworks.")
            else:
                self.logger.log_error("Failed to push data to Hopsworks.")
        else:
            self.logger.log_info("No data files found for processing.")

# Example usage
if __name__ == "__main__":
    data_loader = DataLoadingPipeline()
    data_loader.load_and_push_data()
