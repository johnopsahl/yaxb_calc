#This script assists with determining the optimal canvas location for 
# a polar wall plotter given the workspace size, machine parameters,
# and desired canvas width.

from math import sqrt,pi,floor,fabs,sin,cos,atan,tan
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#general inputs
STEPS_PER_REVOLUTION = 3 #steps per revolution to display
CABLE_PULLEY_RADIUS = 2 #radius of cable pulley (cm)
GONDOLA_MASS = 1.2 #gondola mass (kg)
RATED_MOTOR_TORQUE = 56 #rated motor torque (N*cm)
WORKSPACE_HEIGHT = 1.5 #workspace height (m)
WORKSPACE_WIDTH = 1.5 #workspace width (m)
CANVAS_WIDTH = .75 #desired width of canvas (m)

#define cable tension limits
MAX_CABLE_TENSION = RATED_MOTOR_TORQUE/CABLE_PULLEY_RADIUS #maximum cable tension threshold (N)
MIN_HORIZ_CABLE_TENSION = 3 #minimum horizontal cable tension threshold (N)

CABLE_LENGTH_CHANGE_PER_STEP = 2*(CABLE_PULLEY_RADIUS/100)*pi/STEPS_PER_REVOLUTION #smallest cable length change possible (m)
GONDOLA_WEIGHT = GONDOLA_MASS*9.81 #weight of gondola (N)

