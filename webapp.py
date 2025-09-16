import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

api=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api)
model=genai.GenerativeModel("gemini-2.5-flash-lite")


# Lets Create the UI
st.title(":orange[HEALTHIFY] :blue[AI POWERED HEALTH ASSISTANT]")

st.markdown("""
#### This application will assist you to have a better and healthy life.  
You can ask anything related to health and fitness and get recommendations.
""")

st.sidebar.header(":orange[Enter your details]")

tips = '''Follow the steps 
1. Enter you details
2. Enter your gender
3. Enter your age
4. Enter your weight
5. Enter your height
6.Select the number on the fitness scale (0-5). 5-Fittest , 0 - No fitness
'''
st.write(tips)
name  = st.sidebar.text_input("Enter Your Name ")
gender = st.sidebar.selectbox('Select your gender', ['Male', 'Female', 'Other'])
age=st.sidebar.number_input("Enter your Age",min_value=1,max_value=100)
weight=st.sidebar.number_input("Enter your Weight (in kgs)",min_value=1,max_value=300,value=1,step=1)  
height=st.sidebar.number_input("Enter your Height (in cms)",min_value=30,max_value=250,value=30,step=1)

bmi=pd.to_numeric(weight)/((pd.to_numeric(height)/100)**2)

fitness=st.sidebar.slider("Rate your Fitness Level (0-5)",min_value=0,max_value=5,value=0,step=1)
st.sidebar.write(f"Your BMI is {round(bmi,2)} kg/m^2")

# Lets use Genai model to get the output
user_query=st.text_input("Enter your Health related questions here-->")
prompt = f'''Assume you are a health expert . You are required to answer the question asked by the user based on the following details provided by the user
Name is {name}
Gender is {gender}
Age is {age} years
Weight is {weight} kgs
Height is  {height} cms
BMI is {round(bmi,2)} kg/m^2
and user rates his/her fitness level as {fitness} out of 5.

Your output should be in the following format:
* It should start by giving one two line comment on the details that are being provided by the user.
* It should explain what the real problem is based on the details provided by the user.
* It should provide all the possible causes for this problem.
* It should provide all possible solutions for this problem.
* It should also mention which doctor specialization should the user should for this problem.
* strictly do not recommend or advise any medicines.
* output should be in bullet points and use tables wherever possible.

here is the question asked by the user {user_query}
'''
if user_query:
    response = model.generate_content(prompt)
    st.write(response.text)