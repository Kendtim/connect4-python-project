import random
def clean(game_map):
    '''
        Function cleans the game desk
    '''
    for i in range(len(game_map)):
        for j in range(len(game_map[i])):
            game_map[i][j] = ' '
    return game_map


# def test_clean():
#     assert [[' '],[' ']] == clean([['*'],['0']])




def show_grid(grid):
    '''
        Function shows the grid
    '''
    print("  1 2 3 4 5 6 7  ") 
    for i in range(6):
        print(6-i, " ".join(grid[i]), 6-i)
    print("  1 2 3 4 5 6 7  ")



def is_possible(column, grid):
    '''
        Function checks is it possible to guess given column or not
    '''
    res = False
    for i in range(len(grid)):
        if grid[i][column-1] == ' ':
            res = True
    return res

# def test_is_possible():
#     assert True == is_possible(2, [[' ', ' '],[' ',' ']])
#     assert True == is_possible(1, [['*', ' '],[' ',' ']])
#     assert False == is_possible(1, [['*', ' '],['*',' ']])




def guess(color, colum, gri):
    '''
    dir_rawopped disks to grid
    '''
    if is_possible(colum, gri):
        for i in range(len(gri)):
            if gri[len(gri)-1-i][colum-1] == ' ':
                gri[len(gri)-1-i][colum-1] = color
                break
    return gri

# def test_guess():
#     assert guess('*', 2, [[' ', ' '],[' ', ' ']]) == [[' ', ' '],[' ', '*']]


def count_aligned_disc(row,col,color,grid):
    '''
        The function calculates the length of the longest line of the given color
        starting from position (row, col) in all directions
    '''
    #directions:horizontal, vertical, diagonals (down right), (down left)
    direction = [(0, 1),(1, 0),(1, 1),(1, -1)] 
    max_length = 1  #maximum length of aligned disks

    for dir_raw, dir_col in direction:
        length = 1  #current length
        
        #checking in the forward direction
        r, c = row+dir_raw, col+dir_col 
        while (0<=r<len(grid)) and (0<=c<len(grid[0])) and grid[r][c] == color:
            length+= 1 
            r=r+dir_raw
            c=c+dir_col

        #checking in the opposite direction
        r, c = row-dir_raw, col-dir_col
        while (0<=r <len(grid)) and (0<=c <len(grid[0])) and grid[r][c] == color:
            length+= 1
            r=r-dir_raw
            c=c-dir_col

        #change the maximum length
        max_length = max(max_length,length)

    return max_length



# def test_count_aligned_disc():
#     grid = [
#         ['*', '*', '*', 'O'],
#         ['O', 'O', '*', 'O'],
#         ['O', '*', 'O', 'O']
#     ]

#     assert count_aligned_disc(0, 1, '*', grid) == 3 #Correct

    
# test_count_aligned_disc()





def recommend_random_column(grid):
    '''
       The function randomly selects a column where you can dir_rawop the disc
    '''
    #find all free columns 
    possible_columns = [] 
    for col in range(len(grid[0])):  #Loop through all column indices 
        if is_possible(col+1,grid): # Check if it is possible to throw a disk into this column # col+1 because it starts counting from 0 (but it should be 1) 
            possible_columns.append(col + 1) 

    #If there are possible columns, we select a random one
    if len(possible_columns) > 0:
        return random.choice(possible_columns)
    else:
        return None 
    
# def test_recommend_random_column():
#     grid=[
#         ['*', '*', '*', '*'],
#         ['O', '*', 'O', 'O'],
#         ['O', '*', 'O', 'O']  ]

#     assert recommend_random_column(grid) in [1, 2, 3, 4]  #Correct

#     grid2 = [
#         ['O', 'O', 'O', 'O'],
#         ['O', 'O', 'O', 'O'],
#         ['O', 'O', 'O', 'O']  ]

#     assert recommend_random_column(grid2) is not None  #Error(must be None)
    
# test_recommend_random_column()




def improve_advice(grid,color):
    '''
        Recommends column for throwing:
        Selects the column leading to a win or maximum length,if there are no options, select  random column
    '''
    max_alignment=0    #create max length 
    best_column=None   #and best column are empty 
    
    for col in range(len(grid[0])): #skipping impossible columns
        if not is_possible(col + 1, grid): 
            continue  

        #make copy of the playing field for testing 
        test_grid = []  
        for row in grid:  
            test_grid.append(list(row))#add copy of row

        guess(color, col + 1, test_grid) #Throw disk into the test field
    
        #check  length of line in the test field
        for row in range(len(test_grid)):
            if test_grid[row][col] == color:  
                alignment = count_aligned_disc(row, col, color, test_grid)
                if alignment > max_alignment:
                    max_alignment = alignment
                    best_column = col + 1

    #if we found a column for winning or maximum line,return it
    if best_column is not None:
        return best_column
    #if nothing is found,return a random column
    else:
        return recommend_random_column(grid)
    
# def test_improve_advice():
#     grid=[
#         ['*', '*', '*', 'O'],
#         ['O', 'O', '*', 'O'],
#         ['O', '*', 'O', 'O']
#     ]

#     assert improve_advice(grid,'*')==3  #Correct

#     grid2 = [
#         ['O', 'O', 'O', 'O'],
#         ['O', 'O', 'O', 'O'],
#         ['O', 'O', 'O', 'O']
#     ]

#     assert improve_advice(grid2,'*') is not None  #Error(grid is full,should be None)
    
# test_improve_advice()


def check_winner(grid, color):
    '''
    Checks if there is a line of 4 or more discs of the given color on the grid
    '''
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == color:
                if count_aligned_disc(row, col, color, grid) >= 4:
                    return True
    return False

def play_game():
    '''
    Function to play Connect 4 between a human and the computer
    '''
    c_map = [[' ' for _ in range(7)] for _ in range(6)]  #create 6x7 field
    clean(c_map)  #clean field
    yellow_disk = 'o'  # player color
    red_disk = '*'  #computer color 

    print("Welcome to the Connect 4")
    show_grid(c_map)

    while True:#player play
        while True: 
            user_col = int(input("Your turn (1-7): ")) 
            if 1 <= user_col <= 7 and is_possible(user_col, c_map):
                break
            else:
                print("Invalid number.Try again")
        
        guess(yellow_disk, user_col, c_map)
        show_grid(c_map) #it show the grid 
        
        if check_winner(c_map, yellow_disk):  #player win's check
            print("You win! :)")
            break
        
        if not any(' ' in row for row in c_map):  #checking for dir_rawaw
            print("It's a dir_rawaw!")
            break
        
        #Computer play
        print("Computer play")
        computer_col = improve_advice(c_map, red_disk)
        guess(red_disk, computer_col, c_map)
        show_grid(c_map)
        
        if check_winner(c_map, red_disk):  #computer win's check
            print("Computer wins :(")
            break

        if not any(' ' in row for row in c_map):  #cheching for dir_rawaw
            print("It's a dir_rawaw!")
            break


play_game()




