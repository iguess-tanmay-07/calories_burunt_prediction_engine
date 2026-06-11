import streamlit as st
import streamlit.components.v1 as components
import pickle
import numpy as np

# 1. LOAD YOUR MODEL SAFELY
@st.cache_resource
def load_model():
    with open('calories_model.pkl', 'rb') as f:
        return pickle.load(f)

try:
    model = load_model()
except Exception:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

st.set_page_config(page_title="Burnwise", layout="centered")

# Hide standard Streamlit header/footer elements to keep the UI strictly clean
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)  # FIXED TYPO HERE

# 2. INITIALIZE SESSION STATE TO STORE THE PREDICTION
if 'predicted_calories' not in st.session_state:
    st.session_state.predicted_calories = 487  # Default placeholder value from the mockup

# 3. CAPTURE DATA FROM THE HTML FRONTEND VIA QUERY PARAMS
query_params = st.query_params

if 'calc' in query_params:
    try:
        # Pull parameters sent by the HTML form
        gender_val = 0 if query_params.get('gender', 'Male') == 'Male' else 1
        age_val = int(query_params.get('age', 25))
        height_val = float(query_params.get('height', 175))
        weight_val = float(query_params.get('weight', 72))
        duration_val = float(query_params.get('duration', 45))
        hr_val = float(query_params.get('heart_rate', 138))
        temp_val = float(query_params.get('body_temp', 37.0))
        
        # Format for XGBoost: [Gender, Age, Height, Weight, Duration, Heart_Rate, Body_Temp]
        features = np.array([[gender_val, age_val, height_val, weight_val, duration_val, hr_val, temp_val]])
        
        # Predict and save to session state
        prediction = model.predict(features)[0]
        st.session_state.predicted_calories = round(float(prediction))
        
        # Clear parameters to prevent infinite loops on page re-run
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Prediction processing error: {e}")

# 4. MONOLITHIC HTML/CSS APP FRONTEND WITH INLINE EDITABLE INPUTS
html_template = f"""
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
      background-color: #0e1117; 
      display: flex; justify-content: center; align-items: center; padding: 10px; overflow-x: hidden;
    }}
    .card-container {{ background-color: #fcf8f2; width: 100%; max-width: 650px; border-radius: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.15); margin: 20px auto; }}
    .card-header {{ background-color: #f5eae0; padding: 20px 32px; border-top-left-radius: 24px; border-top-right-radius: 24px; display: flex; justify-content: space-between; align-items: center; }}
    .brand-name {{ font-size: 1.25rem; font-weight: 600; color: #7d5a44; }}
    .streak-badge {{ background-color: #ebd9cb; color: #8c644d; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; }}
    .card-body {{ padding: 32px; display: flex; flex-direction: column; gap: 24px; }}
    .progress-section {{ display: flex; flex-direction: column; align-items: center; }}
    .progress-circle {{ width: 130px; height: 130px; border-radius: 50%; border: 4px solid #ebd9cb; display: flex; justify-content: center; align-items: center; margin-bottom: 16px; background-color: #fcf8f2; }}
    .calorie-number {{ font-size: 2.2rem; font-weight: 600; color: #4a3629; }}
    .calorie-label {{ font-size: 1.1rem; font-weight: 600; color: #634737; }}
    .calorie-subtext {{ font-size: 0.9rem; color: #a48674; }}
    
    .section-title {{ font-size: 0.85rem; font-weight: 700; color: #c0967a; letter-spacing: 0.05em; margin-bottom: -8px; }}
    .details-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
    
    .input-box {{ background-color: #ffffff; border: 1px solid #ebd9cb; border-radius: 12px; padding: 12px 16px; display: flex; flex-direction: column; }}
    .input-label {{ font-size: 0.8rem; color: #bfa18f; font-weight: 500; margin-bottom: 2px; }}
    
    .input-wrapper {{ display: flex; align-items: baseline; }}
    .input-field {{ border: none; outline: none; font-size: 1.3rem; font-weight: 600; color: #4a3629; width: 70%; font-family: inherit; background: transparent; }}
    .select-field {{ border: none; outline: none; font-size: 1.1rem; font-weight: 600; color: #4a3629; width: 100%; font-family: inherit; background: transparent; cursor: pointer; }}
    .unit {{ font-size: 0.95rem; font-weight: 400; color: #927563; margin-left: 4px; }}
    
    .tip-box {{ background-color: #f2e7dd; border-radius: 12px; padding: 16px; font-size: 0.9rem; color: #7d5a44; }}
    
    .cta-button {{
      background-color: #ca8a56; color: #ffffff; border: none; border-radius: 12px; padding: 16px; font-size: 1rem;
      font-weight: 600; cursor: pointer; transition: background-color 0.2s ease; width: 100%; text-align: left; padding-left: 24px;
    }}
    .cta-button:hover {{ background-color: #b57747; }}
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
          <span class="calorie-number">{st.session_state.predicted_calories}</span>
        </div>
        <h2 class="calorie-label">kcal estimated</h2>
        <p class="calorie-subtext">based on today's session</p>
      </section>
      
      <h3 class="section-title">YOUR DETAILS</h3>
      
      <div class="details-grid">
        <div class="input-box">
          <span class="input-label">Gender</span>
          <select id="gender" class="select-field">
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </div>
        
        <div class="input-box">
          <span class="input-label">Age</span>
          <div class="input-wrapper">
            <input type="number" id="age" class="input-field" value="25">
            <span class="unit">yr</span>
          </div>
        </div>
        
        <div class="input-box">
          <span class="input-label">Weight</span>
          <div class="input-wrapper">
            <input type="number" id="weight" class="input-field" value="72">
            <span class="unit">kg</span>
          </div>
        </div>
        
        <div class="input-box">
          <span class="input-label">Height</span>
          <div class="input-wrapper">
            <input type="number" id="height" class="input-field" value="175">
            <span class="unit">cm</span>
          </div>
        </div>
        
        <div class="input-box">
          <span class="input-label">Duration</span>
          <div class="input-wrapper">
            <input type="number" id="duration" class="input-field" value="45">
            <span class="unit">min</span>
          </div>
        </div>
        
        <div class="input-box">
          <span class="input-label">Heart rate</span>
          <div class="input-wrapper">
            <input type="number" id="heart_rate" class="input-field" value="138">
            <span class="unit">bpm</span>
          </div>
        </div>

        <input type="hidden" id="body_temp" value="37.0">
      </div>
      
      <div class="tip-box">
        <p><strong>Tip:</strong> A 30-min brisk walk burns around 180 kcal for your body weight.</p>
      </div>
      
      <button class="cta-button" onclick="sendDataToStreamlit()">Calculate my burn</button>
    </main>
  </div>

  <script>
    function sendDataToStreamlit() {{
      const gender = document.getElementById('gender').value;
      const age = document.getElementById('age').value;
      const weight = document.getElementById('weight').value;
      const height = document.getElementById('height').value;
      const duration = document.getElementById('duration').value;
      const heart_rate = document.getElementById('heart_rate').value;
      const body_temp = document.getElementById('body_temp').value;
      
      const url = new URL(window.parent.location.href);
      url.searchParams.set('calc', 'true');
      url.searchParams.set('gender', gender);
      url.searchParams.set('age', age);
      url.searchParams.set('weight', weight);
      url.searchParams.set('height', height);
      url.searchParams.set('duration', duration);
      url.searchParams.set('heart_rate', heart_rate);
      url.searchParams.set('body_temp', body_temp);
      
      window.parent.location.href = url.toString();
    }}
  </script>
</body>
</html>
"""

components.html(html_template, height=780, scrolling=False)
