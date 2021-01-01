import random
import math

# generate board
def generate_board(n):
    board=[[0 for i in range(n)] for j in range(n)]
    # place each queen randomly in each column of board
    for i in range(n):
        q_Initial=random.randrange(0,n,1)
        board[q_Initial][i]=1
    return board

# to print a board configuration
def print_board(msg,board):
    print(msg)
    for i in range(n):
        print("\n", board[i])

# to get the positions of queens from the current configuration
def get_Queen_Position(board,n,i):
    for j in range(n):
        if board[j][i]==1:
            return j

# to calculate the heuristic value of a particular configuration
def calc_heuristic(board,n):
    heuristic=0
    for i in range(n):
        x_base=get_Queen_Position(board,n,i)
        y_base=i
        for j in range(n):
            if j==i:
                continue
            else:
                x_pair=get_Queen_Position(board,n,j)
                y_pair=j
                if x_base==x_pair or abs(x_base-x_pair)== abs(y_base-y_pair):
                   heuristic+=1
    return int((heuristic)/2)

# to calculate the heuristic value of all n*(n-1) possible configurations reachable from the current configuration - returns a 2D-array with heuristic costs in each cell
def find_all_heuristics(board,n):
    heuristic_all=[[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        x_base=get_Queen_Position(board,n,i)
        y_base=i
        for j in range(n):
            temp_board=[row[ : ] for row in board]
            if j==x_base:
                heuristic_all[j][i]=math.inf
            else:
                temp_board[j][i]=1
                temp_board[x_base][y_base]=0
                heuristic_all[j][i]=calc_heuristic(temp_board, n)
    return heuristic_all

# to find the minimum heuristic move to make to go the next board configuartion
def find_minimum_heuristic_move(board, n):
    heuristic_all=find_all_heuristics(board,n)
    min_heuristic=math.inf
    x_min=0
    y_min=0
    rand_arr = [] #to store the indices of minimum heuristic valued configurations : 1st index is row no. and 2nd index is column no.
    mymin = min([min(r) for r in heuristic_all])
    for i in range(n):
        for j in range(n):
            if heuristic_all[j][i] == mymin:
                min_heuristic = heuristic_all[j][i]
                rand_arr.append([j, i])
    min_index = random.randint(0,len(rand_arr)-1)
    x_min = rand_arr[min_index][0]
    y_min = rand_arr[min_index][1]
    return(x_min,y_min,min_heuristic)

# Approach 1 - traditional hill climbing            
def hill_climbing(heuristic_current,min_heuristic):
    if heuristic_current > min_heuristic:
        return True
    return False

# Approach 2 - hill climbing with sideways move, the limit set on the number of consecutive sideways move is 100
def hill_climbing_sideways(heuristic_current,min_heuristic):
    global counter
    if heuristic_current == min_heuristic:
        counter = counter + 1
    else:
        counter = 0
    if heuristic_current >= min_heuristic and counter < counter_value:
        return True
    return False

no_of_instances = 100
rand_print_counter = 0
rand_print = [random.randint(0,no_of_instances) for ii in range (4)]
rand_print.sort()
if __name__ == "__main__":
    success_rate = 0 #number of successful instances, not percentage
    steps_success = 0
    steps_failure = 0
    no_of_rand_restart = 0
    n = int(input("Enter the value of N : "))
    m = int(input("Enter the variant of hill climibing search to use:\n1 = hill climbing classic; 2 = hill climbing with sideways moves; 3 = random restart without sideways moves; 4 = random restart with sideways moves\n"))
    for k in range(no_of_instances):
        counter = 0
        if(m == 2):
            counter_value = 100 # limit on consecutive sideways move for hill climbing
        else:
            counter_value = 10 # limit on consecutive sideways move for random restart hill climbing
        board=generate_board(n)
        heuristic_all=[[0 for i in range(n)] for j in range(n)]
        heuristic_current=calc_heuristic(board, n)
        if ((m == 1 or m == 2) and rand_print_counter < 4 and k == rand_print[rand_print_counter]):
            print("\nRandom instance :", rand_print_counter+1)
            print_board("\nInitial state ",board)
        min_heuristic=math.inf
        success_local = 0
        failure_local = 0
        no_of_rand_restart_local = 0
        while heuristic_current>0:
            x_min,y_min,min_heuristic = find_minimum_heuristic_move(board, n)      
            if (m == 1 and hill_climbing(heuristic_current,min_heuristic) == True): # approach 1 - do not change any hard coded numbers
                x_temp=get_Queen_Position(board,n,y_min)
                board[x_temp][y_min]=0
                board[x_min][y_min]=1
                heuristic_current=min_heuristic
                success_local = success_local + 1
                if (rand_print_counter < 4 and k == rand_print[rand_print_counter]):
                    print_board("\nNext state ",board)
                if heuristic_current==0:
                    success_rate+=1
                    if (rand_print_counter < 4 and k == rand_print[rand_print_counter]):
                        print("\nThis was a successful instance.")
                        print("----------------------------------------------------------")
    
            elif (m == 2 and hill_climbing_sideways(heuristic_current,min_heuristic) == True): # approach 2 - do not change any hard coded numbers
                x_temp=get_Queen_Position(board,n,y_min)
                board[x_temp][y_min]=0
                board[x_min][y_min]=1
                heuristic_current=min_heuristic
                success_local = success_local + 1
                if (rand_print_counter < 4 and k == rand_print[rand_print_counter]):
                    print_board("\nNext state ",board)
                if heuristic_current==0:
                    success_rate+=1
                    if (rand_print_counter < 4 and k == rand_print[rand_print_counter]):
                        print("\nThis was a successful instance.")
                        print("----------------------------------------------------------")

            elif (m == 3 and k < 50): #approach 3 - do not change any hard coded numbers
                if(hill_climbing(heuristic_current,min_heuristic) == True):
                    x_temp=get_Queen_Position(board,n,y_min)
                    board[x_temp][y_min]=0
                    board[x_min][y_min]=1
                    heuristic_current=calc_heuristic(board, n)
                    success_local += 1
                    if heuristic_current==0:
                        break
                else:
                    no_of_rand_restart_local = no_of_rand_restart_local + 1   
                    board = generate_board(n)
                    heuristic_current=calc_heuristic(board, n)
                            
            elif (m == 4 and k < 50): # approach 4 - do not change any hard coded numbers
                if(hill_climbing_sideways(heuristic_current,min_heuristic) == True):
                    x_temp=get_Queen_Position(board,n,y_min)
                    board[x_temp][y_min]=0
                    board[x_min][y_min]=1
                    heuristic_current=calc_heuristic(board, n)
                    success_local += 1
                    if heuristic_current==0:
                        break
                else:
                    no_of_rand_restart_local = no_of_rand_restart_local + 1    
                    board = generate_board(n)
                    heuristic_current = calc_heuristic(board, n)
                    
            else:
                failure_local = success_local
                if ((m == 1 or m == 2) and rand_print_counter < 4 and k == rand_print[rand_print_counter]):
                    print("\nThis was a failure instance.")
                    print("----------------------------------------------------------")
                success_local = 0
                break
            
        steps_success += success_local
        steps_failure += failure_local
        no_of_rand_restart += no_of_rand_restart_local
        if ((m == 1 or m == 2) and rand_print_counter < 4 and k == rand_print[rand_print_counter]):
            rand_print_counter = rand_print_counter + 1
    if m == 1 or m == 2:
        print("\n\nSuccess rate is : ", (success_rate*100)/no_of_instances, "%")
        print("\nFailure rate is :", ((no_of_instances - success_rate)*100)/no_of_instances, "%")
        if success_rate != 0:
            print('\nAverage No. of steps required for success is ', round(steps_success/success_rate,2), 'which is approximately', math.ceil(steps_success/success_rate),'steps.')
        if success_rate != no_of_instances:
            print("\nAverage No. of steps required for failure is ",round(steps_failure/(no_of_instances - success_rate),2), 'which is approximately',math.ceil(steps_failure/(no_of_instances - success_rate)),'steps.')
    if m == 3 or m == 4:
        print("\nNumber of random restarts required is ", no_of_rand_restart/50, 'which is approximately',math.ceil(no_of_rand_restart/50), 'restarts.')
        print('\nAverage No. of steps required for random restart is ',steps_success/50, 'which is approximately',math.ceil(steps_success/50),'steps.')