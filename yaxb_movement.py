#This script generates a horizontal or vertical path from the map of possible
#positions.

from math import sqrt,pi,floor,fabs,sin,cos,atan,tan
import matplotlib.pyplot as plt

#inputs
STEPS_PER_REVOLUTION = 3 #steps per revolution
CABLE_PULLEY_RADIUS = 2 #radius of pulley (cm)
GONDOLA_MASS = 1.2 #gondola mass (kg)
RATED_MOTOR_TORQUE = 56 #motor holding torque rating (N*cm)
WORKSPACE_HEIGHT = 1.5 #workspace height (m)
WORKSPACE_WIDTH = 1.5 #stepper motor width (m)

#cable tension thresholds
MAX_CABLE_TENSION = RATED_MOTOR_TORQUE/CABLE_PULLEY_RADIUS #maximum cable tension threshold (N)
MIN_HORIZ_CABLE_TENSION = 3 #minimum horizontal cable tension threshold (N)

CABLE_LENGTH_CHANGE_PER_STEP = 2*(CABLE_PULLEY_RADIUS/100)*pi/STEPS_PER_REVOLUTION #smallest cable length change possible (m)
GONDOLA_WEIGHT = GONDOLA_MASS*9.81 #weight of gondola (N)

def main():
    
    #intialize variables
    R1 = CABLE_LENGTH_CHANGE_PER_STEP
    
    #define lists
    x1 = []
    y1 = []
    
    #generate coordinates from geometry equations 
    #R1 is left radius
    #R2 is right radius
    while R1 < sqrt(WORKSPACE_HEIGHT**2+WORKSPACE_WIDTH**2): #while R1 is less than diagonal of workspace
        R2 = floor(sqrt(R1**2+WORKSPACE_WIDTH**2)/CABLE_LENGTH_CHANGE_PER_STEP)*CABLE_LENGTH_CHANGE_PER_STEP #R2 is floor hypotenuse
        while R2> WORKSPACE_WIDTH - R1:
            xp1 = (WORKSPACE_WIDTH**2-R2**2+R1**2)/(2*WORKSPACE_WIDTH)
            yp1 = sqrt(fabs((4*WORKSPACE_WIDTH**2*R1**2 
                             -(WORKSPACE_WIDTH**2-R2**2+R1**2)**2)/(4*WORKSPACE_WIDTH**2)))
            if xp1 <= WORKSPACE_WIDTH and yp1 <= WORKSPACE_HEIGHT:
                x1.append(xp1)
                y1.append(yp1)
            R2 = R2 - CABLE_LENGTH_CHANGE_PER_STEP
        R1 = R1 + CABLE_LENGTH_CHANGE_PER_STEP
    
    #apply color to points according to tension
    for j in range(0,len(x1)):
        alphaT = atan(x1[j]/y1[j])
        betaT = atan((WORKSPACE_WIDTH-x1[j])/y1[j])
        T1 = GONDOLA_WEIGHT/(sin(alphaT)*tan(betaT)**-1+cos(alphaT)) #cable tension - N in cable that is connected to the origin
        T2 = T1*sin(alphaT)/sin(betaT)
        if (T1 > MAX_CABLE_TENSION or T2 > MAX_CABLE_TENSION):
            plt.plot(x1[j],y1[j],'ro')
        elif (0 < T1*sin(alphaT) < MIN_HORIZ_CABLE_TENSION or 
              0 < T2*sin(betaT) < MIN_HORIZ_CABLE_TENSION ):
            plt.plot(x1[j],y1[j],'bo')
        else:
            plt.plot(x1[j],y1[j],'go')

    move(20, 20,'right')
    
    plt.gca().invert_yaxis()
    plt.axes().set_aspect('equal')
    plt.show()


