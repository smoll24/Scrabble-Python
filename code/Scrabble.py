#import enchant
import random
import importlib

#Import enchant if available
enchant = None
try:
    enchant = importlib.import_module('enchant')
except:
    print("Cannot find 'enchant' module. Wordchecker is not available.")

#DEFINITION DES VARIABLES ------------------------------------------------------------

#Dictionaries with ANSI color escape codes
couleur = {"bg_noir":'\u001b[40m',"bg_rouge":"\u001b[41m","bg_jaune":"\u001b[43m","bg_vert":"\u001b[42m",'bg_blanc':'\u001b[47m',"bg_magenta":"\u001b[45m","bg_cyan":"\u001b[46m","bg_bleu":"\u001b[44m",
           'txt_noir':'\u001b[30m',"txt_blanc":"\u001b[37m","clear":"\033[0m"}
couleurs_loc= {"m2":couleur['bg_magenta'],"m3":couleur['bg_rouge'],"l2":couleur['bg_cyan'],"l3":couleur['bg_bleu']}

current_round = 0
current_player = 0

#Initialise board with colors
board = [['  ' for i in range(15)] for i in range(15)]

jetons_pts = {"A":1,"B":3,"C":3,"D":2,"E":1,"F":4,"G":2,"H":4, "I":1, 
              "J":8,"K":10,"L":1,"M":2,"N":1,"O":1,"P":3,"Q":8,"R":1, 
              "S":1,"T":1,"U":1,"V":4,"W":10,"X":10,"Y":10,"Z":10, 
              "joker":0}

jetons_nbre = {"A":9,"B":2,"C":2,"D":3,"E":15,"F":2,"G":2,"H":2,"I":8,"J":1, 
               "K":1,"L":5,"M":3,"N":6,"O":6,"P":2,"Q":1,"R":6,"S":6,"T":6, 
               "U":6,"V":2,"W":1,"X":1,"Y":1,"Z":1, "joker":2} 

plateau = {(0,0):('m',3), (0,7):('m',3), (0,14):('m',3), (7,0):('m',3), 
           (7,7):('m',3), (7,14):('m',3), (14,0):('m',3), (14,7):('m',3), 
           (14,14):('m',3), 
           (1,1):('m',2), (1,13):('m',2), (2,2):('m',2), (2,12):('m',2), 
           (3,3):('m',2), (3,11):('m',2), (4,4):('m',2), (4,10):('m',2), 
           (7,7):('m',2), (10,4):('m',2), (10,10):('m',2), (11,3):('m',2), 
           (11,11):('m',2), (12,2):('m',2), (12,12):('m',2), (13,1):('m',2), 
           (13,13):('m',2), 
           (1,5):('l',3), (1,9):('l',3), (5,1):('l',3), (5,5):('l',3), 
           (5,9):('l',3), (5,13):('l',3), (9,1):('l',3), (9,5):('l',3), 
           (9,9):('l',3), (9,13):('l',3), (13,5):('l',3), (13,9):('l',3), 
           (0,3):('l',2), (0,11):('l',2), (2,6):('l',2), (2,8):('l',2), 
           (3,0):('l',2), (3,7):('l',2), (3,14):('l',2), (6,2):('l',2), 
           (6,6):('l',2), (6,8):('l',2), (6,12):('l',2), (7,3):('l',2), 
           (7,11):('l',2), (8,2):('l',2), (8,6):('l',2), (8,8):('l',2), 
           (8,12):('l',2), (11,0):('l',2), (11,7):('l',2), (11,14):('l',2), 
           (12,6):('l',2), (12,8):('l',2), (14,3):('l',2), (14,11):('l',2)}

title = [' .d8888b.   .d8888b.  8888888b.         d8888 888888b.   888888b.   888      8888888888 ',
         'd88P  Y88b d88P  Y88b 888   Y88b       d88888 888  "88b  888  "88b  888      888       ',
         'Y88b.      888    888 888    888      d88P888 888  .88P  888  .88P  888      888 ',
         ' "Y888b.   888        888   d88P     d88P 888 8888888K.  8888888K.  888      8888888   ',
         '    "Y88b. 888        8888888P"     d88P  888 888  "Y88b 888  "Y88b 888      888    ',
         '      "888 888    888 888 T88b     d88P   888 888    888 888    888 888      888  ',
         'Y88b  d88P Y88b  d88P 888  T88b   d8888888888 888   d88P 888   d88P 888      888       ',
         ' "Y8888P"   "Y8888P"  888   T88b d88P     888 8888888P"  8888888P"  88888888 8888888888']

