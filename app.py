import streamlit as st
import pandas as pd


FILE_PATH = "saved_artifacts\wafer_13012020_090817.csv"

# Streamlit webpage title
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'prediction_project'

def navigate(page):
    st.session_state['current_page'] = page

def home_page():
    st.subheader("Problem Statement:")    

def upload_csv():
    # Upload CSV file
  uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

  # Process uploaded file
  if uploaded_file is not None:
    try:
      df = pd.read_csv(uploaded_file)
      st.success("File uploaded successfully!")

      # Display uploaded data (optional)
      st.dataframe(df)

    except Exception as e:
      st.error("An error occurred while processing the file. Please ensure it's a valid CSV format.")
    
def download_sample():
   # Download button functionality
  if st.button("Download Sample CSV"):
    try:
      # Read CSV data
      with open(FILE_PATH, "rb") as file:
        csv_content = file.read()

      # Create a hidden link with file data
      href = f"<a href=data:text/csv;base64,{st.secrets.text_to_base64(csv_content)} download='wafer_13012020_090817.csv'>Download</a>"
      st.markdown(href, unsafe_allow_html=True)

      # Informative message
      st.success("Click the 'Download' link to download the CSV file.")

    except FileNotFoundError:
      st.error("File not found. Please check the file path.")
    except Exception as e:
      st.error(f"An error occurred: {str(e)}")

def pred_page():
    """
    This function defines the core functionalities of the Streamlit app.
    """
    st.subheader("Prediction page:")
    download_sample()
    upload_csv()

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