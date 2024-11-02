from google.cloud import aiplatform
import streamlit as st
import os

# Set your project and endpoint details
project = "565951471021"
endpoint_id = "8468510025386557440"
location = "us-central1"

# Streamlit sidebar for settings
st.sidebar.title("Settings")
st.sidebar.markdown("Configure your environment and upload credentials.")

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

# Main page layout
st.title("Activity and Emission Rates Predictor")
st.markdown("""
    This app helps you generate responses for potential use cases by matching them to relevant activities and emission values.
    Fill in the inputs below and click on **Generate Response**.
""")
st.divider()

# Text inputs and form layout
if uploaded:
    aiplatform.init(project=project, location=location)
    endpoint = aiplatform.Endpoint(f"projects/{project}/locations/{location}/endpoints/{endpoint_id}")

    with st.form("input_form"):
        st.subheader("Input Details")
        
        instruction = st.text_area(
            "Instruction",
            "Match the potential use case with the corresponding activity and emission values based on the provided context.",
            height=100,
            disabled=True
        )
        
        input_val = st.text_input("Potential Use Case", "Elektrik Hizmetleri, Enerji Dağıtımı, Elektrik Üretimi, Elektrik İletimi, Elektrik Faturası Yönetimi")
        
        # Create columns for a better layout of context fields
        col1, col2 = st.columns(2)
        with col1:
            year = st.text_input("Year", "2020")
            category = st.text_input("Category", "Electricity")
            source = st.text_input("Source", "Government of Canada")
        with col2:
            region = st.text_input("Region", "Canada (CA)")
            unit_type = st.text_input("Unit Type", "Energy")
            extra = st.text_input("Additional Context", "")

        # Construct the context string from individual fields
        context = f"Year: {year}, Category: {category}, Source: {source}, Region: {region}, Unit Type: {unit_type}"

        submit_button = st.form_submit_button("Generate Response")

    if submit_button:
        st.subheader("Results")
        with st.spinner("Generating response..."):
            instances = [
                {
                    "inputs": f"Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction: {instruction}\n\n### Input: {input_val}\n\n### Context: {context}\n\n### Response:",
                    "parameters": {}
                }
            ]

            completions = endpoint.predict(instances=instances)
            for p in completions.predictions:
                st.markdown(f"**Response:** s{p}")
else:
    st.error("Please upload a valid JSON API key to proceed.")
