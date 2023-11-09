from vpython import *

#SATELLITE LAUNCHED EASTWARD

#-------------------
#constants and initial processing (defined variables)
r_E = 6.378137e6 # Radius of Earth (Assuming that Earth is a perfect sphere) # Delete later

v1 = 25761.345*60          #satellite velocity in ft/min
r1 = 21637933              #circular orbit radius in feet
γ1 = 0.5                   #elevation angle between local horizon and velocity vector in degrees
vc = 25506.28*60           #circular orbit velocity in ft/min
poverr1 = 1.020022269      #p (semilatus rectum of the orbit ellipse) over r1
a = 22081775.57            #semimajor axis of orbit in feet
tθ1 = 5.842                #t[θ1] is the time from perigee for 01 in min, where 01 is angle in orbit plane between perigee and burnout
gO = 115991.595            #acceleration due to gravity ft/min^2
R = 2.090226*10**7          #earth radius in feet

                           #launch coordinates
φ1 = 28.50                 #launch latitude
λ1 = 279.45                #launch longitude
φ2 = 34.00                 #intended pass over latitude
λ2 = 241.00                #intended pass over longitude
n = 3                      #number of orbits
ωCapitale = 0.25068        #angular velocity of earth in degrees/min


#--------------------       #Johnson's values from the formulas
p = r1*(v1/vc)**2*cos(radians(γ1))    #Semilatus rectum of the orbit ellipse

θ1 = degrees(atan((tan(radians(γ1))*((p/r1)/((p/r1)-1)))))

e = (1/(cos((θ1))))*(p/r1-1)             #orbit eccentricity - should equal to 0.0219

T = 2*pi*sqrt(R/gO)*sqrt((a/R)**3)             #orbit period - should equal to 91.585

λ2e = λ2+n*ωCapitale*T  #equal to 309.689 degrees east

def Anomaly(θ): # TAKES IN RADIANS AS AN INPUT                              #eccentric anomaly 
    return 2*atan(tan(θ/2)*sqrt((1-e)/(1+e))) # RETURNS IN RADIANS

def t(θ): # TAKES IN RADIANS AS AN INPUT                                     #time from perigee for angle θ
    return T/(2*pi)*(Anomaly(θ)-e*sin(Anomaly(θ)))

marginError = 0.01 # Allowable room for error for approximating Δλminus2e and θ2e
minValue = 0 # Minimum value for iterative procedure
maxValue = 60 # Maximum value for iterative procedure
dx = 0.01 # Delta t for iterative procedure
bestGuess = [] # List to to contain approximations for Δλminus2e and θ2e
Δλminus2eValues = [] # List to contains for Δλminus2e values throughout the iterative procedure
θ2eValues = [] # List to contains for θ2e values throughout the iterative procedure
   
# Iterative procedure to approximate Δλminus2e and θ2e
for x in arange(minValue,maxValue,dx):
    
    # Solve for the intersection
    try:
        y1 = degrees(acos((cos(radians(x)-radians(θ1))-sin(radians(φ2))*sin(radians(φ1)))/(cos(radians(φ2))*cos(radians(φ1)))))
    except:
        y1 = 0

    y2 = λ2e-λ1+ωCapitale*(t(radians(x))-t(radians(θ1)))
        
    θ2eValues.append([y1,x])
    Δλminus2eValues.append([y2,x])
    
    # Check if y2 and y1 are equal within the threshold 
    delta = y2-y1

    # If so, save that value as our best approximation
    if abs(delta) < marginError:
        marginError = abs(y2-y1)
        bestGuess = [(y2+y1)/2,x]
        
print(f'Best guess: Δλminus2e = {round(bestGuess[0],3)}°, θ2e = {round(bestGuess[1],3)}°')

Δλminus2e = bestGuess[0]
θ2e = bestGuess[1]
Ψ1 = degrees(asin(sin(radians(Δλminus2e))*cos(radians(φ2))/sin(radians(θ2e)-radians(θ1)))) # Arcsin makes this value +- # Ψ2 = 180 - Ψ1
i1 = degrees(acos(sin(radians(Ψ1))*cos(radians(φ1))))

# Graph to show the relationship between the inclination angle and the azimuth angle (cos(inclination angle) = cos(latitude) * sin(azimuth angle))
inclination_graph = graph(title="Inclination-Azimuth Relationship", xtitle='Azimuth Angle (°)', ytitle="Inclination Angle (°)", background=vector(0.2,0.2,0.2), foreground=color.black, fast=False)
f1 = gcurve(color=color.red)
for x in arange(0,360,0.1):
    y = degrees(acos(sin(radians(x))*cos(radians(φ1))))
    f1.plot(x,y)
    
azimuth_plot = gdots(data=[Ψ1, i1], color=color.yellow, radius=6)

print(f'This results in the Azimuth angle Ψ1 = {round(Ψ1,3)}° and the inclination angle i1 = {round(i1,3)}°')

# "Contour plot" to show the solution for Δλminus2e and θ2e
λminus2e_VS_θ2e=graph(title="Contour Plot", xtitle="λminus2e (°)", ytitle="θ2e (°)", background=vector(0.2,0.2,0.2), foreground=color.black, xmin=minValue, xmax=maxValue, ymin=minValue, ymax=maxValue, fast=False)
θ2e_curve=gcurve(data=θ2eValues, color=color.blue)
Δλminus2e_curve=gcurve(data=Δλminus2eValues, color=color.red)
bestGuess=gdots(data=bestGuess, color=color.yellow, radius=6)

