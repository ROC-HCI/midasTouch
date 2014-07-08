import Leap, sys, thread, time
import pygame
import random
import math
import serial

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)



class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
 
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        
        
        
        
        
        
# On Ty's Machine
# 0 = middle finger
# 1 = ring finger
# 2 = pointer finger
# 3 = pinkey finger
# 4 = Thumb

# On Morgan's Machine
# 0 = Thumb
# 1 = pointer finger
# 2 = middle finger
# 3 = ring finger
# 4 = pinkey finger
        
        

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    
    #Index Finger Point
    indexx = 0
    indexy = 0
    indexz = 0  
    
    #Bloolean State Variables
    colliding = False
    drawing = False
    tapping = False
    swiping = False
    
    

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")







    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              #frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            #handType = "Left hand" if hand.is_left else "Right hand"

            #hand.palm_position

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            
            
            
            self.indexx = frame.hands.leftmost.fingers[1].tip_position.x
            self.indexy = frame.hands.leftmost.fingers[1].tip_position.y
            print( self.indexx)
            
            # Calculate the hand's pitch, roll, and yaw angles
            #print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                #direction.pitch * Leap.RAD_TO_DEG,
                #normal.roll * Leap.RAD_TO_DEG,
                #direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bones (MAC ONLY)     
            #print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                #arm.direction,
                #arm.wrist_position,
                #arm.elbow_position)
                
                
                
        #-----------------------Drawing-----------------------
        if(self.drawdistance(frame) < 55):
            self.drawing = True
            
            
        #print self.drawing
           

        # Get tools
        for tool in frame.tools:

            print("  Tool id: %d, position: %s, direction: %s" % (
                tool.id, tool.tip_position, tool.direction))

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal 
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

              #  print( "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
               #         gesture.id, self.state_names[gesture.state],
                #        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness))

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                #print("  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                #        gesture.id, self.state_names[gesture.state],
                #        swipe.position, swipe.direction, swipe.speed))

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                #print( "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                #        gesture.id, self.state_names[gesture.state],
                #        keytap.position, keytap.direction ))
                self.tapping = True

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                #print( "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                #        gesture.id, self.state_names[gesture.state],
                #        screentap.position, screentap.direction ))

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print("")

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
    
    def drawdistance(self, frame):
        pointerx = frame.hands.leftmost.fingers[0].tip_position.x
        pointery = frame.hands.leftmost.fingers[0].tip_position.y
        pointerz = frame.hands.leftmost.fingers[0].tip_position.z
        
        middlex = frame.hands.leftmost.fingers[1].tip_position.x
        middley = frame.hands.leftmost.fingers[1].tip_position.y
        middlez = frame.hands.leftmost.fingers[1].tip_position.z
        
        distance = (math.pow(pointerx - middlex,2) + math.pow(pointery - middley,2) + math.pow(pointerz - middlez,2))**(.5)
        
        return distance
    
    #cycles through all of the drawn sprites and returns true if collision detected (EXPAND HERE)
    def collisiondetect(self, player, drawn_sprites_list):
        for sprite in drawn_sprites_list:
            if(player.rect.x > sprite.rect.x and player.rect.x < sprite.rect.x):
                if(player.rect.y > sprite.rect.y and player.rect.y < sprite.rect.y):
                    return True
                else:
                    return False
            else:
                return False
                    
                
        
        








def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller

    # Keep this process running until Enter is pressed
    
    
    
    # Initialize Pygame
    pygame.init()
     
    # Set the height and width of the screen
    screen_width = 700
    screen_height = 400
    screen = pygame.display.set_mode([screen_width, screen_height])
     
    # This is a list of 'sprites.' Each block in the program is
    # added to this list. The list is managed by a class called 'Group.'
    block_list = pygame.sprite.Group()
     
     
     
    # This is a list of every sprite. 
    # All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group()
    
    #List of all sprites drawn (used for clearing screen)
    drawn_sprites_list = pygame.sprite.Group()
    
    
     
     
    for i in range(50):
        # This represents a block
        block = Block(BLACK, 20, 15)
     
        # Set a random location for the block
        block.rect.x = random.randrange(screen_width)
        block.rect.y = random.randrange(screen_height)
     
        # Add the block to the list of objects
        block_list.add(block)
        all_sprites_list.add(block)
     
    # Create a RED player block
    player = Block(RED, 20, 15)
    all_sprites_list.add(player)
    
    # Create Drawn Block
    path = Block(GREEN, 20, 15)
     
    # Loop until the user clicks the close button.
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
     
    score = 0
    
    
    #-------------------SERIAL PORTING-------------------------
    
    #ser = serial.Serial('COM4',9600)  # open first serial port
    #print ser.name          # check which port was really used
    
    #if(listener.collisiondetect(player, drawn_sprites_list)):
        #ser.write('1') 
    #else:
        #ser.write('0')
     
     
     
     
    # ---------------- Main Program Loop ----------------------
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
     
        # Clear the screen
        screen.fill(WHITE)
        controller.add_listener(listener)
     
        # Get the current mouse position. This returns the position
        
        
        player.rect.x = -listener.indexx * 5 + screen_width/2
        player.rect.y = listener.indexy * 5 - screen_height*3
     
        # See if the player block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
        
        
        if(listener.drawing == True):
            # Create Drawn Block
            path = Block(GREEN, 20, 15)
            path.rect.y = player.rect.y
            path.rect.x = player.rect.x
            all_sprites_list.add(path)
            drawn_sprites_list.add(path)
            
            
        listener.drawing = False
        
        
        listener.colliding = listener.collisiondetect(player, 
                                                     drawn_sprites_list)
        
        #print ser.name          # check which port was really used
            
        #----------------------Write to COM4-------------------
        #if(listener.collisiondetect(player, drawn_sprites_list)):
        #    ser.write('1') 
        #else:
        #    ser.write('0')        
        
     
        # Check the list of collisions.
        for block in blocks_hit_list:
            score += 1
            print(score)
     
        # Draw all the spites
        all_sprites_list.draw(screen)
     
        # Limit to 60 frames per second
        clock.tick(60)
     
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
          
    pygame.quit()


if __name__ == "__main__":
    main()
