import streamlit as st
import streamlit.components.v1 as components
import pickle
import numpy as np

# 1. Load your trained ML model (Adjust the filename/path to match yours)
@st.cache_resource
def load_model():
    with open('calories_model.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()

st.set_page_config(layout="centered")

# 2. Standard Streamlit Sidebar or Top Inputs to get data for the ML Model
st.sidebar.header("Update Your Metrics")
age = st.sidebar.number_input("Age", min_value=1, max_value=100, value=25)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=72)
duration = st.sidebar.number_input("Duration (min)", min_value=1, max_value=300, value=45)
heart_rate = st.sidebar.number_input("Heart Rate (bpm)", min_value=40, max_value=220, value=138)

# 3. Run the prediction when inputs change
# (Modify this features array to match the exact order your ML model expects!)
# --- PREDICTION ---
# This order matches the exact training shape expected by your XGBoost Regressor
features = np.array([[gender_numeric, age, height, weight, duration, heart_rate, body_temp]])
predicted_calories = model.predict(features)[0]
predicted_calories = round(float(predicted_calories))

# 4. Define the HTML & Inline CSS String with dynamic Python formatting
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #0e1117; /* Matches default Streamlit dark mode background */
      display: flex; justify-content: center; align-items: center; padding: 10px;
    }}
    .card-container {{
      background-color: #fcf8f2; width: 100%; max-width: 750px; border-radius: 24px; position: relative; font-family: sans-serif;
    }}
    .card-header {{
      background-color: #f5eae0; padding: 20px 32px; border-top-left-radius: 24px; border-top-right-radius: 24px;
      display: flex; justify-content: space-between; align-items: center;
    }}
    .brand-name {{ font-size: 1.25rem; font-weight: 600; color: #7d5a44; }}
    .streak-badge {{ background-color: #ebd9cb; color: #8c644d; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; }}
    .card-body {{ padding: 32px; display: flex; flex-direction: column; gap: 24px; }}
    .progress-section {{ display: flex; flex-direction: column; align-items: center; }}
    .progress-circle {{
      width: 130px; height: 130px; border-radius: 50%; border: 4px solid #ebd9cb;
      display: flex; justify-content: center; align-items: center; margin-bottom: 16px; background-color: #fcf8f2;
    }}
    .calorie-number {{ font-size: 2rem; font-weight: 500; color: #4a3629; }}
    .calorie-label {{ font-size: 1.1rem; font-weight: 600; color: #634737; margin-bottom: 2px; }}
    .calorie-subtext {{ font-size: 0.9rem; color: #a48674; }}
    .details-section {{ display: flex; flex-direction: column; gap: 12px; }}
    .section-title {{ font-size: 0.85rem; font-weight: 700; color: #c0967a; letter-spacing: 0.05em; }}
    .details-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
    .input-box {{ background-color: #ffffff; border: 1px solid #ebd9cb; border-radius: 12px; padding: 14px 18px; display: flex; flex-direction: column; gap: 4px; }}
    .input-label {{ font-size: 0.8rem; color: #bfa18f; font-weight: 500; }}
    .input-value {{ font-size: 1.3rem; font-weight: 600; color: #4a3629; }}
    .input-value .unit {{ font-size: 0.95rem; font-weight: 400; color: #927563; margin-left: 2px; }}
    .tip-box {{ background-color: #f2e7dd; border-radius: 12px; padding: 16px; font-size: 0.9rem; color: #7d5a44; }}
  </style>
</head>
<body>
  <div class="card-container">
    <header class="card-header">
      <h1 class="brand-name">Burnwise</h1>
      <span class="streak-badge">7 day streak</span>
    </header>
    <main class="card-body">
      <section class="progress-section">
        <div class="progress-circle">
          <span class="calorie-number">{predicted_calories}</span>
        </div>
        <h2 class="calorie-label">kcal estimated</h2>
        <p class="calorie-subtext">based on today's session</p>
      </section>
      <section class="details-section">
        <h3 class="section-title">YOUR DETAILS</h3>
        <div class="details-grid">
          <div class="input-box"><span class="input-label">Age</span><div class="input-value">{age} <span class="unit">yr</span></div></div>
          <div class="input-box"><span class="input-label">Weight</span><div class="input-value">{weight} <span class="unit">kg</span></div></div>
          <div class="input-box"><span class="input-label">Duration</span><div class="input-value">{duration} <span class="unit">min</span></div></div>
          <div class="input-box"><span class="input-label">Heart rate</span><div class="input-value">{heart_rate} <span class="unit">bpm</span></div></div>
        </div>
      </section>
      <div class="tip-box">
        <p><strong>Tip:</strong> A 30-min brisk walk burns around 180 kcal for your body weight.</p>
      </div>
    </main>
  </div>
</body>
</html>
"""

# 5. Render the custom frontend dashboard directly inside Streamlit
components.html(html_code, height=650, scrolling=False)
