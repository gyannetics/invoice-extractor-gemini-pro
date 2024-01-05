"""
This module implements a Streamlit app for extracting information from invoices.
It utilizes the Google Generative AI's Gemini Pro Vision model for processing and
interpreting invoice images.
"""

# Standard library imports
import os

# Third-party library imports
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Load the model
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input_text, image_data, prompt):
    """
    Generates a response from the Gemini Pro Vision model.
    """
    try:
        response = model.generate_content([input_text, image_data[0], prompt])
        return response.text
    except Exception as e:
        return f"An error occurred while generating response: {str(e)}"

def input_image_setup(uploaded_file):
    """
    Processes an uploaded image file for model input.
    """
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    bytes_data = uploaded_file.getvalue()
    return [{"mime_type": uploaded_file.type, "data": bytes_data}]

def main():
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(page_title='Multi-lingual Invoice Extractor')
    st.header('Multi-lingual Invoice Extractor')

    user_query = st.text_input("Input Prompt: ", key='input')
    uploaded_file = st.file_uploader("Choose Invoice Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image!', use_column_width=True)

    submit = st.button('Extract from invoice')

    input_prompt = (
        "You are an expert in understanding invoices. We upload an invoice as an image "
        "and you will have to answer any questions based on the uploaded invoice image."
    )

    if submit and user_query:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, user_query)
            st.subheader("Response:")
            st.write(response)
        except FileNotFoundError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
