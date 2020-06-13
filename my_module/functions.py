import random

ship_size = {"battleship": 4, "submarine": 3, "destroyer": 3, "patrol boat": 2}
directions_list = ["left", "right", "up", "down"]

def boat_coords(boat, direction, start_x, start_y):
    """Return all coordinates of the boat given it's type, direction, and back.
    
    Parameters
    ----------
    boat : string
        The type of boat
    direction : string
        The direction the boat is facing
    start_x : int
        The column the back of the boat is at
    start_y : int
        The row the back of the boat is on
    
    Returns
    -------
    coords : list of tuples
        The list of points the given boat is at 
    """
    coords = [(start_x, start_y)]
        
    for i in range(1, ship_size[boat]):
        if direction == "left":
            new_x = coords[0][0] - i
            y_loc = coords[0][1]
            coords.append((new_x, y_loc))
                
        elif direction =="right":
            new_x = coords[0][0] + i
            y_loc = coords[0][1]
            coords.append((new_x, y_loc))
                
        elif direction == "down":
            new_y = coords[0][1] + i
            x_loc = coords[0][0]
            coords.append((x_loc, new_y))
                
        else:
            new_y = coords[0][1] - i
            x_loc = coords[0][0]
            coords.append((x_loc, new_y))
            
    return coords

class Battleship:
    
    def __init__(self):
        self.board = [["+", "+", "+", "+", "+", "+", "+"] for i in range(7)]
        self.ship_dir = {"battleship": None, "submarine": None, \
            "destroyer": None, "patrol boat": None}
        self.ships_locs = {"battleship": None, "submarine": None, \
            "destroyer": None, "patrol boat": None}
        self.moves = []
        self.cpu = Opponent()
        self.cpu.set_ships()
        
    def print_board(self, both = False):
        """Print the game board.
    
        Parameters
        ----------
        both : boolean
            determine whether both user's and computer's boards should be
            printed
        """
        if both:
            print("\n  Your Board:       Opponent's Board:")
            print("  0 1 2 3 4 5 6        0 1 2 3 4 5 6")
            
        else:
            print("\n  Your Board:")
            print("  0 1 2 3 4 5 6")
            
        for i, row in enumerate(self.board):
            print(str(i), end = " ")
            
            for col in row:
                print(col, end = " ")
            
            if both:
                print("    " + str(i), end = "  ")
            
                for col in self.cpu.board[i]:
                    print(col, end = " ")
            
            print()
            
    def adjust_board(self, boat):
        """Change the board in order to account for a boat being placed.
    
        Parameters
        ----------
        boat : string
            The type of boat being placed on the map
        """
        for i in self.ships_locs[boat]:
            if self.ship_dir[boat] == "left" or self.ship_dir[boat] == "right":
                self.board[i[1]][i[0]] = "-"
            else:
                self.board[i[1]][i[0]] = "|"
        
    def verify_side(self, side):
        """Verify that the column or row number given is valid, and keep
            adjusting until it is valid.
    
        Parameters
        ----------
        side : string
            determine that the side is a digit with the a value 0-6

        Returns
        -------
        side : int
            The appropriate side type casted as an int
        """
        acceptable = False
            
        while acceptable is False:
            if not side.isdigit():
                side = input("That is not a number, please enter a number " + 
                    "0-6 ")
            elif int(side) < 0 or int(side) > 6:
                side = input("That number is off the map, please enter a "
                    "number 0-6 ")
                    
            if side.isdigit() and int(side) >= 0 and int(side) <= 6:
                acceptable = True
                    
        return int(side)    
        
    def boat_set_up(self, boat):    
        """Ask the user for information about where they want the boat, and
            update accordingly
    
        Parameters
        ----------
        boat : string
            The type of boat the user is setting up
        """ 
        direction = input("Does your " + boat + " face left, right, up, or " +
            "down? ")
        self.ship_dir[boat] = direction.lower()

        while self.ship_dir[boat] not in directions_list:
            direction = input("That's not a valid direction, please enter " +
                "left, right, up, or down. ")
            self.ship_dir[boat] = direction.lower()

        x = input("On what column is the back of your " + boat + "?")
        x = self.verify_side(x)

        y = input("On what row is the back of your " + boat + "?")
        y = self.verify_side(y)
        
        self.ships_locs[boat] = boat_coords(boat, self.ship_dir[boat], x, y)
        
        for i in self.ships_locs[boat]:
            if i[0] < 0 or i[0] > 6 or i[1] < 0 or i[1] > 6:
                print("Please try again, boats can't go off the map.")
                self.boat_set_up(boat)
                break
        
        for i in self.ships_locs:
            if i != boat and self.ships_locs[i] != None:
                for loc in self.ships_locs[i]:
                    if loc in self.ships_locs[boat]:
                        print("Please try again, boats can't overlap.")
                        self.boat_set_up(boat)
                        return

        self.adjust_board(boat)
        
    def cpu_turn(self):
        """ The computer takes its turn and keeps going until it misses
        """
        move = self.cpu.move()
                
        self.cpu.moves.append(move)
            
        for boat in self.ships_locs:
            if move in self.ships_locs[boat]:
                self.board[move[1]][move[0]] = "X"
                self.ships_locs[boat].remove(move)
                if len(self.ships_locs[boat]) == 0:
                    print("Your " + boat + " has been sunk!")
                else:
                    print("Your " + boat + " was hit!")
                
                self.cpu_turn()

                return

        self.board[move[1]][move[0]] = "O"
        print("Your opponent missed.\n")
        self.print_board(both = True)
    
    def user_turn(self):
        """ The user takes its turn and keeps going until he or she misses
        """
        x = input("What column do you want to strike? ")
        x = self.verify_side(x)
        
        y = input("What row do you want to strike? ")
        y = self.verify_side(y)
        
        while (x, y) in self.moves:
            print("Use a location that you haven't used before.")
            x = input("What column do you want to strike? ")
            x = self.verify_side(x)
            
            y = input("What row do you want to strike? ")
            y = self.verify_side(y)
        
        move = (x, y)
        self.moves.append(move)
        
        for boat in self.cpu.ships_locs:
            if move in self.cpu.ships_locs[boat]:
                self.cpu.board[move[1]][move[0]] = "X"
                self.cpu.ships_locs[boat].remove(move)
                if len(self.cpu.ships_locs[boat]) == 0:
                    print("\nYou sunk your opponent's " + boat + "!")
                else:
                    print("\nYou hit your opponent's " + boat + "!")

                
                self.print_board(both = True)
                self.user_turn()

                return
            
        self.cpu.board[move[1]][move[0]] = "O"
        print("\nYou missed your opponent.")
    
    def is_end(self):
        """ Determine whether or not the game is over.

        Returns
        -------
        boolean
            True if all of the user's boats have no points on the map
        """
        cpu_empty = 0
        user_empty = 0
        
        for boat in self.cpu.ships_locs:
            if len(self.cpu.ships_locs[boat]) == 0:
                cpu_empty += 1
                
        if cpu_empty == 4:
            print("Congratulations, you win!")
            return True
            
        for boat in self.ships_locs:
            if len(self.ships_locs[boat]) == 0:
                user_empty += 1
                
        if user_empty == 4:
            print("You have lost.")
            return True
        
        return False

