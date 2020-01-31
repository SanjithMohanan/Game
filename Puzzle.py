#I ran this code using Python 3.6 in PyCharm

#How to run the code
#   Compile the code
#   Run the code
#   Give initial state and goal state respectively as input
# examaple:
"""
Enter the initial state :: 1,0,3,8,2,4,7,6,5
Enter the goal state :: 1,2,3,8,0,4,7,6,5
<built-in function input>
Input state ::
1   0   3
8   2   4
7   6   5
Goal state ::
1   2   3
8   0   4
7   6   5
The solution can be found in  1 move(s)
Step  1  :: Move  2  from ( 2 , 2 ) to ( 1 , 2 )
1   2   3
8   0   4
7   6   5
"""

#About assign1.py
#   It contains two classes, Strips and Utility and a main method. The execution starts from the main method.

from builtins import print

#Utility class that holds methods for doing many functions required for this assignment.
class Utility:

    #This function reads input from the user
    def read_input_from_user(self):
        initial_state = input("Enter the initial state :: ")
        goal_state = input("Enter the goal state :: ")
        return initial_state,goal_state

    #The input read is in string format. So this method will convert it in to numbers
    def split_and_convert_to_integer(self, user_input):
        converted_input = [int(x) for x in user_input.split(",")]
        return converted_input

    #This function will create all possible moves possible in a 3*3 puzzle
    def getAllPossibleMoves(self):
        all_moves = []
        for value in range(1, 9):
            for i in range(1, 4):
                for j in range(1, 4):
                    if (i == 1 or i == 2):
                        all_moves.append((value, i, j, i+1, j))
                        #all_moves.append((value, i+1, j, i , j))
                    if (i == 2 or i == 3):
                        all_moves.append((value, i, j, i-1 , j))
                        # all_moves.append((value, i-1, j, i, j))
                    if (j == 2 or j == 3):
                        all_moves.append((value, i, j, i, j-1 ))
                        # all_moves.append((value, i, j-1, i , j))
                    if (j == 1 or j == 2):
                        all_moves.append((value, i, j, i, j+1))
                        # all_moves.append((value, i, j+1, i, j))
       # print(all_moves)
        return all_moves

    #Creates precondition required to move a tile
    def createMoveOperator(self, all_moves):
        precondition_action_remove = {}
        for entry in all_moves:
            precondition_action_remove[entry] = {
                "precondition": set([(entry[0], entry[1], entry[2]), (0, entry[3], entry[4])])
            }
        #print(precondition_action_remove)
        return precondition_action_remove

    #Test method- for testing purpose
    def getGoalState(self):
        return set(
            [(1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 2, 1), (5, 2, 2), (6, 2, 3), (7, 3, 1), (8, 3, 2), (0, 3, 3) ])

    #Defines position for all values from the input
    def define_position_for_input(self, input):
        index = 0
        input_positions = set()
        for i in range(1, 4):
            for j in range(1, 4):
                input_positions.add((input[index], i, j))
                index += 1  # incrementing the position from the inout list
        return input_positions

    #Returns position of 0 from the puzzle
    def get_position_of_0(self, anystate):
        for entry in anystate:
            if entry[0] == 0:
                return (entry[1], entry[2])

    #Returns the value at the position i,j
    def get_valueat_indexes(self, anystate, i, j):
        for entry in anystate:
            if (entry[1] == i and entry[2] == j):
                return entry[0]

    #Returns all possible moves in the puzzle realtive to the position of tile with value 0.
    def get_possible_moves(self, anystate):
        actions = set()
        utility = Utility()
        i, j = utility.get_position_of_0(anystate)
        if (i == 1 or i == 2): #checking whether tile can be moved towards right
            value = utility.get_valueat_indexes(anystate, i + 1, j)
            actions.add((value, i, j, i+1 , j)) #?
        if (i == 2 or i == 3): #checking whether tile can be moved towards left
            value = utility.get_valueat_indexes(anystate, i - 1, j)
            actions.add((value, i, j, i-1, j))
        if (j == 2 or j == 3):
            value = utility.get_valueat_indexes(anystate, i, j - 1)
            actions.add((value, i, j, i, j-1))#checking whether tile can be moved towards down
        if (j == 1 or j == 2):
            value = utility.get_valueat_indexes(anystate, i, j + 1)#checking whether tile can be moved towards up
            actions.add((value, i, j, i, j+1 ))
        return actions

    #Displays the output
    def display_output(self, output_steps,output_states):
        utility = Utility()
        print("The solution can be found in ", len(output_steps), "move(s)")
        step = 1
        for eachEntry in output_steps:
            print("Step ", step, " :: Move ", eachEntry[0], " from (", eachEntry[1], ",", eachEntry[2], ") to (", eachEntry[3],
                  ",", eachEntry[4], ")")

            utility.display(output_states[step - 1])
            step += 1

    #Displays the given state
    def  display(self,state):
        for i in range(1, 4):
            nextLine = 0
            for j in range(1, 4):

                for eachState in state:

                    if eachState[1] == i and eachState[2] == j:
                        nextLine += 1
                        print(eachState[0], "  ", end='')
                        if (nextLine == 3):
                            print(" ")

