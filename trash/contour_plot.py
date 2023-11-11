import plotly.express as px
import pandas as pd

Δλminus2e_curve = pd.read_csv('./graphs/lambda_minus_2e_curve.csv')
θ2e_curve = pd.read_csv('./graphs/theta2e_curve.csv')

fig = px.line(Δλminus2e_curve)

fig.show()