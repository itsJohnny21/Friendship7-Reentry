import plotly.express as px
import pandas as pd
from vpython import *
import sympy as sp

# # CONSTANTS
# v1 = 25761.345             # satellite velocity at burnout (ft/secc)
# r1 = 21637933              # distance of satellite from center of earth at burnout (ft)
# γ1 = 0.5                   # elevation angle (degrees)
# vc = 25506.28              # velocity for circulat orbit (ft/sec)
# p_over_r1 = 1.020022269      
# a = 22081775.58            # semimajor axis of orbit (ft)
# θ1 = 23.969                # angle between perigee and burnout (deg)
# e = 0.0219118              # eccentricity
# P = 91.585                 # Period (min)
# t_θ1 = 5.842               # time from perigee to burnout (min)

g0 = 115991.595            # gravitational constant at earth surface (ft/min^2)
R = 2.090226*10**7         # radius of earth
φ1 = 28.50                 # launch latitude
λ1 = 279.45                # launch longitude
# φ2 = 34.00                 # intended pass over latitude
# λ2 = 241.00                # intended pass over longitude
n = 3                      # number of orbits
# ωCapitale = 0.25068        # angular velocity of earth in (degrees/min)


# Equations
a,θ,r,p,r1,γ1,v1,vc,θ1,T,t,E,i,Ψ1 = sp.symbols('a θ r p r1 γ1 v1 vc θ1 T t E i')

eq_9 = sp.Eq(E, 2 * atan(sqrt((1-e) / (1+e)) * tan(θ/2)))
eq_1a = sp.Eq(r, p/(1+e * cos(θ)))
eq_1b = sp.Eq(r, a*(1-e**2) / (1+e*cos(θ)))
eq_1c = sp.Eq(r, a*(1 - eq_9.rhs))
eq_2 = sp.Eq(p/r1, (v1/vc)**2 * cos(γ1)**2)
eq_3 = sp.Eq(v**2, g0*R**2 * ((2/eq_1a.rhs) - (1/a)))
eq_4 = sp.Eq(vc**2, g0*R**2/r1)
eq_5 = sp.Eq(tan(θ1), tan(γ1)*((p/r1)/((p/r1)-1)))
eq_6 = sp.Eq(e, (1/cos(θ1)*((p/r1)-1)))
eq_7 = sp.Eq(T, 2*pi*sqrt(R/g0)*(a/R)**(1/3))
eq_8 = sp.Eq(t, T/(2*pi)*(eq_9.rhs - e*sin(eq_9.rhs)))
eq_10_a = sp.Eq(cos(i, cos(φ1)*sin(Ψ1)))
eq_10_b = sp.Eq(cos(i, -cos(φ1)*sin(Ψ1)))



# Johnson's values from the formulas
def E(θ):
    return 2 * atan(sqrt((1-e) / (1+e)) * tan(θ/2))

r = a * (1 - e * cos(E))                                        # distance of satellite from earth center
satellite_velocity = sqrt(g0 * R**2 * (2/r - 1/a))

p = r1*(v1/vc)**2*cos(radians(γ1))                              # semilatus rectum of the orbit ellipse
θ1 = degrees(atan((tan(radians(γ1))*((p/r1)/((p/r1)-1)))))      # angle in orbit plane betwen perigee and burnout
e = (1/(cos((θ1))))*(p/r1-1)                                    # orbit eccentricity
T = 2*pi*sqrt(R/gO)*sqrt((a/R)**3)                              # orbit period
λ2e = λ2+n*ωCapitale*T                                          # equivalent longitude to λ2 but with earth's rotation taken into consideration

def Anomaly(θ): # TAKES IN RADIANS AS AN INPUT                              #eccentric anomaly 
    return 2*atan(tan(θ/2)*sqrt((1-e)/(1+e))) # RETURNS IN RADIANS

def t(θ): # time from pergee
    return T/(2*pi)*(Anomaly(θ)-e*sin(Anomaly(θ)))