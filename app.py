import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Dancing Toy Dashboard", layout="wide")

# ---------- HEADER ----------
st.markdown(
    "<h1 style='text-align: center;'>🧸 Dancing Dashboard Toy Simulator</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Visualizing vibration-driven motion using a spring-mass-damper system</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------- SIDEBAR ----------
st.sidebar.header("🎛️ Control Panel")

m = st.sidebar.slider("Mass (kg)", 0.1, 1.0, 0.3)
k = st.sidebar.slider("Spring Stiffness (N/m)", 10, 500, 120)
c = st.sidebar.slider("Damping", 0.1, 10.0, 1.0)
F0 = st.sidebar.slider("Force Amplitude", 0.1, 10.0, 1.0)
input_freq = st.sidebar.slider("Input Frequency (Hz)", 1, 30, 12)

omega_input = 2 * np.pi * input_freq

# ---------- CALCULATIONS ----------
fn = (1/(2*np.pi)) * np.sqrt(k/m)

A = F0 / np.sqrt((k - m*omega_input**2)**2 + (c*omega_input)**2)

# ---------- METRICS ----------
col1, col2, col3 = st.columns(3)

col1.metric("Natural Frequency (Hz)", f"{fn:.2f}")
col2.metric("Input Frequency (Hz)", f"{input_freq}")
col3.metric("Amplitude", f"{A:.3f}")

st.divider()

# ---------- RESONANCE STATUS ----------
if abs(fn - input_freq) < 2:
    st.success("🔥 Resonance! Maximum dancing effect")
else:
    st.warning("⚠️ Not in resonance range")

# ---------- LAYOUT ----------
left, right = st.columns([1,1])

# ---------- GRAPH ----------
with left:
    st.subheader("📈 Frequency Response")

    freq = np.linspace(0.1, 30, 400)
    omega = 2 * np.pi * freq

    X = F0 / np.sqrt((k - m*omega**2)**2 + (c*omega)**2)

    fig1, ax1 = plt.subplots()
    ax1.plot(freq, X)
    ax1.axvline(fn, linestyle='--', label="Natural Frequency")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Amplitude")
    ax1.legend()

    st.pyplot(fig1)

# ---------- ANIMATION ----------
with right:
    st.subheader("🧸 Live Toy Animation")

    placeholder = st.empty()

    t_vals = np.linspace(0, 5, 160)

    for t in t_vals:
        x = A * np.sin(omega_input * t)

        fig, ax = plt.subplots(figsize=(4,6))

        # ----- BASE -----
        ax.add_patch(plt.Rectangle((-0.5, -1.8), 1, 0.3))

        # ----- SPRING (zig-zag) -----
        n_coils = 12
        y_vals = np.linspace(-1.5, x, n_coils * 2)
        x_vals = []

        for i in range(len(y_vals)):
            if i % 2 == 0:
                x_vals.append(-0.2)
            else:
                x_vals.append(0.2)

        ax.plot(x_vals, y_vals, linewidth=2)

        # ----- BODY -----
        body_y = x - 0.4
        ax.add_patch(plt.Rectangle((-0.2, body_y), 0.4, 0.5))

        # ----- HEAD -----
        head_y = x + 0.3
        head = plt.Circle((0, head_y), 0.25)
        ax.add_patch(head)

        # ----- FACE -----
        # Eyes
        ax.plot(-0.08, head_y + 0.05, 'o', markersize=4)
        ax.plot(0.08, head_y + 0.05, 'o', markersize=4)

        # Smile
        smile_x = np.linspace(-0.1, 0.1, 50)
        smile_y = head_y - 0.05 - 0.05 * (smile_x**2)*20
        ax.plot(smile_x, smile_y)

        # ----- SETTINGS -----
        ax.set_xlim(-1, 1)
        ax.set_ylim(-2, 2)
        ax.axis('off')

        ax.set_title("Dancing Toy (Spring-Mass System)")

        placeholder.pyplot(fig)
# ---------- EXPLANATION ----------
st.markdown("""
### 🧠 How it works
- The toy behaves like a **spring-mass-damper system**
- When input frequency ≈ natural frequency → **resonance**
- This produces large oscillations → **dancing effect**
""")
