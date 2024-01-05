from dotenv import load_dotenv
load_dotenv() # Load the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
              "mime_type": uploaded_file.type,
              "data": bytes_data  
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App

st.set_page_config(page_title='Multi-lingual Invoice Extractor')
st.header('Multi-lingual Invoice Extractor')

input = st.text_input("Input Prompt: ", key='input')
uploaded_file = st.file_uploader("Choose Invoice Image", type=["jpg", "jpeg", "png"])

image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='uploaded image!', use_column_width=True)
    

submit = st.button('Extract from invoice')

input_prompt = """
You are an expert in understanding invoice. We upload an invoice as an image 
and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Well...")
    st.write(response)