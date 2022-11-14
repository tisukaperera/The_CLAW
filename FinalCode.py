## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)


## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Example to rotate the base: arm.rotateBase(90)
import random
import time

#coordinates
home = [0.4064, 0.0, 0.4826]
pick_up = [0.4814, 0.0, 0.0287]

#creating list for cages already been used
used_cage_list = []

#arm thresholds
threshold_1 = 0.00
threshold_2 = 0.10
threshold_3 = 0.20
threshold_4 = 0.50
threshold_5 = 0.60
threshold_6 = 1.00

#take ID no. as parameter then returns location of dropoff based on ID
def autobin_location(ID):
    #small red cage location and ID
    if ID == 1:
        location = [-0.5883, 0.2347, 0.364]

    #small green cage location and ID
    elif ID == 2:
        location = [0.0, -0.6231, 0.3647]

    #small blue cage location and ID
    elif ID == 3:
        location = [0.0, -0.6321, 0.3647]

    #large red cage location and ID
    elif ID == 4:
        location = [-0.3782, 0.1528, 0.2147]

    #large green cage location and ID
    elif ID == 5:
        location = [0.0, -0.4079, 0.2147]

    #large blue cage location and ID
    elif ID == 6:
        location = [0.0, -0.4079, 0.2147]
    return location

#takes muscle value and move arm based on value and return where it moved as string
def move_end_effector(ID):
    box_instruction = "nothing"

    #move arm to home location
    if arm.emg_left() == threshold_1:
        box_instruction = "goHome"
        arm.move_arm(home[0],home[1],home[2])

    #pick up cage when it spawns
    elif arm.emg_left() >= threshold_2 and arm.emg_left() < threshold_3:
        box_instruction = "pickUpBox"
        time.sleep(1)
        arm.move_arm(pick_up[0],pick_up[1],pick_up[2])
    
    #move box to dropoff location
    elif arm.emg_left() == threshold_6:
        box_instruction = "moveBox"
        #set ID location as a list
        location = autobin_location(ID)
        time.sleep(1)
        arm.move_arm(location[0],location[1],location[2])

    return box_instruction

#open and close claw using muscle values
def control_end_effector():
    #open the claw
    if arm.emg_right() == threshold_6:
        arm.control_gripper(40)
    
    #close the claw
    elif arm.emg_right() == threshold_1:
        arm.control_gripper(-40)

#open autoclave depending on value of muscle and ID number
def open_autoclave(ID):
    if arm.emg_right() >= threshold_4 and arm.emg_right() < threshold_5:

        #open red autoclave
        if ID == 4:
            arm.open_red_autoclave(True)

        #open green autoclave
        if ID == 5:
            arm.open_green_autoclave(True)

        #open blue autoclave
        if ID == 6:
            arm.open_blue_autoclave(True)
                    
def close_autoclave(ID):

        #close red autoclave
        if ID == 4:
            arm.open_red_autoclave(False)

        #close green autoclave
        if ID == 5:
            arm.open_green_autoclave(False)

        #close blue autoclave
        if ID == 6:
            arm.open_blue_autoclave(False)

#spawn random cage by choosing random number and returning ID spawned cage
def spawn_cage():
    #pick random number between 1 and 6
    container_ID = random.randint(1,6)

    #check if the random number has already been used by comparing to list
    check_ID = container_ID in used_cage_list

    #while the container cage has already been used
    while check_ID == True:
        #pick another random number
        container_ID = random.randint(1,6)

        #check again with list
        check_ID = container_ID in used_cage_list

        #the cage has not been used yet
        if check_ID == False:
            #add cage ID to the list
            used_cage_list.append(container_ID)

            #spawn the cage
            ID = arm.spawn_cage(container_ID)

            print(used_cage_list)
        return ID

#main function
def main():
    #number of cycles program has run through
    cycle = 0

    #no cage is being moved
    running = False

    #when no cage is being moved
    while running == False:
        #when the program on 6th cycle
        if cycle == 6:
            #exit program
            sys.exit()

        #add 1 to number of cycles
        cycle += 1

        #spawn the cage and set its returned number as an ID
        ID = spawn_cage()

        #the program is now moving a cage
        running =True

        #while the program is moving a cage
        while running == True:
            #call function to move arm and set as a value
            move_value = move_end_effector(ID)

            #if it is one of the big autoclaves
            if ID == 4 or ID == 5 or ID == 6:
                #use the function that opens the autoclave depending on ID
                open_autoclave(ID)

            #if the function wants to pick up the box close/open gripper
            if move_value == "pickUpBox":
                control_end_effector()

            #if it moves the box to drop off location
            elif move_value == "moveBox":

                #when the program is moving the box
                while running == True:
                    #close/open gripper
                    control_end_effector()

                    #if function returned go home, then move home and close any open autoclaves
                    if move_end_effector(ID) == "goHome":
                        close_autoclave(ID)

                        #program is no loger moving box
                        running = False