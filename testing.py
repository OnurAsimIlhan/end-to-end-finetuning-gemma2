from google.cloud import aiplatform
import streamlit as st
import os

# Set your project and endpoint details
project = "565951471021"
endpoint_id = "9175012216930304000"
location = "us-central1"

# Streamlit sidebar for settings
st.sidebar.title("Settings")
# Sidebar file uploader for JSON file
uploaded_file = st.sidebar.file_uploader("Upload your Google Cloud API Key JSON file:", type="json")
uploaded = False

# Initialize environment variable
if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with open("google_credentials.json", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Set the environment variable to the path of the saved file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"
    st.sidebar.success("API Key uploaded successfully.")
    uploaded = True
else:
    st.sidebar.info("Please upload a JSON file with your Google Cloud credentials.")

# Initialize the AI Platform with the project and location
if uploaded:
    aiplatform.init(project=project, location=location)
    endpoint = aiplatform.Endpoint("projects/" + project + "/locations/" + location + "/endpoints/" + endpoint_id)

    # Text inputs for instruction and input data
    instruction = st.text_input("Instruction", "Match the potential use case with the corresponding activity and emission values based on the provided context.")
    input_text = st.text_area("Input", "Doğal Gaz Kullanımı, Gaz Faturası Yönetimi, Isınma Maliyetleri, Enerji Tasarrufu, Gaz Dağıtımı")

    if st.button("Generate Response"):
        with st.spinner("Generating response..."):
            instances = [
                {
                    "inputs": f"Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request. \n\n### Instruction: {instruction} \n\n### Input: {input_text} \n\n### Response:",
                    "parameters": {}
                }
            ]

            completions = endpoint.predict(instances=instances)

            st.write("Predictions:")
            for p in completions.predictions:
                st.write(p)
