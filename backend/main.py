from fastapi import FastAPI
from physics import DynamicsEngine
from pydantic import BaseModel

app = FastAPI(title="VibraSim API")

class SimRequest(BaseModel):
    m: float
    k: float
    zeta: float
    freq: float
    amp: float

@app.post("/simulate")
async def simulate(data: SimRequest):
    # Calculate critical damping for the engine
    c_crit = 2 * (data.m * data.k)**0.5
    actual_c = data.zeta * c_crit
    
    engine = DynamicsEngine(data.m, data.k, actual_c)
    t, y = engine.solve_rk4(f_ext=data.amp * data.k / 1000, freq_hz=data.freq)
    return {"time": t, "displacement": y}
