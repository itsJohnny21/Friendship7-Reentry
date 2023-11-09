from vpython import *

###################################################
    # This program uses SI units only!!!! #
###################################################

# Scene setup
r_E = 6.378137e6 # Radius of Earth (Assuming that Earth is a perfect sphere)
min = 60 # 60 seconds in one minute
hour = 60*min  # 60 minutes in one hour
day = 24*hour # 24 hours in one day
year = 365*day # 365 days in one year
e = 2.718281828459045

scene = canvas(title="Friendship 7 Orbit Simulation", width=900, height=600, origin=vector(0,0,0), center=vector(0,0,0), background=vector(0.2,0.2,0.2)) # Creates a canvas called scene.
scene.camera.rotate(axis=scene.up, angle=pi/2) # Changes the orientation of the camera to match a traditional cartesian coordinate system
scene.camera.rotate(axis=scene.forward, angle=-pi/2) # Changes the orientation of the camera to match a traditional cartesian coordinate system
scene.camera.autoscale = False # Camera will not autsocale when new objects are introduced.
scene.camera.follow(None) # Camera will not follow any objects
scene.range = 7*r_E # The range that the camera will span
scene.camera.pos = vector(scene.range/tan(scene.fov/2),0,0) # Positions the camera so that it has a certain range
scene.camera.axis = -scene.camera.pos + scene.origin # Makes the camera's axis point to the origin

