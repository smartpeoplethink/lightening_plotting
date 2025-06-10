

# Window setup########################
scene.width = 800 #The width of your view window
scene.height = 400 #The height of your view window
######################################
 
# Parameters and Initial Conditions###
BaR = 10 #Radius of the ball
BaS = 1 #Scalar to change ball speed
Bh = 5 #Height of books in first stack of books
Bw = 30 #Width of books in first stack of books
Bs = -100 #X-value offset of the center of the first book stack
Tt = 0 #refrence point for drawing the books (not used in any real math)
Bc = 1 #condition for beginning to draw books (checked against time)
R1L = 100 #Length of first ramp
nB = 5 #The number of books in the first stack
R2L = 100 #Length of flat section **
n2B = 5 #The number of books in the second stack of books ***
B2c = 1 #condition for beginning second stack of books (checked against time)***
T2t = 0 #refrence point for drawing second stack of books(not used in any real math) ***
B2h = 5 #height of books in second stack of books ***
B2w = 30 #width of books in second stack of books ***
R3L= 100 #length of second ramp ***
#########################################
 
# Time and time step#####################
t = 0 #start time (this command sets the counter to 0)
tFinal = 100 #The end number on the counter to stop actions
tFinal2=100 #Same as above but for second loop (final counter number)**
#########################################
 
#Ramp and speed calculations#############
R1Y = Bh*nB #Starting Y-value coordinate for ramp (total Y value of ramp)
R1X = sqrt(R1L**2 - R1Y**2) #Starting X-value coordinate for ramp (total X value of ramp)
S1x = R1X/R1L*BaS #the horizontal vector of movement down first ramp
S1y = R1Y/R1L*BaS #the vertical vector of movement down first ramp
R3Y = B2h*n2B #Y-value for second ramp ***
R3X = sqrt(R3L**2 - R3Y**2) #X-value for third ramp ***
B2s = R1X + R2L + R3X + Bs + B2w #X-value of the centerpoint of the second stack of books ***
#########################################
 
#Drawing initial objects#################
#draw tabletop
Table= box(pos = vector(75,-6,0), size = vector(400, 10, 30), color = color.orange)
 
#Stack of books
Bc = Tt
while t<nB:
    Bc = Tt + Bh*t +Bh/2
    book = cylinder(pos = vector(Bs, Bc, 0), axis = vec(Bw, 0, 0), radius = Bh, color = color.yellow)
    t=t+1
ballstopx = Bs - Bw/2 - R1L/2
t=t+1
 
#Downward Ramp
R1h = Tt + Bh*t +Bh/2
R1s = Bs + Bw
ramp1 = cylinder(pos = vector(R1s, R1h, 0), axis = vec(R1X, -R1Y, 0), radius = Bh, color = color.white)
 
#Ball
BaX = R1s + BaR/2 
BaY = R1h+Bh + BaR/2
ball =  sphere(pos=vec(BaX,BaY,0), radius = BaR/2, color=color.red)
 
#draw ramp 2 **
R2h = Tt + Bh/2
R2s = Bs + Bw + R1X + R2L/2
ramp2 = box(pos = vector(R2s, R2h, 0), size = vector(R2L, Bh*4, 10), color = color.orange)
 
##########################################
 
#MOVEMENT COMMANDS LOCATED BELOW###############################################################################
 
 
#Command for ball rolling down first ramp################################################### 
 
scene.camera.follow(ball) #this makes the camera follow the ball
t=0 #resets the time counter to 0 at the start of the loop
 
theta = acos(R1X/R1L) #this calculates angle of the ramp
A1x = sin(theta)*cos(theta) #calculates x-value of acceleration
A1y = sin(theta)*sin(theta) #calculates y-value of acceleration
 
while t<tFinal: #sets the condition for this command taking place
    rate(20) #how many times per cycle the action will take place
    ball.pos.x = ball.pos.x + S1x #updates the x position of the ball at rate listed above every sec
    ball.pos.y = ball.pos.y - S1y #updates the y position of the ball at rate listed above every sec
    S1x = S1x + A1x #adjusts the update position based on the x acceleration
    S1y = S1y + A1y #adjusts the update position based on the y acceleration
    t=t+1 #makes it so ever cycle it adds 1 to the time counter
 
    if ball.pos.x > R1s + R1X: #sets condition for when the ball's x position reaches the end of the ramp 
        t=tFinal #sets the timer to the final value, so the loop stops
 
###########################################################################################
 
#Command for our second stage animation####################################################
 
t=0 #reset counter for second loop
S2x = S1x # carries over x-value speed from end of ramp 1
S2y = 0 #stop vertical movement of the ball as we hit the flat section
 
while t<tFinal2:#sets the condition for this command taking place
  rate(20) #how many timeps per cycle the action will take place
  ball.pos.x = ball.pos.x + S2x #updates the x position of the ball at rate above
  ball.pos.y = ball.pos.y + S2y #updates the y position of the ball at the rate above
  if ball.pos.x > R2s + .5*R2L - BaR*.5: #sets condition for when ball reaches end of plane
    t = tFinal2 #sets timer to the final for section 2 when above condition is met
  t=t+1 #increases the time counter by 1 every time loop runs
 
###########################################################################################