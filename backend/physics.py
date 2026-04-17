import numpy as np

class DynamicsEngine:
    def __init__(self, m, k, c):
        self.m = m  # Mass (kg)
        self.k = k  # Stiffness (N/m)
        self.c = c  # Damping (Ns/m)

    def ode_system(self, state, t, f_ext, omega_ext):
        """Defines the state-space representation of the system."""
        x, v = state
        # Force = F0 * sin(omega * t)
        dxdt = v
        dvdt = (f_ext * np.sin(omega_ext * t) - self.c * v - self.k * x) / self.m
        return np.array([dxdt, dvdt])

    def solve_rk4(self, f_ext, freq_hz, duration=3, fps=60):
        """Solves the motion using 4th-order Runge-Kutta."""
        dt = 1.0 / fps
        t_steps = np.arange(0, duration, dt)
        omega_ext = 2 * np.pi * freq_hz
        
        state = np.array([0.0, 0.0])  # Initial [displacement, velocity]
        results = []

        for t in t_steps:
            k1 = self.ode_system(state, t, f_ext, omega_ext)
            k2 = self.ode_system(state + 0.5 * dt * k1, t + 0.5 * dt, f_ext, omega_ext)
            k3 = self.ode_system(state + 0.5 * dt * k2, t + 0.5 * dt, f_ext, omega_ext)
            k4 = self.ode_system(state + dt * k3, t + dt, f_ext, omega_ext)
            
            state += (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
            results.append(state[0]) # Store displacement
            
        return t_steps.tolist(), results
