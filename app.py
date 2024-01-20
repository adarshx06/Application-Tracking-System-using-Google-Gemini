import base64
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pandas as pd
import pdf2image as p2i
import io
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#here taking the content and give to model base on prompt(prompt means which this model need to be doing)
def get_gemini_response(input, pdf_content,prompt):
    model= genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, pdf_content[0],prompt])
    return response.text

#here convert the pdf to image
def input_pdf_con(uploaded_file):
    if uploaded_file is not None:
        
        pdf_to_img = p2i.convert_from_bytes(uploaded_file.read())
        first_page = pdf_to_img[0]

        #here convert to image
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #here encode to base64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


#here for Streamlit App

st.set_page_config(page_title="ATS using Google Gemini", page_icon=":gem:", layout="wide")
st.header("ATS using Google Gemini")
input_text =st.text_area("Enter the Job Description", key="input")
uploaded_file = st.file_uploader("Upload your CV/Resume in PDF format", type=["pdf"])

if uploaded_file is not None:
    st.write("Uploaded CV/Resume")

submit1 = st.button("How is my Resume? 😊")
submit2= st.button(" How can I improvise? 😔. Also, Tell me about the keywords i am missing 😎")
submit3 = st.button("How much percentage it matches with my CV/Resume 😇")


input_prompt1=""" Your task is to review the provided how the resume is it fit for other ATS, Fonts are good, Are there any mistakes, grammar.Please share your professional evaluation on 
whether the candidate's resume is good or bad. Also, Highlight the strengths and weaknesses of the resume"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, machine learning, web development, 
full stack development, Computer science Domain and ATS functionality, your task here is to evaluate the resume against the provided job description. And Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""
input_prompt3 = """Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_con(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Repsonse Is:")
        st.write(response)
    else:
        st.write("Please upload the CV/Resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_con(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("Repsonse Is:")
        st.write(response)
    else:
        st.write("Please upload the CV/Resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_con(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("Repsonse Is:")
        st.write(response)
    else:
        st.write("Please upload the CV/Resume")





