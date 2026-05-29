import streamlit as st
from PIL import Image
from google import genai
import os

st.set_page_config(page_title="My AI Doctor", layout="wide")

# Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")

st.title("🩺 My AI Doctor")
st.write("AI-Powered Healthcare Assistant Demo")

# Sidebar
st.sidebar.header("Patient Details")

age = st.sidebar.number_input("Age", 1, 100, 25)
height = st.sidebar.number_input("Height (cm)", 100, 220, 170)
weight = st.sidebar.number_input("Weight (kg)", 20, 200, 70)

# BMI
bmi = weight / ((height / 100) ** 2)

col1, col2 = st.columns(2)

with col1:
    st.metric("BMI", round(bmi, 2))

with col2:
    if bmi < 18.5:
        st.warning("Underweight")
    elif bmi < 25:
        st.success("Normal Weight")
    elif bmi < 30:
        st.warning("Overweight")
    else:
        st.error("Obese")

# Food Scanner
st.header("🍔 AI Food Scanner")

food_image = st.file_uploader(
    "Upload Food Image",
    type=["jpg", "jpeg", "png"]
)

if food_image:
    image = Image.open(food_image)
    st.image(image, width=300)

    st.info("Food analysis demo")

# AI Coach
st.header("🤖 AI Coach")

question = st.text_input(
    "Ask a health-related question"
)

if st.button("Get Advice"):

    if API_KEY and question:

        client = genai.Client(api_key=API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )

        st.success("AI Response")
        st.write(response.text)

    else:
        st.warning("Enter a question")

# Footer
st.markdown("---")
st.write("Built with Python, Streamlit and Gemini AI")
