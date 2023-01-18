import random

# Read in the French Scrabble word list from a file
word_list_path = 'french_scrabble_words2.txt'
scrabble_words = None
try:
    with open(word_list_path, 'r',encoding="utf-8") as f:
        scrabble_words = f.read().splitlines()
except:
    print("Cannot find",word_list_path,"Wordchecker is not available.\n")

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
    
    mot = mot.lower()
    
    if len(mot) < 2:
        print('Word must be longer than 2 letters.')
        return False
    
    if scrabble_words and mot not in scrabble_words:
        print('Word not a valid scrabble word.')
        return False
        
    return True

def title_screen():
    '''Initialises the game and displays the title'''
    global num_players, score_board, scrabble_words
    
    for line in title:
        print(line)
    print(('\n')*2)
    
    #Ask if they want the wordchecker
    if not scrabble_words:
        print("Cannot find",word_list_path,"Wordchecker is not available.\n")
    else:
        ans = input('Would you like to use wordchecker (y/n): ')
        if ans == 'n':
            scrabble_words = None
    
    #begin = input((' ')*35+'Begin? ')
    print(('\n')*2)
        
    #Gets number of players
    num_players = 0
    while num_players < 2:
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

def score(word_table,n_letters):
    total = 0
    for cord,let in word_table.items(): #score letters
        num = jetons_pts[let]
        x,y = cord
        if not board[y][x][0].isupper(): #if there is already a jeton don't use the multiplier.
            if cord in plateau and plateau[cord][0] == 'l':
                num *= plateau[cord][1]
        total = total + num
        
    for cord in word_table.keys(): #word multipliers
        x,y = cord
        if not board[y][x][0].isupper(): #if there is already a jeton don't use the multiplier.
            if cord in plateau and plateau[cord][0] == 'm':
                total *= plateau[cord][1]
            
    if n_letters >=7: #using all 7 tiles bonus
        print('BINGO!')
        total += 50
    
    return total

def get_power(num):
    if num == 1:
        c = chr(0x00b9)
    elif 2 <= num <= 3:
        c = chr(0x00b0 + num)
    elif num == 10:
        c = chr(0x00b9)+chr(0x2070)
    else:
        c = chr(0x2070 + num)
    return c

def print_letters():
    '''Prints out the player's letters and letter count in bag'''
    
    print('There are',len(bag),'letters left in the bag.\n')

    print_letters = []
    for let in jetons_joueurs[current_player-1]:
        c = get_power(jetons_pts.get(let))
        print_letters.append(let+c)
    
    print("LETTRES DE PLAYER",current_player)
    print(*print_letters)
    
def distrib_letters():
    global bag, jetons_joueurs
    #Distributes random letters for players
    if len(bag) > 0:
        if len(jetons_joueurs[current_player-1]) < 7:
            for i in range(7-len(jetons_joueurs[current_player-1])):
                #Picks a random jetons from the bag
                jeton_rnd = random.choice(bag)
                jetons_joueurs[current_player-1].append(jeton_rnd)
                bag.remove(jeton_rnd)

def place_let(let, cord):
    '''Places a letter on the board
    Input: let - single chr string that isalpha
           cord - tuple countaining two ints (x,y)'''
    x,y = cord
    c = get_power(jetons_pts.get(let))
    board[y][x] = let.upper()+c

def get_word_table(word, cord, direct):
    '''Creates a dict of all the letter's cordinates in a word
    Input: let - single chr string that isalpha
           cord - tuple countaining two ints (x,y)
           direct - bool True is right and False is down
    Returns: word_table - dict of tuple:string '''
    word_table = {}
    x,y = cord
    length = len(word)
    
    valide = True
    
    if direct == True: #horizontal
        if board[y][x-1][0].isupper():
            valide = False
        elif board[y][x+length][0].isupper():
            valide = False
    else:
        if board[y-1][x][0].isupper():
            valide = False
        elif board[y+length][x][0].isupper():
            valide = False
    
    if not valide:
        print('Please spell out the full word!')
        return False
    
    for i in range(length):
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

def has_letters(letters):
    '''Tests if the current player has the required letters
    Input: letters - iterable of strings
    Returns: bool'''
    global jetons_joueurs
    
    #we don't want to effect the actual player's hand until we know they can play the move
    current_jetons = jetons_joueurs[current_player-1].copy()
    
    for let in letters:
        if let in current_jetons:
            current_jetons.remove(let)
        else:
            print('You do not have the letters for this move.')
            return False
    return True

