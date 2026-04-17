import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dancing Toy Simulator", layout="wide")

st.title("🕺 Dancing Dashboard Toy: Vibration Simulator")
st.markdown("""
This dashboard simulates the motion of a non-electronic dashboard toy (bobblehead).
It models the toy as a **Spring-Mass-Damper system** excited by car vibrations.
Adjust the parameters on the left to see how the toy 'dances'!
""")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Design Parameters")
mass = st.sidebar.slider("Toy Mass (kg)", 0.05, 0.50, 0.15, step=0.01)
k_stiffness = st.sidebar.slider("Spring Stiffness (N/m)", 10, 500, 100, step=10)
damping_ratio = st.sidebar.slider("Damping Ratio (ζ)", 0.01, 0.50, 0.10, step=0.01)

st.sidebar.header("Vehicle Input")
car_freq = st.sidebar.slider("Road Vibration Frequency (Hz)", 1, 50, 15)

# --- PHYSICS CALCULATIONS ---
# Natural Frequency: ωn = sqrt(k/m)
wn = np.sqrt(k_stiffness / mass)
fn = wn / (2 * np.pi)

# Frequency Ratio: r = f / fn
freq_range = np.linspace(0.1, 60, 500)
r_range = freq_range / fn
r_input = car_freq / fn

# Magnification Factor (Amplitude Ratio): 
# MF = 1 / sqrt((1-r^2)^2 + (2*zeta*r)^2)
def get_magnification(r, zeta):
    return 1 / np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)

mf_curve = get_magnification(r_range, damping_ratio)
current_mf = get_magnification(r_input, damping_ratio)

# Define a base input amplitude (e.g., 5mm vibration from the car)
input_amplitude_mm = 5 
output_amplitude_mm = input_amplitude_mm * current_mf

# --- VISUALIZATION (Layout) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Frequency Response Analysis")
    fig = go.Figure()
    
    # Plot resonance curve
    fig.add_trace(go.Scatter(x=freq_range, y=mf_curve, name="System Response", line=dict(color='royalblue', width=3)))
    
    # Highlight current operating point
    fig.add_trace(go.Scatter(x=[car_freq], y=[current_mf], mode='markers+text', 
                             name='Current Operation', text=["Working Point"],
                             textposition="top right", marker=dict(color='red', size=12)))

    fig.update_layout(
        xaxis_title="Input Frequency (Hz)",
        yaxis_title="Amplitude Magnification (Output/Input)",
        hovermode="x unified",
        template="plotly_white",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Engineering Metrics")
    st.metric("Natural Frequency (fn)", f"{fn:.2f} Hz")
    st.metric("Current Gain", f"{current_mf:.2f}x")
    st.metric("Estimated Swing", f"±{output_amplitude_mm:.1f} mm")
    
    # Logic for user feedback
    st.markdown("---")
    if 0.9 < r_input < 1.1:
        st.error("⚠️ **RESONANCE DETECTED:** The frequencies match! The toy will shake violently!")
    elif current_mf > 2.0:
        st.success("✅ **GOOD DANCING:** Large, satisfying motion achieved.")
    elif current_mf > 1.2:
        st.info("ℹ️ **SLIGHT MOTION:** The toy is moving, but could dance more.")
    else:
        st.warning("💤 **STATIC:** Toy is barely moving. Lower stiffness (k) or increase mass (m).")

# --- 🕺 ANIMATION SECTION 🕺 ---
st.divider()
st.subheader("Live Dance Floor")

ani_col1, ani_col2 = st.columns([1, 2])

with ani_col1:
    st.markdown("""
    **How to watch:**
    1. Click the 'Start Dancing' button below.
    2. The animation loop simulates the toy's motion for about 5 seconds.
    3. Change parameters in the sidebar and click again to see the effect!
    """)
    start_ani = st.button("▶️ Start Dancing")

with ani_col2:
    # Create the placeholder for the plot
    plot_placeholder = st.empty()

    if start_ani:
        # Simulation parameters for animation
        fps = 30
        duration_sec = 5
        t_ani = np.linspace(0, duration_sec, fps * duration_sec)
        
        # Calculate displacement over time (steady-state response)
        # y = Amplitude * sin(wt)
        displacement = output_amplitude_mm * np.sin(2 * np.pi * car_freq * t_ani)

        # Pre-create the figure object (speeds up the loop)
        # We model the toy as a simple base (static) and a bobble head (moving dot)
        fig_ani = go.Figure()
        
        # Add the "Bobble Head"
        fig_ani.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text',
                                    marker=dict(size=40, color='Gold', line=dict(width=2, color='DarkSlateGrey')),
                                    text=["🤩"], textposition="middle center", textfont=dict(size=25),
                                    name="Toy Head"))
        
        # Add the "Dashboard Base"
        fig_ani.add_trace(go.Scatter(x=[-20, 20], y=[-10, -10], mode='lines', 
                                    line=dict(color='black', width=4), name="Dashboard"))

        # Configure the layout (static axes are CRITICAL for animation)
        # We set the Y-axis range to accommodate the maximum possible swing
        # (Assuming max magnification ~10x, input 5mm -> 50mm, so +/-60mm is safe)
        max_range = 60 
        fig_ani.update_layout(
            template="plotly_white",
            xaxis=dict(range=[-30, 30], showgrid=False, zeroline=False, visible=False),
            yaxis=dict(range=[-max_range, max_range], showgrid=False, zeroline=False, title="Displacement (mm)"),
            showlegend=False,
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        # The Animation Loop
        for y_val in displacement:
            # Efficiently update ONLY the y-data of the 'Toy Head' trace
            fig_ani.data[0].y = [y_val]
            
            # Draw the figure in the placeholder
            plot_placeholder.plotly_chart(fig_ani, use_container_width=True, key=f"ani_{time.time()}")
            
            # Control the frame rate
            time.sleep(1/fps)
            
        st.success("Animation Finished.")

    else:
        # Display a static "Ready" image before the button is clicked
        fig_ready = go.Figure()
        fig_ready.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text',
                                    marker=dict(size=40, color='lightgrey'),
                                    text=["😐"], textposition="middle center", textfont=dict(size=25)))
        fig_ready.add_trace(go.Scatter(x=[-20, 20], y=[-10, -10], mode='lines', line=dict(color='black', width=4)))
        fig_ready.update_layout(
            template="plotly_white",
            xaxis=dict(range=[-30, 30], visible=False),
            yaxis=dict(range=[-60, 60], title="Displacement (mm)"),
            showlegend=False, height=400
        )
        plot_placeholder.plotly_chart(fig_ready, use_container_width=True)