#creat bag which we will pull from to get letters
bag = []
for let, nb in jetons_nbre.items():
    for i in range(nb):
        bag.append(let)
        
jetons_joueurs = {}

#DEFINITION DES FONCTIONS ---------------------------------------------------------------

def initialise_board():
    '''Adds the multipleir squares onto the board'''
    #add in multiplier squares and colors
    for cord, value in plateau.items():
        i, j = cord
        val = value[0]+str(value[1])
        board[i][j] = val

def initialise_letters():
    '''Randomly distributes jetons for the start'''
    for player in range(len(score_board[0])):
        temp_jetons = []
        for i in range(7):
            #Picks a random jetons from the bag
            jeton_rnd = random.choice(bag)
            temp_jetons.append(jeton_rnd)
            bag.remove(jeton_rnd)
        jetons_joueurs[player] = temp_jetons
    
def mot_valide(mot):
    '''Check if a word is valid for Scrabble
    Input: mot - string of letters
    Returns: bool'''
    if len(mot) < 2:
        return False
    
#     try:
#         french_dict = enchant.Dict("fr")
#         if not french_dict.check(mot):
#             return False
#     except:
#         print('No spellcheck')
        
    return True
    
def title_screen():
    '''Initialises the game and displays the title'''
    global num_players, score_board
    for line in title:
        print(line)
    print(('\n')*2)
    begin = input((' ')*35+'Begin? ')
    print(('\n')*2)
        
    #Gets number of players
    num_players = 0
    while num_players < 1:
        try:
            num_players = int(input('How many players? '))
        except:
            print("I'm sorry, that is not a valid number of players.")
            
    #Initializes the score board with the correct number of rows and columns
    score_board = [['0' for i in range(num_players)] for i in range(2)]
    
    #Adds player names to the first row
    for i in range(num_players):
        score_board[0][i] = input('Name of Player '+str(i+1)+'? ')
    print(('\n')*2)

def color_elt(elt):
    '''Adds color to a board element
    Input: elt - string
    Returns: new_elt - string'''
    new_elt = ''
    
    if elt.isspace(): #backgroung
        new_elt = new_elt= couleur['bg_noir']+elt+couleur['clear']
    elif elt.islower(): #multipliers
        new_elt = couleur['txt_blanc']+couleurs_loc[elt]+elt+couleur['clear']
    elif elt.isupper():
        new_elt = couleur['txt_noir']+couleur['bg_blanc']+elt+couleur['clear']
    return new_elt
        

def print_board():
    '''Prints out the board'''
    print('  ',end='')
    for i in range(15):
        print(' '+chr(i+97), end = '')
    print()
    for i,row in enumerate(board):
        print(str(i+1).rjust(2), end = '')
        for element in row:
            print(color_elt(element), end='')
        print()

def print_score():
    '''Prints the score and scoreboard'''
    print()
    #Finds the length that the score board will be
    len_row = 0
    temp_len = 0

    #Checks len of first row
    for i in range(len(score_board[0])):
        len_row += len(score_board[0][i])
        
    #Checks len of second row
    for i in range(len(score_board[1])):
        temp_len += len(score_board[1][i])
        
    #If seecond row is bigget takes second row length
    if temp_len > len_row:
        len_row = temp_len

    len_row += (len(score_board[0])*3)
    line = (('+')+('-')*(len_row-1)+('+'))

    #Finds length on each column
    len_columns = [' ' for i in range(num_players)]
    temp_row0 = 0
    temp_row1 = 0
    for i in range(len(score_board[0])):
        temp_row0 = len(score_board[0][i])
        temp_row1 = len(score_board[1][i])
        if temp_row0 > temp_row1:
            len_columns[i] = temp_row0+1
        else:
            len_columns[i] = temp_row1+1
                
    #Prints the score board
    print('SCOREBOARD')
    print(line)
    for i in range(len(score_board)):
        for j in range(len(score_board[0])):
            el = ('| '+str(score_board[i][j])+' '*(len_columns[j]-len(score_board[i][j])))
            print(el, end="")
        print('|')
        print(line)
    print()

def score(word_table):
    total = 0
    for cord,let in word_table.items(): #score letters
        num = jetons_pts[let]
        if cord in plateau and plateau[cord][0] == 'l':
            num *= plateau[cord][1]
        total = total + num
        
    for cord in word_table.keys(): #word multipliers
        if cord in plateau and plateau[cord][0] == 'm':
            total *= plateau[cord][1]
            
    if len(word_table) >= 7: #using all 7 tiles bonus
        print('BINGO!')
        total += 50
    
    return total

