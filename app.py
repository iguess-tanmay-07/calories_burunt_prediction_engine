import streamlit as st
import pickle
import numpy as np

# Page standard alignment controls (Wider spacing layout)
st.set_page_config(page_title="Wellness Tracker", layout="centered")

# LOAD THE MACHINE LEARNING MODEL (.pkl file matches)
@st.cache_resource
def load_model():
    try:
        with open('calories_model.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        with open('model.pkl', 'rb') as f:
            return pickle.load(f)

try:
    model = load_model()
except Exception as e:
    st.error(f"Model File Error: {e}")
    model = None

# Custom styling to inject global changes to native inputs (Matching the mockup layout)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Clean standard frame wrappers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0e1117 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Central Baseline Container Box */
    .main-flat-card {
        background-color: #fcf8f2;
        border-radius: 24px;
        padding: 36px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        max-width: 660px;
        margin: 20px auto;
    }
    
    /* Circle Layout Metrics Viewport */
    .circle-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 24px;
    }
    .counter-circle {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        border: 4px solid #ebd9cb;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #fcf8f2;
        margin-bottom: 12px;
    }
    .metric-number {
        font-size: 2.5rem;
        font-weight: 600;
        color: #4a3629;
    }
    .metric-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #634737;
        margin-bottom: 2px;
    }
    .metric-sub {
        font-size: 0.9rem;
        color: #a48674;
    }
    
    /* Structural Metadata Text Blocks */
    .grid-header {
        font-size: 0.85rem;
        font-weight: 700;
        color: #c0967a;
        letter-spacing: 0.05em;
        margin-bottom: 16px;
        text-transform: uppercase;
    }
    
    /* Restyle native streamlit forms transparently */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }
    
    .stSelectbox label, .stNumberInput label {
        font-size: 0.8rem !important;
        color: #bfa18f !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        margin-bottom: 4px !important;
    }
    
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid #ebd9cb !important;
        border-radius: 12px !important;
    }
    
    input {
        color: #4a3629 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    
    .tip-container {
        background-color: #f2e7dd;
        border-radius: 12px;
        padding: 16px;
        font-size: 0.9rem;
        color: #7d5a44;
        margin-top: 24px;
        margin-bottom: 20px;
    }
    
    /* Native calculation button overwrite */
    div.stButton > button {
        background-color: #ca8a56 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 24px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        text-align: left !important;
        transition: background-color 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #b57747 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Tracks output memory state safely across button interactions
if 'computed_value' not in st.session_state:
    st.session_state.computed_value = 487

# START BUILDING CONTAINER INNER CONTENT
st.markdown('<div class="main-flat-card">', unsafe_allow_html=True)

# Render Circular Interactive Node Displays
st.markdown(f"""
<div class="circle-wrapper">
    <div class="counter-circle">
        <span class="metric-number">{st.session_state.computed_value}</span>
    </div>
    <div class="metric-title">kcal estimated</div>
    <div class="metric-sub">based on today's session</div>
</div>
<div class="grid-header">Your Details</div>
""", unsafe_allow_html=True)

# Streamlit native processing architecture grid blocks
with st.form(key='fitness_input_form'):
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        weight = st.number_input("Weight (kg)", min_value=1.0, value=72.0, step=1.0)
        duration = st.number_input("Duration (min)", min_value=1.0, value=45.0, step=1.0)
    with row1_col2:
        age = st.number_input("Age (yr)", min_value=1, max_value=120, value=25)
        height = st.number_input("Height (cm)", min_value=1.0, value=175.0, step=1.0)
        heart_rate = st.number_input("Heart rate (bpm)", min_value=1.0, value=138.0, step=1.0)
    
    # 7TH INTERACTIVE ACCURACY INPUT BLOCK RESTORED
    body_temp = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, value=37.0, step=0.1)

    st.markdown("""
    <div class="tip-container">
        <p><strong>Tip:</strong> A 30-min brisk walk burns around 180 kcal for your body weight.</p>
    </div>
    """, unsafe_allow_html=True)
    
    calculate_btn = st.form_submit_button(label="Calculate my burn")

# Execution block logic maps parameters inside backend variables instantly
if calculate_btn and model is not None:
    try:
        gender_code = 0 if gender == "Male" else 1
        
        # Exact DataFrame/Array column tracking format mapping: [Gender, Age, Height, Weight, Duration, Heart_Rate, Body_Temp]
        input_features = np.array([[gender_code, age, height, weight, duration, heart_rate, body_temp]])
        
        # Send details directly into the model to update states
        raw_output = model.predict(input_features)[0]
        st.session_state.computed_value = max(0, round(float(raw_output)))
        
        st.rerun()
    except Exception as calculation_error:
        st.error(f"Prediction matrix error: {calculation_error}")

st.markdown('</div>', unsafe_allow_html=True)
