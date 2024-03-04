import streamlit as st
import pandas as pd
import os
from sensorqualityclassifier.pipeline.inference_pipeline import InferencePipeline
import shutil

# Streamlit webpage title
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'prediction_project'

def navigate(page):
    st.session_state['current_page'] = page

def home_page():
    problem_statement_text ="""The inputs of various sensors for different wafers have been provided. 
    <br> In electronics, a wafer (also called a slice or substrate) is a thin slice of semiconductor 
    used for the fabrication of integrated circuits. 
    The goal is to build a machine learning model which predicts whether a wafer needs
      to be replaced or not(i.e., whether it is working or not) based on the inputs from 
      various sensors. <br> <b>There are two classes: +1 and -1.</b>
      <br> •+1 means that the wafer is in a working condition and it doesn’t need to be replaced.
      <br> •-1 means that the wafer is faulty and it needs to be replaced.<br><br> """
    
    project_stucture_text="""

- **config:** Contains configuration files.
- **saved_artifacts:** Directory to store model artifacts files.
- **sensorqualityclassifier:**
  - **pipeline:**
    - **data_extraction_pipeline.py:** Module for downloading the traing data from the datasource mentioned in config.yml
    - **data_transform_and_loading_pipeline.py:** Module for data loading and preprocessing.
    - **model_training_pipeline.py:** Module for training the classification model.
    - **inference_pipeline.py:** Module for running inference on new data.
  - **utils:** Utility functions used across the project like logger.
- **README.md:** Overview and instructions for the project."""

    st.subheader("Problem Statement:")    
    st.markdown(f"<div style='text-align: justify;'>{problem_statement_text}</div>", unsafe_allow_html=True)

    st.subheader("Project Structure")
    st.markdown(f"<div style='text-align: justify;'>{project_stucture_text}</div>", unsafe_allow_html=True)

    if st.button("Lets Predict the Quality of wafer here"):
            navigate('prediction_project')

def upload_csv():
    # Upload CSV file
  uploaded_file = st.file_uploader("Choose a CSV file to Predict good and bad quality wafer", type="csv")
  

  # Process uploaded file
  if uploaded_file is not None:
    # To read file as string:
        stringio = uploaded_file.getvalue().decode("utf-8")
        
        # You can also save this file to the server
        # Specify the location where you want to save the file
        save_location = 'saved_artifacts/prediction_dir/' + uploaded_file.name

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(save_location), exist_ok=True)

        # Write the file to the specified location
        with open(save_location, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File {uploaded_file.name} uploaded and saved to {save_location}!")
    
def delete_csv():
  save_location= 'saved_artifacts/prediction_dir/'
  shutil.rmtree(save_location)
  print(f"Directory {save_location} has been removed")

def pred_page():
    """
    This function defines the core functionalities of the Streamlit app.
    """
    st.subheader("Prediction:")
    sample_file_text="""There are certain number of sensor readings are available for any wafer which is being used in production.
    Our AI Model  also required same number of sensor reading present in the input to accurately predict the condition of wafer.
    Inorder to get a proper input for prediction, following is sample input csv for your reference."""



    # URL to the file (this needs to be a direct link to the file)
    file_url = 'https://github.com/krunalss/SensorQualityClassifier/raw/main/saved_artifacts/wafer_13012020_090817.csv'

    # Create a clickable link to download the file
    st.markdown(f"<div style='text-align: justify;'>{sample_file_text}</div>", unsafe_allow_html=True)
    st.markdown(f"[Download file]({file_url})", unsafe_allow_html=True)
    
    upload_csv()
    
    if st.button('Run Inference'):
            inference_runner = InferencePipeline()
            good,bad=inference_runner.run_inference()  # Add arguments if your function requires them
            st.success('Inference run successfully')
            st.success(f'In the given input csv file, There are total {good} good quality wafers and {bad} bad quality wafers which needs to be replaced.')
            delete_csv()        

def main():
    # Navigation bar
    project_title="""<h1><div style='text-align: center; color: #ff6961;'>
                        <span>Semiconductor <br> Wafer Quality Classification </span>
                    </div></h1><br><br>
                 """
    st.markdown(project_title, unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("About the Project"):
            navigate('home')

    with col2:
        if st.button("Prediction"):
            navigate('prediction_project')

    # Display the selected page
    if st.session_state['current_page'] == 'home':
        home_page()
    elif st.session_state['current_page'] == 'prediction_project':
        pred_page()

if __name__ == "__main__":
    main()