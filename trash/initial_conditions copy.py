from vpython import *
import csv
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# CONSTANTS
v1 = 25761.345*60          # satellite velocity in (ft/min)
r1 = 21637933              # circular orbit radius in (ft)
γ1 = 0.5                   # elevation angle between local horizon and velocity vector in degrees
vc = 25506.28*60           # circular orbit velocity in (ft/min)
p_over_r1 = 1.020022269    # p (semilatus rectum of the orbit ellipse) over r1
a = 22081775.57            # semimajor axis of orbit in (ft)
tθ1 = 5.842                # t[θ1] is the time from perigee for 01 in min, where 01 is angle in orbit plane between perigee and burnout
gO = 115991.595            # acceleration due to gravity (ft/min^2)
R = 2.090226*10**7         # earth radius in (ft)
φ1 = 28.50                 # launch latitude
λ1 = 279.45                # launch longitude
φ2 = 34.00                 # intended pass over latitude
λ2 = 241.00                # intended pass over longitude
n = 3                      # number of orbits
ωCapitale = 0.25068        # angular velocity of earth in (degrees/min)

# JOHNSON'S VALUES FROM THE FORMULAS
p = r1*(v1/vc)**2*cos(radians(γ1))                                  # semilatus rectum of the orbit ellipse
θ1 = degrees(atan((tan(radians(γ1))*((p/r1)/((p/r1)-1)))))          # angle in orbit plane between perigee and burnout point
e = (1/(cos((θ1))))*(p/r1-1)                                        # orbit eccentricity
T = 2*pi*sqrt(R/gO)*sqrt((a/R)**3)                                  # orbit period
λ2e = λ2+n*ωCapitale*T                                              # equivalent longitude to λ2 but with earth's rotation taken into consideration

def Anomaly(θ): # eccentric anomaly 
    return 2*atan(tan(θ/2)*sqrt((1-e)/(1+e)))

def t(θ): # time from perigee
    return T/(2*pi)*(Anomaly(θ)-e*sin(Anomaly(θ)))

###############################################################################################################################################################################
#------------------ APPROXIMATION FOR Δλminus2e USING CONTOUR PLOT ------------------#
bestApprox = [] # List to contain the best approximation
Δλminus2eVals = [] # List to contain λminus2e values from iterative procedure
θ2eVals = [] # List to contain θ2e values from iterative procedure
x_vals = []
bestDelta = float('inf')

for x in arange(0, 60.01, 0.01):   
    try:
        y1 = degrees(acos((cos(radians(x)-radians(θ1))-sin(radians(φ2))*sin(radians(φ1)))/(cos(radians(φ2))*cos(radians(φ1)))))
    except:
        y1=0

    y2 = λ2e-λ1+ωCapitale*(t(radians(x))-t(radians(θ1)))
        
    # θ2eVals.append([x, y1])
    # Δλminus2eVals.append([x, y2])
    θ2eVals.append(y1)
    Δλminus2eVals.append(y2)
    x_vals.append(x)

    if abs(y2-y1) < bestDelta:
        bestDelta = abs(y2-y1)
        bestApprox = [x, (y2+y1)/2]
        
Δλminus2e = bestApprox[0] # best approximation for Δλminus2e
θ2e = bestApprox[1] # best approximation for θ2e

# # Save contour plot data
# file_name = './graphs/theta2e_curve.csv'
# with open(file_name, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(θ2eVals)
    
# file_name = './graphs/lambda_minus_2e_curve.csv'
# with open(file_name, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(Δλminus2eVals)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x_vals, y=θ2eVals))
fig.add_trace(go.Scatter(x=x_vals, y=Δλminus2eVals))
fig.add_trace(go.Scatter(x=[Δλminus2e], y=[θ2e]))
fig.show()


###############################################################################################################################################################################
#------------------ NOW WE CAN COMPUTE Ψ1 and i1 USING Δλminus2e ------------------#
Ψ1 = degrees(asin(sin(radians(Δλminus2e))*cos(radians(φ2))/sin(radians(θ2e)-radians(θ1))))
i1 = degrees(acos(sin(radians(Ψ1))*cos(radians(φ1))))