def main():

    R1 = CABLE_LENGTH_CHANGE_PER_STEP

    #generate coordinates from geometry equations 
    #R1 is the left cable radius
    #R2 is the right cable radius
    
    #while R1 is less than diagonal of canvas
    while R1 < sqrt(WORKSPACE_HEIGHT**2+WORKSPACE_WIDTH**2): 
    
        #R2 is floor hypotenuse
        R2 = floor(sqrt(R1**2+WORKSPACE_WIDTH**2)
             /CABLE_LENGTH_CHANGE_PER_STEP)*CABLE_LENGTH_CHANGE_PER_STEP
        
        while R2 > WORKSPACE_WIDTH-R1:
            
            x_plot = (WORKSPACE_WIDTH**2+R1**2-R2**2)/(2*WORKSPACE_WIDTH)
            y_plot = WORKSPACE_HEIGHT-sqrt(fabs((4*WORKSPACE_WIDTH**2*R2**2 
                     -(WORKSPACE_WIDTH**2-R1**2+R2**2)**2)/(4*WORKSPACE_WIDTH**2)))
                
            #the point is on the canvas
            if x_plot <= WORKSPACE_WIDTH and y_plot <= WORKSPACE_HEIGHT and y_plot > 0:
                
                cable_tension_state = cable_tension(x_plot,y_plot)
                
                #apply color to points based on cable tension
                if cable_tension_state == 1:
                    plt.plot(x_plot,y_plot,'ro',alpha = 0.75)
                elif cable_tension_state == 2:
                    plt.plot(x_plot,y_plot,'bo',alpha = 0.75)
                elif cable_tension_state == 3:
                    plt.plot(x_plot,y_plot,'go',alpha = 0.75,zorder = 1)
                    
            R2 = R2 - CABLE_LENGTH_CHANGE_PER_STEP
            
        R1 = R1 + CABLE_LENGTH_CHANGE_PER_STEP

    plt.axes().set_aspect('equal')
    
    increment = 0.01
    canvas_width_flag = False    
    
    #start from the top of the workspace and left side of the canvas
    #increment down the workspace until the first valid canvas point is found
    x_mid = WORKSPACE_WIDTH/2
    y_top = WORKSPACE_HEIGHT - increment
    
    top_flag = False
    
    while top_flag == False:
        
        cable_tension_state = cable_tension(x_mid,y_top)
        
        #cable tension is above limits        
        if cable_tension_state == 3:
            
            top_flag = True
            #print(y_top)
            
            x_left_max = x_mid
            
            max_canvas_width_flag = False
            
            #determine the largest cable width possible for the workspace
            while max_canvas_width_flag == False:
                
                cable_tension_state = cable_tension(x_left_max, y_top)
                
                if cable_tension_state == 2:
                    max_canvas_width_flag = True
                else:
                    x_left_max -= increment
            
            if CANVAS_WIDTH > (WORKSPACE_WIDTH/2-x_left_max)*2:
                canvas_width_flag = True
                print("The canvas width is too large for the workspace")
                break
                
            #start from y_top, increment down the workspace until the first low tension
            #point is found
            x_left = x_mid - CANVAS_WIDTH/2
            y_bottom = y_top
            
            bottom_flag = False
            
            while bottom_flag == False:
                
                cable_tension_state = cable_tension(x_left,y_bottom)
                
                #cable tension is below limits
                if cable_tension_state == 2 or y_bottom-increment < 0:
                    bottom_flag = True
                    #print(y_bottom)
                else:
                    y_bottom -= increment
                    
        else:
            y_top -= increment
    
    if canvas_width_flag == False:
        
        x_left = round(x_left,2)
        x_right = round(x_left + CANVAS_WIDTH,2)
        y_top = round(y_top,2)
        y_bottom = round(y_bottom,2)
        
        rect = patches.Rectangle((x_left,y_bottom),
                                 CANVAS_WIDTH,
                                 y_top - y_bottom,
                                 linewidth = 2,
                                 fill = False,
                                 zorder = 2)
                                 
        plt.gca().add_patch(rect)
        
        #bottom left
        plt.annotate('(%s,%s)' %(x_left,y_bottom),
                     xy = (x_left,y_bottom),
                     textcoords='data',
                     size ='medium',
                     zorder = 3, 
                     bbox=dict(boxstyle='round', fc='1'), 
                     horizontalalignment='right', 
                     verticalalignment = 'top')
        
        #top left
        plt.annotate('(%s,%s)' %(x_left,y_top),
                     xy = (x_left,y_top),
                     textcoords='data',
                     size ='medium',
                     zorder = 3, 
                     bbox=dict(boxstyle='round', fc='1'), 
                     horizontalalignment='right', 
                     verticalalignment = 'bottom')
        
        #bottom right
        plt.annotate('(%s,%s)' %(x_right,y_bottom),
                     xy = (x_right,y_bottom),
                     textcoords='data',
                     size ='medium',
                     zorder = 3, 
                     bbox=dict(boxstyle='round', fc='1'), 
                     horizontalalignment='left', 
                     verticalalignment = 'top')
        
        #top right
        plt.annotate('(%s,%s)' %(x_right,y_top),
                     xy = (x_right,y_top),
                     textcoords='data',
                     size ='medium',
                     zorder = 3, 
                     bbox=dict(boxstyle='round', fc='1'), 
                     horizontalalignment='left', 
                     verticalalignment = 'bottom')
    
    plt.show()

def cable_tension(x,y):
    
    alphaT = atan(x/(WORKSPACE_HEIGHT-y))
    betaT = atan((WORKSPACE_WIDTH-x)/(WORKSPACE_HEIGHT-y))
    T1 = GONDOLA_WEIGHT/(sin(alphaT)*tan(betaT)**-1+cos(alphaT)) #left cable tension - N
    T2 = T1*sin(alphaT)/sin(betaT) #right cable tension - N
    
    #determine cable tension state based on 
    if (T1 > MAX_CABLE_TENSION or T2 > MAX_CABLE_TENSION):
        cable_tension_state = 1
    elif (0 < T1*sin(alphaT) < MIN_HORIZ_CABLE_TENSION 
          or 0 < T2*sin(betaT) < MIN_HORIZ_CABLE_TENSION ):
        cable_tension_state = 2
    else:
        cable_tension_state = 3
    
    return cable_tension_state
    
main()
    
    