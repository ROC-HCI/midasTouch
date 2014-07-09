# COMMENT - overview of program

import Leap, sys, thread, time
import pygame
import random
import math
import serial

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

DEBUG_FLAG = True
DRAW_THRESHOLD = 55  # DISTANCE BETWEEN THUMB AND INDEX DEFINING WHEN DRAWING
CURSOR_TO_INK_DISTANCE_THRESHOLD = 20 # pixel units

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)


# pick a better name?
class Block(pygame.sprite.Sprite):
    """
    This class represents the cursor and data that is drawn.
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
        
# FINGER NUMBERS ASSIGNED BY LEAP LIBRARY IS DIFFERENT BASED ON
# OS?

#IN ORDER TO WORK ON BOTH OS REPLACE HARDCODING WITH 
# On Ty's Machine
# 0 = middle finger
# 1 = ring finger
# 2 = index finger
# 3 = pinkey finger
# 4 = Thumb

# On Morgan's Machine
# 0 = Thumb
# 1 = index finger
# 2 = middle finger
# 3 = ring finger
# 4 = pinkey finger  

INDEX_FINGER_NUM = 1
THUMB_NUM = 0

#INDEX_FINGER_NUM = 2
#THUMB_NUM = 4

# pick a better name
class SampleListener(Leap.Listener):
    """
    This is a listener that uses LeapMotion API.
    Gets data from Leap. Detects gestures.
    Updates drawing state variables
    
    """
         
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    
    #Index Finger Point
    #  the index fingers location in raw LEAP coordinates
    #  y represents distance from the leap (up and down), (0-200) zeroed on leap
    #  x is the is side to side (-200 to 200, zeroed on leap)
    #  z is the (forward and back) (-200 to 200, zeroed on leap) 
    indexx = 0    
    indexy = 0
    indexz = 0  
    
    #Boolean State Variables 
    colliding = False
    drawing = False
    tapping = False
    swiping = False    

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        """
        Called as soon as you connect to the Leap 
        """
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

    def onGesture(gesture):
        if gesture.type == Leap.Gesture.TYPE_CIRCLE:
            circle = CircleGesture(gesture)

            # Determine clock direction using the angle between the
            # pointable and the circle normal 
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
        
    def dumpFrame(frame):
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        
        
    def on_frame(self, controller):
        """
        Get the most recent frame (index finger position) and report 
        some basic information.
        Launch actions based on gestures.
        Update state variables (this.drawing)
        """
        frame = controller.frame()

        if(DEBUG_FLAG):
            dumpFrame(frame)
        
        self.indexx = frame.hands.leftmost.fingers[INDEX_FINGER_NUM].tip_position.x
        self.indexy = frame.hands.leftmost.fingers[INDEX_FINGER_NUM].tip_position.y
        print(self.indexx)
            
        if(self.drawDistance(frame) < DRAW_THRESHOLD):
            self.drawing = True
        else:
            self.drawing = False
                

        for gesture in frame.gestures():
            self.onGesture(gesture)
          
          
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
    
    def fingerDistance(self, frame):
        """
        Calculates the realworld distance between the 0th and 1st
        fingers in the leftmost hand
        """
        x = frame.hands.leftmost.fingers[INDEX_FINGER_NUM].tip_position.x
        y = frame.hands.leftmost.fingers[INDEX_FINGER_NUM].tip_position.y
        z = frame.hands.leftmost.fingers[INDEX_FINGER_NUM].tip_position.z
        
        x2 = frame.hands.leftmost.fingers[THUMB_NUM].tip_position.x
        y2 = frame.hands.leftmost.fingers[THUMB_NUM].tip_position.y
        z2 = frame.hands.leftmost.fingers[THUMB_NUM].tip_position.z
        
        distance = (math.pow(x - x2,2) + math.pow(y - y2,2) + math.pow(z - z2,2))**(.5)
        
        return distance
    
    def spriteDistance(self, spriteA, spriteB):
        """
        TODO
        """
        print("I like chocolate")
        
    def collisionDetect(self, cursor, ink_blot_list):
        """
        cycles through all of the drawn sprites and returns true if collision
        detected (EXPAND HERE)
        We can likely speed this up eventually. Think about how to speed up.
        Tile system?
        """
        for ink_blot in ink_blot_list:            
            if( spriteDistance(cursor, ink_blot) > CURSOR_TO_INK_DISTANCE_THRESHOLD):
                return True
            '''
            if(player.rect.x > sprite.rect.x and player.rect.x < sprite.rect.x + 20):
                if(player.rect.y > sprite.rect.y and player.rect.y < sprite.rect.y + 15):
                    return True
            '''
      
def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller() # 
    
    # Initialize Pygame
    pygame.init()
     
    # Set the height and width of the screen
    # make these globals defined at top
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
         
    '''
    for i in range(50):
        # This represents a block
        block = Block(BLACK, 20, 15)
     
        # Set a random location for the block
        block.rect.x = random.randrange(screen_width)
        block.rect.y = random.randrange(screen_height)
     
        # Add the block to the list of objects
        block_list.add(block)
        all_sprites_list.add(block)
    '''
     
    # Create a RED player block
    # rename to cursor
    player = Block(RED, 20, 15)
    all_sprites_list.add(player)
    
    # TODO do we need this?
    # Create Drawn Block
    path = Block(GREEN, 20, 15)
     
    # Loop until the user clicks the close button.
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
     
    score = 0
    
    
    #-------------------SERIAL PORTING-------------------------
    
    ser = serial.Serial('/dev/cu.usbmodemfd131',9600)  # open first serial port
    #print ser.name          # check which port was really used
     
    # ---------------- Main Program Loop ----------------------
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True
            
        # Clear the screen
        screen.fill(WHITE)
        # TODO double check if this can run outside the loop
        controller.add_listener(listener)
     
        # Get the current mouse position. This returns the position
        
        
        player.rect.x = -listener.indexx * 5 + screen_width/2
        player.rect.y = listener.indexy * 5 - screen_height*3
    
        ''' removed, make sure doesn't kill anything
        # See if the player block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
        '''
        
        if(listener.drawing == True):
            # Create Drawn Block
            # TODO only draw a new ink block if no current ink blot is at the 
            # exact same location
            path = Block(GREEN, 20, 15)
            path.rect.y = player.rect.y
            path.rect.x = player.rect.x
            all_sprites_list.add(path)
            drawn_sprites_list.add(path)

        listener.colliding = listener.collisiondetect(player, 
                                                     drawn_sprites_list)
        
        #print ser.name          # check which port was really used
            
        #----------------------Write to COM4-------------------
        if(listener.colliding):
            ser.write('1') 
            print 'COLLLIDING'
        else:
            ser.write('0')                
     
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