class Opponent:
    def __init__(self):
        self.board = [["+", "+", "+", "+", "+", "+", "+"] for i in range(7)]
        self.ship_dir = {"battleship": None, "submarine": None, \
            "destroyer": None, "patrol boat": None}
        self.ships_locs = {"battleship": None, "submarine": None, \
            "destroyer": None, "patrol boat": None}
        self.moves = []
        
    def set_ships(self):
        """ Randomly assign the four boats on the computer's map, adjusting all
            necessary variables.
        """ 
        directions = ["left", "right", "up", "down"]
        for boat in self.ship_dir:
            self.ship_dir[boat] = random.choice(directions)

            x = random.randrange(7)
            y = random.randrange(7)
            self.ships_locs[boat] = boat_coords(boat, self.ship_dir[boat], x,\
                y)
            
            for i in self.ships_locs[boat]:
                if i[0] < 0 or i[0] > 6 or i[1] < 0 or i[1] > 6:
                    self.set_ships()
                    return

            for i in self.ships_locs:
                if i != boat and self.ships_locs[i] != None:
                    for loc in self.ships_locs[i]:
                        if loc in self.ships_locs[boat]:
                            self.set_ships()
                            return
        
    def move(self):
        """ Randomly generate a new point for the computer to shoot.
        """ 
        move = (random.randrange(7), random.randrange(7))
            
        while move in self.moves:
            move = (random.randrange(7), random.randrange(7))
                
        self.moves.append(move)        
        return move