def print_letters():
    '''Prints out the player's letters and letter count in bag'''
    
    #Distributes random letters for players
    if len(jetons_joueurs[current_player-1]) < 7:
        for i in range(7-len(jetons_joueurs[current_player-1])):
            #Picks a random jetons from the bag
            jeton_rnd = random.choice(bag)
            jetons_joueurs[current_player-1].append(jeton_rnd)
            bag.remove(jeton_rnd)
    
    print('There are',len(bag),'letters left in the bag.\n')

    
    print("LETTRES DE PLAYER",current_player)
    print(jetons_joueurs[current_player-1])

def place_let(let, cord):
    '''Places a letter on the board
    Input: let - single chr string that isalpha
           cord - tuple countaining two ints (x,y)'''
    x = cord[0]
    y = cord[1]
    board[y][x] = let.upper()+' '

def get_word_table(word, cord, direct):
    '''Creates a dict of all the letter's cordinates in a word
    Input: let - single chr string that isalpha
           cord - tuple countaining two ints (x,y)
           direct - bool True is right and False is down
    Returns: word_table - dict of tuple:string '''
    word_table = {}
    x = cord[0]
    y = cord[1]
    
    for i in range(len(word)):
        word_table[x,y] = word[i]
        
        if direct:
            x += 1
        else:
            y += 1
            
    return word_table

def place_word(word, cord, direct):
    word_table = get_word_table(word, cord, direct)
    for cord, let in word_table.items():
        place_let(let,cord)

def test_word(word,cord,direct):
    word_table = get_word_table(word,cord,direct)
    valide = True
    
    #test location and creat new_table containing all the required jetons
    new_table = {}
    for cord,let in word_table.items():
        x = cord[0]
        y = cord[1]
        if board[y][x][0].isupper(): #if it is a jeton
            if board[y][x][0] != let: #[0] cuz only the letter
                valide = False
        else:
            new_table[(x,y)] = let
    
    #check that they have the jetons --DOESN"T FULLY WORK YET IN PROGRESS
    check = all(item in jetons_joueurs[current_player-1] for item in new_table.values())
    if not check:
        return False
    
    #preview board
    print('  ',end='')
    for i in range(15):
        print(' '+chr(i+97), end = '')
    print()
    for y,row in enumerate(board):
        print(str(y+1).rjust(2), end = '')
        for x,elt in enumerate(row):
            if (x,y) in word_table:
                let = word_table[(x,y)]
                if elt[0].isupper(): #if it is a jeton
                    if elt[0] == let:
                        print(couleur['txt_noir']+couleur['bg_vert']+let+' '+couleur['clear'], end='')
                    else:
                        print(couleur['txt_blanc']+couleur['bg_rouge']+'XX'+couleur['clear'], end='')
                else:
                    print(couleur['txt_noir']+couleur['bg_jaune']+let+' '+couleur['clear'], end='')
            else:
                print(color_elt(elt), end='')
        print()
    
    #Calculate points
    if valide:
        pts = score(word_table)
        print('This move gets you',pts,'points.')
    
    return valide


def user_input():
    print()
    while True:
        mot = input("Saissisez un mot que vous aimerez placer sur le plateau: ")
        if mot.isalpha() and mot_valide(mot): #checks if the letter is not part of the alphabet
            break
    
    while True:
        range_num = range(1,16) #range of numbers from 1 to 15(since 16 is excluded)
        range_letters='abcdefghijklmno'
        location = input("Saissisez un coordonné pour la premiere lettre de votre mot (ex: a1): ")
        if len(location)<=3: 
            if range_letters.find(location[0])!=-1 and int(location[1:]) in range_num:
                break
    while True:
        orientation = input("Saissisez une orientation right/down pour votre mot: ")
        if orientation == 'right' or orientation=='down':
            break
    
    word = mot.upper()
    cord = (range_letters.find(location[0]),int(location[1])-1)
    direct = True if orientation == 'right' else False
    return word,cord,direct

def print_round():
    print()
    global current_round, current_player, score_board
    current_round += 1
    current_player = (current_player % len(score_board[0]))+1
    print("ROUND",current_round,"- PLAYER",current_player,"\n")

def test_game():
    while True:
        print_round()
        print_board()
        print_score()
        print_letters() 
        
        while True:
            word,cord,direct = user_input()
            if test_word(word,cord,direct):
                break
        ans = input('Would you like to place the word (y,n): ')
        if ans == 'y':
            place_word(word,cord,direct)

#PROGRAMME ------------------------------------------------------------------------------
    
title_screen()

initialise_board()

print_round()
initialise_letters()
print_board()
print_score()
print_letters()
