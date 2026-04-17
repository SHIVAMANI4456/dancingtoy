import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dancing Dashboard Toy", layout="wide")

st.title("🚗 Dancing Dashboard Toy Simulation")

st.markdown("Simulating a vibration-driven toy using a spring-mass-damper system")

# Sidebar Inputs
st.sidebar.header("Input Parameters")

m = st.sidebar.slider("Mass (kg)", 0.1, 1.0, 0.3)
k = st.sidebar.slider("Spring Stiffness (N/m)", 10, 500, 100)
c = st.sidebar.slider("Damping Coefficient", 0.1, 10.0, 1.0)
F0 = st.sidebar.slider("Force Amplitude", 0.1, 10.0, 1.0)

# Natural Frequency
fn = (1/(2*np.pi)) * np.sqrt(k/m)

st.subheader("📊 Natural Frequency")
st.write(f"Natural Frequency: **{fn:.2f} Hz**")

# Frequency Response
freq = np.linspace(0.1, 30, 500)
omega = 2 * np.pi * freq

X = F0 / np.sqrt((k - m*omega**2)**2 + (c*omega)**2)

# Plot Frequency Response
st.subheader("📈 Frequency Response")

fig1, ax1 = plt.subplots()
ax1.plot(freq, X)
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Amplitude")
ax1.set_title("Amplitude vs Frequency")

st.pyplot(fig1)

# Time Response Simulation
st.subheader("⏱️ Time Response (Toy Motion)")

t = np.linspace(0, 5, 500)
omega_input = 2 * np.pi * st.sidebar.slider("Input Vibration Frequency (Hz)", 1, 30, 10)

x = (F0 / np.sqrt((k - m*omega_input**2)**2 + (c*omega_input)**2)) * np.sin(omega_input * t)

fig2, ax2 = plt.subplots()
ax2.plot(t, x)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Displacement")
ax2.set_title("Toy Oscillation Over Time")

st.pyplot(fig2)

# Insight Section
st.subheader("💡 Insights")

if abs(fn - omega_input/(2*np.pi)) < 2:
    st.success("Resonance! Maximum dancing effect 🎉")
else:
    st.warning("Not in resonance range. Try adjusting parameters.")

st.markdown("""
### 🎯 Goal:
Tune parameters so that natural frequency ≈ vibration frequency (10–20 Hz)
""")