# Functions
# Convert seconds to a calendar time format. Example: passing in 600 returns "10 min"
def calendarTimeFormat(time):
    
    years = int(time//year)
    time -= year*years
    
    days = int(time//day)
    time -= day*days
    
    hours = int(time//hour)
    time -= hour*hours
    
    minutes = int(time//min)
    time -= minutes*min
    
    seconds = time
    time -= seconds*1
    
    calendar_time = ''
    l = [[years, 'y '], [days,'d '], [hours, 'hr '],[minutes, 'min '], [round(seconds,3), 's ']]
    
    for each in l:
        if each[0] != 0:
            calendar_time += (str(each[0]) + each[1])

    return calendar_time

# Rotate a list of objects
def rotateObjects(objects_list, orig, axi, ang):
    for object in objects_list:
        object.rotate(origin=orig, axis=axi, angle=ang)
        
        if hasattr(object, 'label'):
            object.label.pos = object.pos
        
# Show the labels that belong to the objects in a list      
def showObjectsLabel(objects_list):
    for object in objects_list:
        if hasattr(object, 'label'):
            object.label.visible = True
        
# Hide the labels that belong to the objects in a list   
def hideObjectsLabel(objects_list):
    for object in objects_list:
        if hasattr(object, 'label'):
            object.label.visible = False

# Convert from geographic to cartesian
def geographicToCartesian(geographic_vec):

    rho = geographic_vec.x
    phi = geographic_vec.y
    theta = geographic_vec.z

    x = rho*sin(pi/2-phi)*cos(theta)
    y = rho*sin(pi/2-phi)*sin(theta)
    z = rho*cos(pi/2-phi)

    cartesian_vec = vector(x,y,z)
    return cartesian_vec

# Convert from geographic to cartesian using a transform
def geographicToCartesianTransform(geographic_vec, newX, newY, newZ):

    rho = geographic_vec.x
    phi = geographic_vec.y
    theta = geographic_vec.z

    x = rho*sin(pi/2-phi)*cos(theta)
    y = rho*sin(pi/2-phi)*sin(theta)
    z = rho*cos(pi/2-phi)

    cartesian_vec = x*newX.hat+ y*newY.hat + z*newZ.hat
    return cartesian_vec

# Convert from spehrical to cartesian
def sphericalToCartesian(spherical_vec):
    
    rho = spherical_vec.x
    phi = spherical_vec.y
    theta = spherical_vec.z

    x = rho*sin(phi)*cos(theta)
    y = rho*sin(phi)*sin(theta)
    z = rho*cos(phi)

    cartesian_vec = vector(x,y,z)
    return cartesian_vec

# Convert from cartesian to geographic
def cartesianToGeographic(cartesian_vec):
    
    x = cartesian_vec.x
    y = cartesian_vec.y
    z = cartesian_vec.z
    
    rho = sqrt(x**2+y**2+z**2)
    phi = pi/2-acos(z/rho)
    
    if x>0:
        theta = atan(y/x)
    elif y>0:
        theta = atan(y/x)+pi
    else:
        theta = atan(y/x)-pi
    
    geographical_vec = vector(rho, phi, theta)
    
    return geographical_vec

# Return the smaller value of the two
def maximum(a, b):
    return a if a > b else b

# Return the greater value of the two
def minimum(a, b):
    return a if a < b else b

# Earth attributes (Source: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html)
G = 6.674e-11 # Gravitational constant
r_E = 6.378137e6 # Radius of Earth (Assuming that Earth is a perfect sphere)
m_E = 5.9722e24 # Mass of Earth
T_E = 23.9345*60*60 # Period for Earth's rotation about its axis
day_E = 24*60*60 # Length of time for one full day. This takes into account Earth's orbit around the sun
escape_v_E = (2*G*m_E/r_E)**0.5 # Calculated escape velocity of Earth
omega_E = 2*pi/T_E # Calculated angular velocity of Earth
fomega_E = 2*pi/day_E # False angular velocity of Earth. It assumes that one full rotation of Earth equals 24 hours (really it's 23.9345 hours)
equator_v_E = r_E*omega_E # Calculated tangential velocity at Earth's equator
capsule_h0 = 260714 # Altitude at reentry

# Geographical coordinates for points of interest
geo_KSC = vector(r_E, radians(28.5729), radians(-80.6490)) # https://www.latlong.net/place/kennedy-space-center-fl-usa-31881.html
geo_EMCC = vector(r_E, radians(33.48087), radians(-112.34356)) # Apple maps
geo_ActualSD = vector(r_E, radians(21.333), radians(-68.667)) # https://en.wikipedia.org/wiki/Mercury-Atlas_6
geo_intended_pass = vector(r_E+capsule_h0, radians(34), radians(241)) # Target coordinates for reentry
geo_intended_pass2e = vector(r_E, radians(34), radians(310)) # Target coordinates for reentry with Earth's rotation taken into account

# Cartesian coordinates for points of interest
cart_KSC = geographicToCartesian(geo_KSC)
cart_EMCC = geographicToCartesian(geo_EMCC)
cart_ActualSD = geographicToCartesian(geo_ActualSD)
cart_intended_pass = geographicToCartesian(geo_intended_pass)
cart_intended_pass2e = geographicToCartesian(geo_intended_pass2e)

# Earth object
earth = sphere(pos=vector(0,0,0), radius=r_E, mass=m_E, texture=textures.earth, visible=True)
earth.rotate(axis=vector(0,0,1), angle=pi/2)
earth.rotate(axis=vector(0,1,0), angle=pi/2) 
earth.omega = vector(0,0,omega_E) # Angular velocity of earth (accurate)
earth.fomega = vector(0,0,fomega_E)# Angular velocity of earth (approximation)

# List of points of Earth's surface
list_points = [] # List for containing points of interest
point_size = r_E/500 # Size of a point of interest object (visual purposes only)

point_IP = sphere(pos=cart_intended_pass, radius=point_size, color=color.yellow, visible=False)
point_IP.label = label(pos=point_IP.pos, text='Re-entry point', height=10, visible=False, box=False, color=color.white,
                        xoffset=10, yoffset=10, opacity=0)
list_points.append(point_IP)

point_KSC = sphere(pos=cart_KSC, radius=point_size, color=color.red)
point_KSC.label = label(pos=point_KSC.pos, text='Kennedy Space Center', height=10, visible=True, box=False, color=color.white,
                        xoffset=10, yoffset=10, opacity=0)
list_points.append(point_KSC)

point_ActualSD = sphere(pos=cart_ActualSD, radius=point_size, color=color.blue)
point_ActualSD.label = label(pos=point_ActualSD.pos, text='Actual Splashdown', height=10, visible=True, box=False, color=color.white,
                        xoffset=0, yoffset=0, opacity=0)
list_points.append(point_ActualSD)

# Important Variables
IA=34.043 # Inclination Angle
LOAN = 225.971 # Longitude of the ascending node
IA_vector = geographicToCartesian(vector(1,radians(IA),0)).hat # Inclination angle vector
LOAN_vector = geographicToCartesian(vector(1,0,radians(LOAN))).hat # Longitude of the ascending node vector
AA = 70.470 # Azimuth Angle
newX_orbit = geographicToCartesian(vector(1, 0, radians(LOAN))).hat # New x-axis created using transforms
newZ_orbit = geographicToCartesian(vector(1, radians(IA+90), radians(LOAN+90))).hat # New z-axis created using transforms
newY_orbit = cross(newX_orbit, newZ_orbit).hat # New y-axis created using transforms
tf = 281.398*min # Time duration for the capsule's reentry phase
plane_thickness = r_E/1000 # Thickness of a plane created (visual purposes)
p_orbit = 6727551.316971349 # Semilatus rectum in meters
a_orbit = 6730525.193736 # Semimajor axis in meters
b_orbit = 6728903.946156 # Semiminor axis in meters
arrow_size_scale = 12 # Scales the size of arrows used for visual purposes
arrow_shaftwidth = r_E/1000 # Shaftwidth size for arrows used for visual purposes
arrow_headwidth = 2*arrow_shaftwidth # Headwidth size for arrows used for visual purposes
arrow_headlength = arrow_headwidth # Headlength size for arrows used for visual purposes
dp_altitude = 8534 # Altitude for when the drogue parachute was released
dp_A  = 50 # Surface area of a small sized parachute
dp_CD = 1.5 # Coefficient of drag from a parachute
mp_altitude = 3292 # Altitude for when the main parachute was released
mp_A = 200 # Surface area of a big sized parachute
mp_CD = 1.5 # Coefficient of drag from a parachute
retrofire_t = 0.4*min # Duration of retrofire
retrofire_thrust = 20.1e3 # Thrust from three retrofire rockets used on the Mercury mission

##### AXIS ARROWS AS OBJECTS FOR VISUALIZATION #####
x_arrow = arrow(pos=scene.origin, shaftwidth=r_E/100, axis=vector(r_E*1.5,0,0), color=color.red, round=True)
x_arrow.label = label(pos=x_arrow.pos+x_arrow.axis.hat*x_arrow.length, text="x", height=10, visible=True, box=False, color=x_arrow.color,
                      xoffset = 0, yoffset=5, opacity=0)
y_arrow = arrow(pos=scene.origin, shaftwidth=r_E/100, axis=vector(0,r_E*1.5,0), color=color.white, round=True)
y_arrow.label = label(pos=y_arrow.pos+y_arrow.axis.hat*y_arrow.length, text="y", height=10, visible=True, box=False, color=y_arrow.color,
                      xoffset = 0, yoffset=5, opacity=0)
z_arrow = arrow(pos=scene.origin, shaftwidth=r_E/100, axis=vector(0,0,r_E*1.5), color=color.yellow, round=True)
z_arrow.label = label(pos=z_arrow.pos+z_arrow.axis.hat*z_arrow.length, text="z", height=10, visible=True, box=False, color=z_arrow.color,
                      xoffset = 0, yoffset=5, opacity=0)
                      
# Capsule Object
capsule_M = 1207.82576 # Mercury capsule mass
capsule_A = 9.226296 # Mercury capsule reference area (used for drag force) 
capsule_CD = 0.45 #  Mercury capsule drag coefficient
capsule_h0 = 260714 # Initial altitude at reentry
capsule_r0_geo = vector(r_E+capsule_h0, geo_intended_pass.y, geo_intended_pass.z) # Coordinates for initial position (geographical)
capsule_r0 = geographicToCartesian(capsule_r0_geo) # Coordinates for initial position (cartesian)

capsule = sphere(pos=capsule_r0, m=capsule_M, A=capsule_A, CD=capsule_CD, color=vector(1,0,0.9), make_trail=False) # Friendship 7 Object

list_of_objects = [earth, point_ActualSD, point_IP, point_KSC, capsule] # List of objects for animation
list_of_points = [point_ActualSD, point_KSC] # List of points of interest for animation
rotateObjects(list_of_objects, scene.origin, earth.fomega, tf*fomega_E) # Rotates objects to skip to re-entry part
showObjectsLabel(list_of_objects) # Shows labels if objects have any
        
capsule.v = sqrt(G*m_E/(r_E+capsule_h0))*cross(newZ_orbit, capsule.pos).hat # Initial velocity
capsule.gforce = -G*m_E*capsule.m*capsule.pos/(capsule.pos.mag)**3 # Gravity force
capsule.p = minimum(1, pow(e, -(capsule.pos.mag-r_E)/(capsule_h0/100))) # Air density (initially 0 due to capsule being in space)
capsule.dforce = capsule.p*capsule.A*capsule.v.mag**2*capsule.CD/2*-capsule.v.hat # Initial drag force
capsule.tforce = -capsule.axis.hat*0 # Initial thrust force
capsule.netforce = capsule.gforce+capsule.dforce+capsule.tforce # Initial netforce
capsule.a = capsule.netforce/capsule.m # Initial acceleration
capsule.axis.hat = capsule.v # Orients the capsule so that it's axis is in the same direction as its velocity vector
capsule.radius = r_E/1000 # Radius of the capsule

# Planes
orbital_plane_shape = shapes.ellipse(width=a_orbit*2, height=b_orbit*2) # Orbital plane shape used to create an orbital plane object
orbital_plane = extrusion(path=[vector(0,0,-plane_thickness/2), vector(0,0,plane_thickness)], shape=orbital_plane_shape, color=color.cyan, opacity=0.5, visible=False) # Orbital plane object
orbital_plane.rotate(axis=vector(0,0,1), angle=radians(LOAN)) # Orient the orbital plane properly
orbital_plane.rotate(axis=LOAN_vector, angle=radians(IA)) # Orient the orbital plane properly

# Capsule arrows (visual arrows for velocity, gravity, drag, thrust, and netforce)
capsule.v_arrow = arrow(pos=capsule.pos, axis=capsule.v*arrow_size_scale, shaftwidth=arrow_shaftwidth, headwidth=arrow_headwidth,
                    headlength=arrow_headlength, color=color.blue)
capsule.v_arrow.label = label(pos=capsule.v_arrow.pos+capsule.v_arrow.axis, text='Velocity', height=15, border=False, box=False, opacity=0, visible=True)

                    
capsule.gforce_arrow = arrow(pos=capsule.pos, axis=capsule.gforce*arrow_size_scale, shaftwidth=arrow_shaftwidth, headwidth=arrow_headwidth,
                    headlength=arrow_headlength, color=color.red)
capsule.gforce_arrow.label = label(pos=capsule.gforce_arrow.pos+capsule.gforce_arrow.axis, text='Fg', height=15, border=False, box=False, opacity=0, visible=True,
                                  xoffset=-10, yoffset=-10)
           
    
capsule.dforce_arrow = arrow(pos=capsule.pos, axis=capsule.dforce*arrow_size_scale, shaftwidth=arrow_shaftwidth, headwidth=arrow_headwidth,
                    headlength=arrow_headlength, color=color.orange)
capsule.dforce_arrow.label = label(pos=capsule.dforce_arrow.pos+capsule.dforce_arrow.axis, text='Fd', height=15, border=False, box=False, opacity=0, visible=True)
        
    
capsule.tforce_arrow = arrow(pos=capsule.pos, axis=capsule.tforce*arrow_size_scale, shaftwidth=arrow_shaftwidth, headwidth=arrow_headwidth,
                    headlength=arrow_headlength, color=color.green)
capsule.tforce_arrow.label = label(pos=capsule.tforce_arrow.pos+capsule.tforce_arrow.axis, text='Ft', height=15, border=False, box=False, opacity=0, visible=True)


capsule.netforce_arrow = arrow(pos=capsule.pos, axis=capsule.netforce*arrow_size_scale, shaftwidth=arrow_shaftwidth, headwidth=arrow_headwidth,
                    headlength=arrow_headlength, color=color.black)
capsule.netforce_arrow.label = label(pos=capsule.netforce_arrow.pos+capsule.netforce_arrow.axis, text='Netforce', height=15, border=False, box=False, opacity=0, visible=True,
                                    xoffset=10, yoffset=-10)

# Animation Settings
program_speed = 30/1 # Ratio: program time / real time. Example: 3600 means 3600 seconds in the program equals 1 second in real time. (1hr/s)
fps = 100 # Frame rate of the program (frames per second). The higher the value, the more accurate the program is at simulating real physics (smaller dt).
dt = program_speed/fps # Calculated dt so that the program speed works properly
t0 = 0 # Initial time
t = t0 # Time variable

dp_toggle = False # Toggle to deploy the capsule's drogue parachute
mp_toggle = False # Toggle to deploy the capsule's main parachute
retrofire_end_toggle = False # Toggle to end the capsule's retrofire phase

scene.camera.follow(capsule) # Camera will follow the capsule
scene.waitfor('click') # Event listener that will start the animation when the mouse button is clicked
capsule.make_trail = True # Creates a trail for the capsule's trajectory
print("START")
while t<tf*2: # While the time variable t is less than 
    rate(fps)
    
    # Retrofire phase
    if t<retrofire_t:
        capsule.tforce = retrofire_thrust*-capsule.v.hat
    else:
        capsule.tforce = vector(0,0,0)
        if retrofire_end_toggle == False:
            print(f't = {t}: Retrofire is over')
            retrofire_end_toggle = True
        
    # Rotation for Earth and points of interest 
    earth.rotate(axis=earth.fomega.hat, angle=earth.fomega.mag*dt)
    rotateObjects(list_of_points, earth.pos, earth.fomega, earth.fomega.mag*dt)

    # Capsule updates
    capsule.pos += capsule.v*dt
    capsule.p = minimum(1, pow(e, -(capsule.pos.mag-r_E)/(capsule_h0/100)))
    capsule.gforce = -G*m_E*capsule_M*capsule.pos/(capsule.pos.mag)**3
    capsule.dforce = capsule.p*capsule.A*capsule.v.mag**2*capsule.CD/2*-capsule.v.hat
    capsule.netforce = capsule.gforce+capsule.dforce+capsule.tforce
    capsule.a = capsule.netforce/capsule.m
    capsule.v += capsule.a*dt
    
    # Arrows updates
    capsule.v_arrow.pos = capsule.pos
    capsule.v_arrow.axis = capsule.v*arrow_size_scale
    capsule.v_arrow.label.pos = capsule.v_arrow.pos+capsule.v_arrow.axis
    
    capsule.gforce_arrow.pos = capsule.pos
    capsule.gforce_arrow.axis = capsule.gforce*arrow_size_scale
    capsule.gforce_arrow.label.pos = capsule.gforce_arrow.pos+capsule.gforce_arrow.axis
    
    capsule.dforce_arrow.pos = capsule.pos
    capsule.dforce_arrow.axis = capsule.dforce*arrow_size_scale
    capsule.dforce_arrow.label.pos = capsule.dforce_arrow.pos+capsule.dforce_arrow.axis
    
    capsule.tforce_arrow.pos = capsule.pos
    capsule.tforce_arrow.axis = capsule.tforce*arrow_size_scale
    capsule.tforce_arrow.label.pos = capsule.tforce_arrow.pos+capsule.tforce_arrow.axis
    
    capsule.netforce_arrow.pos = capsule.pos
    capsule.netforce_arrow.axis = capsule.netforce*arrow_size_scale
    capsule.netforce_arrow.label.pos = capsule.netforce_arrow.pos+capsule.netforce_arrow.axis
    
    # Drogue parachute deployment
    if capsule.pos.mag-r_E < dp_altitude: # Deploy dorgue parachute if it is less than the threshold altitude
        capsule.A = dp_A
        capsule.CD = dp_CD
        if dp_toggle == False:
            print(f't = {t}: Drogue parachute deployed')
            dp_toggle = True
            
    # Main parachute deployment
    if capsule.pos.mag-r_E < mp_altitude: # Deploy main parachute if it is less than the threshold altitude
        capsule.A = mp_A
        capsule.CD = mp_CD
        if mp_toggle == False:
            print(f't = {t}: Main parachute deployed')
            mp_toggle = True
    
    # Splashdown
    if capsule.pos.mag < r_E: # Collision detection between the capsule and Earth's surface
        splashdown_label = label(pos=capsule.pos, text='Simulated Splashdown', height=15, border=False, box=False, opacity=0, visible=True,
                            xoffset=20, yoffset=20)
        print(f't = {t}: SPLASHDOWN')
        break

    t = t+dt
    
print("FINISH")
exit()



