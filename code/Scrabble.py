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

board = [["\u001b[40m[]\033[0m" for i in range(15)] for i in range(15)]

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

couleurs = {"m2":"\u001b[45m","m3":"\u001b[41m","l2":"\u001b[46m","l3":"\u001b[44m"}
jetons_p1 = []

#creat bag which we will pull from to get letters
bag = []
for let, nb in jetons_nbre.items():
    for i in range(nb):
        bag.append(let)

#DEFINITION DES FONCTIONS ---------------------------------------------------------------

def mot_valide(mot):
    try:
        french_dict = enchant.Dict("fr")
        return french_dict.check(mot)
    except:
        print('Error with spellcheck')
    
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
        board[i][j] = couleurs[str(val)]+val+"\033[0m"

def print_board():
    for row in board:
        for element in row:
            print(element, end='')
        print()

#PROGRAMME ------------------------------------------------------------------------------
        
initialise_board()
print_board()

initialise_jetons()
print(jetons_p1)