def remove_letters(letters):
    '''Removes letters from the player's hand
    Input: letters - iterable of strings'''
    global jetons_joueurs
    
    for let in letters:
        jetons_joueurs[current_player-1].remove(let)
    print('You used',*letters)

def preview_board(word_table):
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

def test_word(word,cord,direct):
    word_table = get_word_table(word,cord,direct)
    if not word_table:
        return False
    
    valide = True
    off_board = False
    connected = False
    
    #test location and create new_table containing all the required jetons
    #also check that there is at least 1 connection
    new_table = {}
    for cord,let in word_table.items():
        x,y = cord
        
        if x < 0 or x > 14: #Check that letter is on the board
            off_board = True
        elif y < 0 or y > 14:
            off_board = True
        else:
            if board[y][x][0].isupper(): #if it is a jeton
                if board[y][x][0] != let: #[0] cuz only the letter
                    valide = False
                else:
                    connected = True
            else:
                new_table[(x,y)] = let
    
    #check that they have the jetons
    check = has_letters(new_table.values())
    if not check:
        return False
    
    #preview board
    preview_board(word_table)
    
    if not connected:
        valide = False
        print('The word is not connected to any other.')
    
    if off_board:
        valide = False
        print("The word doesn't fit on the board.")
    
    #Calculate points
    if valide:
        pts = score(word_table,len(new_table.values()))
        print('This move gets you',pts,'points.')
    
        ans = input('Would you like to place the word (y/n): ')
        if ans == 'y':
          remove_letters(new_table.values())
        else:
            valide = False
    
    return valide


def user_input():
    print()
    while True:
        try:
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
        except:
            print('Invalide input.')
            continue
        else:
            word = mot.upper()
            cord = (range_letters.find(location[0]),int(location[1:])-1)
            direct = True if orientation == 'right' else False
            
            return word,cord,direct

def print_round():
    print()
    global current_round, current_player, score_board
    current_round += 1
    current_player = (current_player % len(score_board[0]))+1
    print("ROUND",current_round,"- PLAYER",current_player,"|",score_board[0][current_player-1],"\n")

def first_move():
    print_round()
    print_board()
    print_score()
    print_letters()
    
    while True: #input loop
        w,c,d = user_input()
        
        in_center = False
        if has_letters(w):
            word_table = get_word_table(w,c,d)
            if not word_table:
                continue
            
            for cord in word_table.keys():
                if cord == (7,7):
                    in_center = True
            preview_board(word_table)
            
            if not in_center:
                print("Please place the first word in the center of the board (h8)")
            else:
                pts = score(word_table,len(w))
                print('This move gets you',pts,'points.')
            
                ans = input('Would you like to place the word (y/n): ')
                if ans == 'y':
                    remove_letters(w)
                    place_word(w,c,d)
                    break
    distrib_letters()

def game():
    first_move()
    
    while True: #game loop
        print_round()
        print_board()
        print_score()
        print_letters() 
        
        while True: #input loop
            w,c,d = user_input()
            if test_word(w,c,d): #if the move is correct and they want to place it
                place_word(w,c,d)
                break
        distrib_letters()


def final_scores():
    '''Function called if both players skip their turn and they answer 'yes' to stopping game'''
    #Makes a new list with the scores in the form of ints
    scores = [int(x) for x in score_board[1]]
    
    #Subtracts the amount of letters the players have left from their scores
    for i in range(len(score_board[0])):
        #If a player has used all of their letters, the sum of the other players' unplayed letters is added to that player's score
        if len(jetons_joueurs[i]) == 0:
            for j in range(len(jetons_joueurs)):
                if i != j:
                    scores[i] += len(jetons_joueurs[j])
            else:
                if scores[i] > 0:
                    scores[i] -= len(jetons_joueurs[i])
    
    #Puts the new scores back into the board and prints them
    for i in range(len(score_board[0])):
        score_board[1][i] = str(scores[i])
    print('GAME OVER!')
    print('The final scores are:')
    print_score()
    
    #Finds the best score and if there is a tie
    best_score = max(scores)
    best_count = scores.count(best_score)
    
    #If there is a tie, find and print the winners
    if best_count > 1:
        winners = []
        for i,score in enumerate(score_board[1]):
            if int(score) == best_score:
                winners.append(score_board[0][i])
                
        winners[-1] = 'and '+str(winners[-1])
        print('The game is tied. The winners are '+(", ".join(str(x) for x in winners))+'!')
    
    #If there is no tie, print the winner
    else:
        winner = score_board[0][scores.index(best_score)]
        print('The winner is '+winner+'!')

#PROGRAMME ------------------------------------------------------------------------------
    
title_screen()
initialise_board()
initialise_letters()

print('To play, call game()')
