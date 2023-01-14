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
couleur = {"bg_noir":'\u001b[40m',"bg_rouge":"\u001b[41m",'bg_blanc':'\u001b[47m','txt_noir':'\u001b[30m',"bg_magenta":"\u001b[45m","bg_cyan":"\u001b[46m","bg_bleu":"\u001b[44m","txt_blanc":"\u001b[37m","clear":"\033[0m"}
couleurs_loc= {"m2":couleur['bg_magenta'],"m3":couleur['bg_rouge'],"l2":couleur['bg_cyan'],"l3":couleur['bg_bleu']}

#Initialise board with colors
board = [[couleur['bg_noir']+'  '+couleur['clear'] for i in range(15)] for i in range(15)]

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

jetons_p1 = []

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

#DEFINITION DES FONCTIONS ---------------------------------------------------------------

def mot_valide(mot):
    
    if len(mot) < 2:
        return False
    
    try:
        french_dict = enchant.Dict("fr")
        if not french_dict.check(mot):
            return False
    except:
        print('Error with spellcheck')
        
    return True
    
def initialise_jetons():
    for i in range(7):
        #Vérifie que le nombre de jetons de la lettre choisie est plus grand que 0
        jeton_rnd = random.choice(bag)#[i for i, j in jetons_nbre.items() if j > 0])
        jetons_p1.append(jeton_rnd)
        #jetons_nbre[jeton_rnd] -= 1
        bag.remove(jeton_rnd)

def initialise_board():
    #add in multiplier squares and colors
    for cord, value in plateau.items():
        i, j = cord
        val = value[0]+str(value[1])
        board[i][j] = couleur['txt_blanc']+couleurs_loc[str(val)]+val+couleur['clear']

def place_let(let,cord):
    x = cord[0]
    y = cord[1]
    board[y][x] = couleur['txt_noir']+couleur['bg_blanc']+let.upper()+' '+couleur['clear']

def print_board():
    print('  ',end='')
    for i in range(15):
        print(' '+chr(i+97), end = '')
    print()
    for i,row in enumerate(board):
        print(str(i+1).rjust(2), end = '')
        for element in row:
            print(element, end='')
        print()
    print()
    print('There are',len(bag),'letters left in the bag.')
    
def title_screen():
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
    
def print_score():
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
    line = (('+')+('-')*(len_row)+('+'))

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

#PROGRAMME ------------------------------------------------------------------------------
    
title_screen()

initialise_jetons()
initialise_board()

print("ROUND 1 - PLAYER 1\n")
print_board()
print_score()
print("LETTERS")
print(jetons_p1)
