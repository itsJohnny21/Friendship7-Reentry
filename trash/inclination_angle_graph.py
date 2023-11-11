import plotly.express as px
import pandas as pd
import vpython as vp

def get_inclination_angle(azimuth, latitude):
    return vp.acos(vp.sin(azimuth) * vp.cos(latitude))

################################################################################################################################################
launch_latitude = 0.49741883681838395
x_values = vp.arange(start=0, stop=2 * vp.pi, step=0.1)
y_values = [get_inclination_angle(azimuth=x, latitude=launch_latitude) for x in x_values]

df = pd.DataFrame({
   'x': x_values,
   'f(x)': y_values,
})

fig = px.line(data_frame=df, x=df['x'], y=df['f(x)'])
fig.show()
    