def move(sl0, sr0, direction): #input direction as a string
    
    R1i = sl0*CABLE_LENGTH_CHANGE_PER_STEP
    R2i = sr0*CABLE_LENGTH_CHANGE_PER_STEP
    x0 = (WORKSPACE_WIDTH**2-R2i**2+R1i**2)/(2*WORKSPACE_WIDTH)
    y0 = sqrt(fabs((4*WORKSPACE_WIDTH**2*R1i**2 
                    -(WORKSPACE_WIDTH**2-R2i**2+R1i**2)**2)/(4*WORKSPACE_WIDTH**2)))
    
    xn = []
    yn = []
    xn.append(x0)
    yn.append(y0) 
    
    drn = []
    R1n = []
    R2n = []
    xsee = []
    ysee = []
    
    valb = 1 #if valb = 1, point is within acceptable boundary; valb = 0, then not
    
    while valb == 1:

        R1, R2, dr = dirpoints(R1i,R2i,direction)
        
        x = []
        y = []
        
        for i in range(0,len(R1)):
    
            xp = (WORKSPACE_WIDTH**2-R2[i]**2+R1[i]**2)/(2*WORKSPACE_WIDTH)
            yp = sqrt(fabs((4*WORKSPACE_WIDTH**2*R1[i]**2 
                            -(WORKSPACE_WIDTH**2-R2[i]**2+R1[i]**2)**2)/(4*WORKSPACE_WIDTH**2)))
            x.append(xp)
            y.append(yp)
           
        diff = []
        
        for j in range(0,len(x)):
            if direction == 'up' or direction == 'down':
                d = fabs(x[j]-x0)
            elif direction == 'left' or direction == 'right':
                d = fabs(y[j]-y0)
            
            diff.append(d)
            
        hdi = diff.index(min(diff)) #find index of point with minmum horizontal difference from initial point
        
        valb = boundary(x[hdi],y[hdi],valb)
          
        if valb == 1:
            R1n.append(R1[hdi])
            R2n.append(R2[hdi])
            xn.append(x[hdi]) #next point x value
            yn.append(y[hdi]) #next point y value
            drn.append(dr[hdi]) #next point direction
            xsee.append(x) #list of x coordinates of all points considered
            ysee.append(y) #list of y coordinates of all points considered
                
            R1i = R1[hdi]
            R2i = R2[hdi]
            
            plt.plot(xsee,ysee,'co')
            plt.plot(xn, yn,'mo')
            
    print(drn)
        
def boundary(x,y,valb):
    
        #evaluate tension at point
        alphaT = atan(x/y)
        betaT = atan((WORKSPACE_WIDTH-x)/y)
        T1 = GONDOLA_WEIGHT/(sin(alphaT)*(tan(betaT))**-1+cos(alphaT)) #cable tension - N in cable that is connected to the origin
        T2 = T1*sin(alphaT)/sin(betaT)
        
        #check that point satisfies minimum and maximum tension requirements
        if T1 > MAX_CABLE_TENSION or T2 > MAX_CABLE_TENSION:
            valb = 0
        elif (T1*sin(alphaT) < MIN_HORIZ_CABLE_TENSION or 
              T2*sin(betaT) < MIN_HORIZ_CABLE_TENSION ):
            valb = 0
        elif x < 0 or x > WORKSPACE_WIDTH:
            valb = 0
        elif y < 0 or y > WORKSPACE_HEIGHT: #check that point is within canvas height; required for down direction case only
            valb = 0
        else:
            valb = 1
        
        return valb

def dirpoints(R1i, R2i, direction):
    
    if direction == 'up':
        R1 = [ R1i-CABLE_LENGTH_CHANGE_PER_STEP, R1i-CABLE_LENGTH_CHANGE_PER_STEP, R1i]
        R2 = [ R2i, R2i-CABLE_LENGTH_CHANGE_PER_STEP, R2i-CABLE_LENGTH_CHANGE_PER_STEP]
        dr = ['ul', 'u', 'ur']
        
    elif direction == 'down':
        R1 = [ R1i, R1i+CABLE_LENGTH_CHANGE_PER_STEP, R1i+CABLE_LENGTH_CHANGE_PER_STEP]
        R2 = [ R2i+CABLE_LENGTH_CHANGE_PER_STEP, R2i+CABLE_LENGTH_CHANGE_PER_STEP, R2i]
        dr = ['dl', 'd', 'dr']
        
    elif direction == 'left':
        R1 = [ R1i-CABLE_LENGTH_CHANGE_PER_STEP, R1i-CABLE_LENGTH_CHANGE_PER_STEP, R1i]
        R2 = [ R2i, R2i+CABLE_LENGTH_CHANGE_PER_STEP, R2i+CABLE_LENGTH_CHANGE_PER_STEP]
        dr = ['lu', 'l', 'ld']
        
    elif direction == 'right':
        R1 = [ R1i, R1i+CABLE_LENGTH_CHANGE_PER_STEP, R1i+CABLE_LENGTH_CHANGE_PER_STEP]
        R2 = [ R2i-CABLE_LENGTH_CHANGE_PER_STEP, R2i-CABLE_LENGTH_CHANGE_PER_STEP, R2i]
        dr = ['ru', 'r', 'rd']
        
    return(R1, R2, dr)
    
main()
