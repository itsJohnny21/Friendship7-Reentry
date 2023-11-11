from vpython import *
import plotly.graph_objects as go

φ1 = 28.50                 # launch latitude

def inclination(azimuth, latitude):
    return degrees(acos(sin(radians(azimuth))*cos(radians(latitude))))

ΨVals = arange(0,360,0.1) # azimuth values
iVals = [inclination(Ψ, φ1) for Ψ in ΨVals] # inclination angle values

fig = go.Figure()
fig.add_trace(go.Scatter(x=ΨVals, y=iVals))
fig.add_trace(go.Scatter(x=φ1, y=iVals))
fig.show()