#Class that executes STRIPS algorithm
class Strips:
    utility = Utility()

    #constructor of Strips class
    def __init__(self, input_state,goal_state):
        self.all_moves = utility.getAllPossibleMoves()  # computing all possible moves
        self.predicate_action_removes = utility.createMoveOperator(
            self.all_moves)  # defining predicate,action and remove
        self.goal_state = goal_state
        self.initial_state = input_state

    #Identifying the best moves given all the possible moves
    def get_best_move(self, possible_moves_from_goal_state):
        max = 0
        indexes = []
        position_of_move = 0
        for eachMove in possible_moves_from_goal_state:
            predicate = self.predicate_action_removes[eachMove]["precondition"] #getting the precondition for the move
            number_of_equal_predicate = len(predicate.intersection(self.initial_state)) #number of common predicates
            if (number_of_equal_predicate >= max):
                if (number_of_equal_predicate > max):
                    indexes = []
                max = number_of_equal_predicate
                indexes.append(position_of_move) #storing the index of the move from the possible_moves_from_goal_state
            position_of_move += 1
        # if more than one move, fetch the first value.Heuristic to choose the best possible move towards initial stae can be given here
        return list(possible_moves_from_goal_state)[indexes[0]]  # casting set to list and fetching the first entry

    #Returns the precondition
    def get_predicate_for_move(self, move):
        return self.predicate_action_removes[move]["precondition"]

    #Updates the goal state based on the given  move
    def get_updated_state(self, required_move):
        utility = Utility()
        new_state = self.goal_state.copy()
        for eachValue in self.goal_state:
            if ((eachValue[1] == required_move[1] and eachValue[2] == required_move[2]) or (
                    eachValue[1] == required_move[3] and eachValue[2] == required_move[4])):
                new_state.remove(eachValue)
        predicates = self.get_predicate_for_move(required_move)
        for predicate in predicates:
            new_state.add(predicate)
       # new_state.add((required_move[0],required_move[1],required_move[2]))
        #new_state.add((0, required_move[3], required_move[4]))
        return new_state

    #This is the main strips implementation
    def execute_strips(self):
        required_move_list = []
        self.output_state = []
        while (len(self.goal_state.intersection(self.initial_state)) < 9):
            possible_moves_from_goal_state = utility.get_possible_moves(self.goal_state) #Fetching all possible moves
            required_move = self.get_best_move(possible_moves_from_goal_state) #Selecting the best possible move
           # print("best moves ", required_move)
            required_move_list.append(required_move)
            #  predicate = self.get_predicate_for_move(required_move)
            self.output_state.append(self.goal_state.copy())
            self.goal_state = self.get_updated_state(required_move)
            if (len(required_move_list) > 10):
                print("Sorry, the number of steps needed to reach the solution is more than 10 !!!")
                print("Terminating program....")
                exit(0)
        required_move_list.reverse()
        self.output_state.reverse()
        return required_move_list,self.output_state


if __name__ == "__main__":
    utility = Utility()
    initial_state,goal_state = utility.read_input_from_user()  # reading input from user through console as string
    initial = utility.split_and_convert_to_integer(initial_state)  # extracting only the numbers and creating the list of input
    goal = utility.split_and_convert_to_integer(goal_state)
    print(input)  # Printing the input state
    input_state = utility.define_position_for_input(initial)  # defining the position fo each input value
    goal_state = utility.define_position_for_input(goal)  # defining the position fo each goal state value
    print("Input state :: ")
    utility.display(input_state) #displaying input state
    print("Goal state :: ")
    utility.display(goal_state) #displaying goal state
    strips_instance = Strips(input_state,goal_state)  # instantiating Strips instance
    output_steps,output_states = strips_instance.execute_strips() #executing STRIPS algorithm
    utility.display_output(output_steps,output_states) #displaying output
