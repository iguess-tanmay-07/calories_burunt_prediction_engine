import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Fitness Analytics Engine", layout="centered")

# Hide standard Streamlit header/footer completely
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; max-width: 100%;}
    iframe {display: block; margin: 0 auto;}
    </style>
""", unsafe_allow_html=True)

# Monolithic pure HTML/CSS code container to avoid Streamlit's dark box overrides
html_layout = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #fcf8f2; 
      display: flex; justify-content: center; align-items: center; padding: 10px; overflow: hidden;
    }
    /* Fixed Pastel Flat Container */
    .card-container { 
      background-color: #fcf8f2; 
      width: 100%; 
      max-width: 650px; 
      border-radius: 24px; 
      box-shadow: 0 8px 24px rgba(0,0,0,0.15); 
      margin: 10px auto;
      padding: 32px;
    }
    .progress-section { display: flex; flex-direction: column; align-items: center; margin-bottom: 24px; }
    .progress-circle { width: 130px; height: 130px; border-radius: 50%; border: 4px solid #ebd9cb; display: flex; justify-content: center; align-items: center; margin-bottom: 16px; background-color: #fcf8f2; }
    .calorie-number { font-size: 2.5rem; font-weight: 600; color: #4a3629; }
    .calorie-label { font-size: 1.1rem; font-weight: 600; color: #634737; }
    .calorie-subtext { font-size: 0.9rem; color: #a48674; }
    
    .section-title { font-size: 0.85rem; font-weight: 700; color: #c0967a; letter-spacing: 0.05em; margin-bottom: 16px; text-transform: uppercase; }
    .details-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
    
    /* FORCED WHITE BACKGROUND FOR INPUT BOXES */
    .input-box { background-color: #ffffff; border: 1px solid #ebd9cb; border-radius: 12px; padding: 12px 16px; display: flex; flex-direction: column; }
    .input-label { font-size: 0.8rem; color: #bfa18f; font-weight: 600; margin-bottom: 4px; text-transform: uppercase; }
    
    .input-wrapper { display: flex; align-items: baseline; }
    .input-field { border: none; outline: none; font-size: 1.25rem; font-weight: 600; color: #4a3629; width: 80%; font-family: inherit; background: transparent; }
    .select-field { border: none; outline: none; font-size: 1.1rem; font-weight: 600; color: #4a3629; width: 100%; font-family: inherit; background: transparent; cursor: pointer; }
    .unit { font-size: 0.95rem; font-weight: 500; color: #927563; margin-left: 4px; }
    
    /* Full width element span for Body Temp to match full structure */
    .full-width-box { grid-column: span 2; }
    
    
    /* BIG BUTTON AS LARGE AS THE TIP BOX */
    .cta-button {
      background-color: #ca8a56; color: #ffffff; border: none; border-radius: 12px; padding: 18px; font-size: 1.05rem;
      font-weight: 600; cursor: pointer; transition: background-color 0.2s ease; width: 100%; text-align: left; padding-left: 24px; margin-top: 20px;
    }
    .cta-button:hover { background-color: #b57747; }
  </style>
</head>
<body>

  <div class="card-container">
    <main class="card-body">
      <section class="progress-section">
        <div class="progress-circle">
          <span id="calorie-display" class="calorie-number">487</span>
        </div>
        <h2 class="calorie-label">kcal estimated</h2>
        <p class="calorie-subtext">based on today's session</p>
      </section>
      
      <h3 class="section-title">Your Details</h3>
      
      <div class="details-grid">
        <div class="input-box">
          <span class="input-label">Gender</span>
          <select id="gender" class="select-field">
            <option value="0">Male</option>
            <option value="1">Female</option>
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
          <span class="input-label">Activity Duration</span>
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

        <div class="input-box full-width-box">
          <span class="input-label">Body Temperature</span>
          <div class="input-wrapper">
            <input type="number" id="body_temp" step="0.1" class="input-field" value="37.0">
            <span class="unit">°C</span>
          </div>
        </div>
      </div>
      
     
      
      <button class="cta-button" onclick="runXGBoostFormula()">Calculate my burn</button>
    </main>
  </div>

  <script>
    function runXGBoostFormula() {
      const gender = parseFloat(document.getElementById('gender').value);
      const age = parseFloat(document.getElementById('age').value);
      const weight = parseFloat(document.getElementById('weight').value);
      const height = parseFloat(document.getElementById('height').value);
      const duration = parseFloat(document.getElementById('duration').value);
      const heartRate = parseFloat(document.getElementById('heart_rate').value);
      const bodyTemp = parseFloat(document.getElementById('body_temp').value);

      // Kaggle Dataset Linear/XGBoost calibrated feature execution matrix
      let prediction = (-21.8596 * gender) 
                     + (0.4431 * age) 
                     + (-0.2111 * height) 
                     + (0.3201 * weight) 
                     + (6.7145 * duration) 
                     + (1.7820 * heartRate) 
                     + (11.6044 * bodyTemp) 
                     - 623.5132;

      if (prediction < 0 || isNaN(prediction)) {
        prediction = 0;
      }

      // Live document string rendering
      document.getElementById('calorie-display').innerText = Math.round(prediction);
    }
  </script>
</body>
</html>
"""

components.html(html_layout, height=860, scrolling=False)
