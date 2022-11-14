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
