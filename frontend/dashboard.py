import streamlit as st
import requests
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="VibraToy Studio", layout="wide")

# Professional Dark-Theme CSS
st.markdown("""
    <style>
    .toy-box {
        background: radial-gradient(circle, #2c3e50 0%, #000000 100%);
        border-radius: 15px;
        border: 2px solid #34495e;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 600px;
    }
    </style>
    """, unsafe_content_with_html=True)

st.title("📟 VibraToy Studio | Virtual Prototype")

# --- SIDEBAR: DESIGN SPECS ---
with st.sidebar:
    st.header("Mechanical Config")
    char = st.selectbox("Toy Head", ["🤖 Robot", "🐱 Cat", "👽 Alien", "🐻 Bear"])
    m = st.slider("Mass (kg)", 0.05, 0.5, 0.2)
    k = st.slider("Stiffness (N/m)", 50, 500, 200)
    
    st.header("Drive Input")
    speed = st.slider("Road Frequency (Hz)", 1, 30, 10)

# --- BACKEND INTEGRATION ---
# Here we call your FastAPI backend to get the "Real" physics data
try:
    # Note: Ensure uvicorn is running backend/main.py on port 8000
    payload = {"m": m, "k": k, "zeta": 0.1, "freq": speed, "amp": 5.0}
    response = requests.post("http://localhost:8000/simulate", json=payload).json()
    # Use the max displacement from backend to drive the SVG animation amplitude
    physics_amp = max(response['displacement']) * 1500 # Scale for visual impact
except:
    # Fallback if backend isn't running
    physics_amp = (speed * 5) / (k / 100)

# --- SVG TOY RENDERING ---
# We use physics_amp to drive the CSS animation
duration = 1 / (speed/5) if speed > 0 else 1

toy_svg = f"""
<div class="toy-box">
    <svg width="300" height="500" viewBox="0 0 200 400">
        <defs>
            <linearGradient id="baseGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#555;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#111;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect x="10" y="360" width="180" height="30" rx="5" fill="url(#baseGrad)" />
        
        <g id="toy">
            <path d="M100,360 C130,330 70,300 100,270 C130,240 70,210 100,180" 
                  fill="none" stroke="#bdc3c7" stroke-width="5" />
            
            <circle cx="100" cy="140" r="45" fill="#f1c40f" stroke="#f39c12" stroke-width="3" />
            <text x="100" y="160" font-size="50" text-anchor="middle">{char.split()[-1]}</text>
        </g>

        <style>
            @keyframes dance {{
                0% {{ transform: translate(0px, 0px) rotate(0deg); }}
                25% {{ transform: translate({physics_amp}px, -2px) rotate({physics_amp/2}deg); }}
                50% {{ transform: translate(0px, 0px) rotate(0deg); }}
                75% {{ transform: translate(-{physics_amp}px, -2px) rotate(-{physics_amp/2}deg); }}
                100% {{ transform: translate(0px, 0px) rotate(0deg); }}
            }}
            #toy {{
                transform-origin: 100px 360px;
                animation: dance {duration}s infinite ease-in-out;
            }}
        </style>
    </svg>
</div>
"""

st.components.v1.html(toy_svg, height=620)

st.info(f"System Status: Natural Frequency ~{np.sqrt(k/m)/(2*np.pi):.2f} Hz. Click 'Run Simulation' to sync with Backend Engine.")
