import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 1. THE PHYSICS ENGINE ---
class DynamicsEngine:
    @staticmethod
    def solve_rk4(m, k, zeta, freq_hz, amp_mm, duration=3, fps=60):
        dt = 1.0 / fps
        t_steps = np.arange(0, duration, dt)
        omega_ext = 2 * np.pi * freq_hz
        f_ext = (amp_mm * k / 1000) 
        c_crit = 2 * np.sqrt(k * m)
        c = zeta * c_crit
        
        state = np.array([0.0, 0.0]) 
        results = []

        def ode_system(s, t):
            x, v = s
            dxdt = v
            dvdt = (f_ext * np.sin(omega_ext * t) - c * v - k * x) / m
            return np.array([dxdt, dvdt])

        for t in t_steps:
            k1 = ode_system(state, t)
            k2 = ode_system(state + 0.5 * dt * k1, t + 0.5 * dt)
            k3 = ode_system(state + 0.5 * dt * k2, t + 0.5 * dt)
            k4 = ode_system(state + dt * k3, t + dt)
            state += (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
            results.append(state[0])
            
        return t_steps, np.array(results)

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="VibraToy Studio", layout="wide")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛠️ Mechanical Lab")
    char_map = {"Robot": "🤖", "Cat": "🐱", "Alien": "👽", "Panda": "🐼"}
    toy_char = st.selectbox("Select Character", options=list(char_map.keys()))
    
    st.divider()
    m = st.slider("Head Mass (kg)", 0.05, 1.0, 0.2)
    k = st.slider("Spring Stiffness (N/m)", 10, 1000, 250)
    zeta = st.slider("Damping Ratio (ζ)", 0.01, 0.5, 0.1)
    
    st.divider()
    f_in = st.slider("Input Frequency (Hz)", 1, 50, 12)
    amp_in = st.slider("Road Intensity (mm)", 1, 10, 5)

# --- 4. PHYSICS LOGIC ---
t, displacements = DynamicsEngine.solve_rk4(m, k, zeta, f_in, amp_in)
max_d = np.max(np.abs(displacements)) * 1000 

# --- 5. UI LAYOUT ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("Live Digital Twin")
    
    # Calculate visual timing
    anim_duration = 1 / (f_in/4) if f_in > 4 else 1 / f_in
    visual_amp = min(max_d * 2, 40) 
    
    # COMBINED CSS + SVG (Bypasses st.markdown entirely)
    full_component_html = f"""
    <div style="
        background: radial-gradient(circle, #1a1c24 0%, #000000 100%);
        border-radius: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 550px;
        border: 1px solid #3d444d;
        overflow: hidden;
    ">
        <svg width="300" height="500" viewBox="0 0 200 400">
            <rect x="10" y="360" width="180" height="30" rx="10" fill="#333" />
            <g id="toy-assembly">
                <path d="M100,360 Q120,320 100,280 Q80,240 100,200 Q120,160 100,120" 
                      fill="none" stroke="#888" stroke-width="6" />
                <circle cx="100" cy="110" r="50" fill="#FFD700" stroke="#B8860B" stroke-width="4" />
                <text x="100" y="130" font-size="65" text-anchor="middle">{char_map[toy_char]}</text>
            </g>
            <style>
                @keyframes sway {{
                    0% {{ transform: rotate(0deg) translateX(0px); }}
                    25% {{ transform: rotate({visual_amp/2}deg) translateX({visual_amp}px); }}
                    75% {{ transform: rotate(-{visual_amp/2}deg) translateX(-{visual_amp}px); }}
                    100%
