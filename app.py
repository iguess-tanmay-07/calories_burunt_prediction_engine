import streamlit as st
import pandas as pd
import pickle

# 1. Set up the title of the web page
st.set_page_config(page_title="Calories Predictor", layout="centered")
st.title("🔥 Calories Burnt Prediction Engine")
st.write("Enter your workout details below to predict calories burned.")

# 2. Automatically load the saved model 'brain' we created in Step 1
@st.cache_resource
def load_model():
    with open('calories_model.pkl', 'rb') as file:
        return pickle.load(file)

model = load_model()

# 3. Create the input fields on the screen for the user to fill out
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=25)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0)

with col2:
    duration = st.number_input("Duration of Workout (minutes)", min_value=1.0, max_value=180.0, value=30.0)
    heart_rate = st.number_input("Heart Rate (BPM)", min_value=40.0, max_value=240.0, value=100.0)
    body_temp = st.number_input("Body Temperature (°C)", min_value=35.0, max_value=43.0, value=38.0)

# 4. What happens when the user clicks the "Calculate" button
if st.button("Calculate Calories Burnt", use_container_width=True):
    
    # Convert 'Male' or 'Female' to 0 or 1, exactly how your model learned it
    gender_encoded = 0 if gender == "Male" else 1
    
    # Put the inputs into a structured format the model expects
    input_data = pd.DataFrame([{
        'Gender': gender_encoded,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'Duration': duration,
        'Heart_Rate': heart_rate,
        'Body_Temp': body_temp
    }])
    
    # Feed data to the model and get the prediction
    prediction = model.predict(input_data)[0]
    
    # Show the result to the user
    st.success(f"✨ Estimated Calories Burnt: **{prediction:.2f} kcal**")