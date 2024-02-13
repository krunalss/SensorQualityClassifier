import os
import requests
import zipfile
from sensorqualityclassifier.utils.logger import AppLogger
import yaml

class DataIngestionPipeline:
    """
    A data ingestion pipeline class that handles downloading,
    unzipping, and saving batch files containing wafer sensor data.
    """

    def __init__(self, config_path='config/config.yml'):
        """
        Initializes the DataIngestionPipeline with the necessary configuration.
        """
        self.config = self.read_config(config_path)
        self.logger = AppLogger()
        # Ensure the root directory exists
        self.ensure_directory(self.config['root_directory'])

    @staticmethod
    def read_config(config_path):
        """
        Reads the YAML configuration file.
        """
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    @staticmethod
    def ensure_directory(path):
        """
        Ensures the specified directory exists. Creates it if it does not.
        """
        os.makedirs(path, exist_ok=True)

    def download_data(self):
        """
        Downloads the zip file from the source URL specified in the configuration file.
        """
        source_url = self.config['source_url']
        zip_path = os.path.join(self.config['root_directory'], 'data.zip')
        try:
            self.logger.log_info(f"Downloading data from {source_url}...")
            response = requests.get(source_url)

            if response.status_code == 200:
                with open(zip_path, 'wb') as file:
                    file.write(response.content)
                self.logger.log_info("Data download complete.")
            else:
                self.logger.log_error(f"Failed to download data. Status code: {response.status_code}")
        except Exception as e:
            self.logger.log_exception(f"An exception occurred during data download: {e}")

    def unzip_data(self):
        """
        Unzips the downloaded file and saves it to the root directory.
        """
        zip_path = os.path.join(self.config['root_directory'], 'data.zip')
        try:
            if not os.path.exists(zip_path):
                self.logger.log_error(f"Zip file does not exist: {zip_path}")
                return

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                self.logger.log_info("Unzipping the data...")
                zip_ref.extractall(self.config['root_directory'])
                self.logger.log_info("Data unzipping complete.")
            os.remove(zip_path)
        except Exception as e:
            self.logger.log_exception(f"An exception occurred during data unzipping: {e}")

    def ingest_data(self):
        """
        Public method to initiate the data ingestion process.
        """
        self.download_data()
        self.unzip_data()

# Example usage
if __name__ == "__main__":
    ingestion_pipeline = DataIngestionPipeline()
    ingestion_pipeline.ingest_data()
