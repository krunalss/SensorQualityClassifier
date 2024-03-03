# Sensor Quality Classifier

This project aims to classify the quality of sensors based on various features extracted from sensor data. It consists of several Python scripts organized into a pipeline for data preprocessing, model training, inference, and evaluation. Below is an overview of the project structure and how to use it.

## Problem Statement:  
The inputs of various sensors for different wafers have been provided. In electronics, a wafer (also called a slice or substrate) is a thin slice of semiconductor used for the fabrication of integrated circuits. The goal is to build a machine learning model which predicts whether a wafer needs to be replaced or not(i.e., whether it is working or not) based on the inputs from various sensors. There are two classes: +1 and -1. 
•	+1 means that the wafer is in a working condition and it doesn’t need to be replaced.
•	-1 means that the wafer is faulty and it needs to be replaced. 


## Project Structure

- **config:** Contains configuration files.
- **data:** Directory to store data files.
- **sensorqualityclassifier:**
  - **pipeline:**
    - **data_transform_and_loading_pipeline.py:** Module for data loading and preprocessing.
    - **model_training_pipeline.py:** Module for training the classification model.
    - **inference_pipeline.py:** Module for running inference on new data.
  - **utils:** Utility functions used across the project like logger.
- **README.md:** Overview and instructions for the project.

## Tools and Technologies

In this project, we have utilized several tools and technologies to streamline the development, deployment, and operation processes:

1. **Poetry**: Manages the project's environment setup and dependencies.
2. **Hopsworks**: Used for data loading, which aids in data versioning, data integrity, and monitoring for data drift and concept drift.
3. **XGBClassifier**: we have utilized the `XGBClassifier` from XGBoost for solving the binary classification problem. XGBoost is an optimized distributed gradient boosting library designed to be highly efficient, flexible, and portable.
4. **Hopsworks**: Employed for model registry to maintain and manage different versions of the models.
5. **Streamlit**: Utilized to create a prototype user interface for demonstrating the model's usage.
6. **GitHub Actions**: Implements CI/CD pipelines to automate the testing and deployment processes.
7. **Docker**: Used to containerize the application, ensuring consistency across various development and deployment environments.
8. **Heroku**: Serves as the platform for hosting the application during the development phase.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/sensor-quality-classifier.git
   cd sensor-quality-classifier
   ```

2. Install the required Python dependencies:
 ```bash 
 pip install -r requirements.txt
 ```


## Usage

### Data Loading and Preprocessing

Modify the configuration file `config/config.yml` according to your data locations and parameters.

Run the data loading and preprocessing pipeline:
```python 
python sensorqualityclassifier/pipeline/data_transform_and_loading_pipeline.py
```
### Model Training

Modify the configuration file `config/config.yml` if necessary.

Run the model training pipeline:
```python
python sensorqualityclassifier/pipeline/model_training_pipeline.py
```
### Inference

Ensure that the trained model is available at the location specified in the configuration.

Modify the configuration file `config/config.yml` if necessary.

Run the inference pipeline:
```python
python sensorqualityclassifier/pipeline/inference_pipeline.py
```

## Configuration

The `config/config.yml` file contains various parameters such as file paths, model hyperparameters, and feature settings. Modify this file according to your requirements.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please open an issue or create a pull request.

## License
**Open-Source**
This project is licensed under the MIT License.

## Acknowledgments

This project is inspired by the need to classify sensor quality efficiently. Thanks to the contributors of the libraries used in this project.

## References
1. **Krish Naik**
- https://www.youtube.com/user/krishnaik06 
- https://github.com/krishnaik06

2. **Pau Labarta Bajo**
- https://github.com/Paulescu

3. **Hopsworks**  <img src="https://uploads-ssl.webflow.com/5f6353590bb01cacbcecfbac/6202a13e7cafec5553703f6b_logo.svg" width="40%" >

- https://docs.hopsworks.ai/machine-learning-api/3.7/generated/model-serving/model_serving_api/

- https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb#scrollTo=DH1vdELNF0Uw

## Contact
For any questions or inquiries, please contact krunalss@outlook.com