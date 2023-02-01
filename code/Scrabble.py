import random

# Read in the French Scrabble word list from a file
fr_word_list_path = 'french_scrabble_words2.txt'
en_word_list_path = 'english_scrabble_words2.txt'
scrabble_words_fr = None
scrabble_words_en = None
scrabble_words = None
try:
    with open(fr_word_list_path, 'r',encoding="utf-8") as f:
        scrabble_words_fr = f.read().splitlines()
except:
    pass
    
try:
    with open(en_word_list_path, 'r',encoding="utf-8") as f:
        scrabble_words_en = f.read().splitlines()
except:
    pass

#DEFINITION DES VARIABLES ------------------------------------------------------------

#Dictionaries with ANSI color escape codes
couleur = {"bg_noir":'\u001b[40m',"bg_rouge":"\u001b[41m","bg_jaune":"\u001b[43m","bg_vert":"\u001b[42m",'bg_blanc':'\u001b[47m',"bg_magenta":"\u001b[45m","bg_cyan":"\u001b[46m","bg_bleu":"\u001b[44m",
           'txt_noir':'\u001b[30m',"txt_blanc":"\u001b[37m","txt_rouge":"\u001b[31m","txt_vert":"\u001b[32m","clear":"\033[0m"}
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

end_title = [
 '  _____                         ____                   _ ',
 ' / ____|                       / __ \                 | |',
 '| |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __  | |',
 "| | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__| | |",
 '| |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |    |_|',
 ' \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|    (_)']



#Regles du jeu
regles = """\n\n\u001b[32m\033[1mRègles\033[0m\n\n\
\u001b[32mCe jeu de Scrabble suit en grande partie les règles du Scrabble classique, avec quelques modifications.\
\u001b[32m\n\n\033[1mAvant de commencer le jeu\033[0m\n\n\
\u001b[32m[•] Dictionnaires : Vous pouvez choisir entre un dictionnaire français, anglais ou sans dictionnaire.\n\
\u001b[32mCela aura un impact sur les mots que vous pourrez jouer. Gardez à l'esprit que si vous choisissez de \n\
\u001b[32mjouer en anglais, le score et le nombre de lettres seront déséquilibrés pour faire la différence de \n\
\u001b[32mfréquence des lettres entre les langues.\n\
\u001b[32m[•] Nombre de joueurs : de 2 à 10.\n\
\u001b[32m[•] But du jeu : Cumuler le plus de points en formant des mots entrecroisés sur une grille de 15×15 cases.\n\
\u001b[32mLes lettres possèdent des valeurs différentes et les cases, selon leur couleur peuvent multiplier la valeur\n\
\u001b[32mdes lettres (cases bleues) ou des mots (cases rouges).\n\n\
\u001b[32m\033[1mPlacer un mot\033[0m\n\n\
\u001b[32m[•] Longueur minimum : deux lettres.\n\
\u001b[32m[•] Premier mot : Le premier mot doit toujours couvrir la case centrale (h8).\n\
\u001b[32m[•] Placement des mots suivants : soit perpendiculairement, soit parallèlement à un mot déjà placé.\n\
\u001b[32m[•] Sens d’écriture : Les mots doivent toujours être écrits de gauche à droite ou de haut en bas.\n\
\u001b[32m[•] Prolonger un mot : Possibilité de continuer un mot déjà placé en le prolongeant par l’avant, \n\
\u001b[32ml’arrière ou les deux à la fois.\n\n\
\u001b[32m\033[1mAutres actions par tour\033[0m\n\n\
\u001b[32mChaque tour, le joueur peut soit placer un mot ou il peut :\n\
\u001b[32m[•] Tirer à nouveau ses lettres : Le joueur recycle toutes ses lettres et en choisit 7 nouvelles\n\
\u001b[32mau hasard, mais son tour est sauté.\n\
\u001b[32m[•] Passer son tour : Le joueur passe son tour. Si tous les joueurs sautent leur tour consécutivement,\n\
\u001b[32mle jeu vous demandera si vous souhaitez terminer la partie.\n\
\u001b[32m[•] Abandonner : Vous pouvez quitter le jeu entièrement, et vous serez retiré du jeu pendant que\n\
\u001b[32mles autres continuent à jouer.\n\
\u001b[32m[•] Terminer le jeu : Le jeu est terminé pour tous les joueurs et les scores sont calculés.\n\n\
\u001b[32m\033[1mCalcul du score\033[0m\n\n\
\u001b[32mChaque lettre a une valeur indiquée dans son angle supérieur droit.\n\
\u001b[32mLes jokers prennent la valeur de la lettre qu’ils deviennent.\n\n\
\u001b[32mLes cases, selon leur couleur peuvent multiplier la valeur des lettres :\n\
\u001b[32m[•] l2 (bleue claire) : double la valeur de la lettre (x2)\n\
\u001b[32m[•] l3 (bleue foncée) : triple la valeur de la lettre (x3)\n\
\u001b[32m[•] m2 (rose) : double la valeur du mot (x2)\n\
\u001b[32m[•] m3 (rouge) : triple la valeur du mot (x3)\n\n\
\u001b[32mDès qu’une case de couleur est recouverte, elle perd son effet multiplicateur.\n\n\
\u001b[32m[•] Mots formés simultanément : Lorsque deux ou plusieurs mots sont formés lors d’un même coup, les\n\
\u001b[32mvaleurs de chacun de ces mots se cumulent.\n\
\u001b[32m[•] Le bonus « Bingo » : Tout joueur plaçant ses sept lettres en un seul coup (« Bingo ») reçoit une\n\
\u001b[32mbonification de 50 points.\n\n\
\u001b[32m\033[1mCalcul du gagnant\033[0m\n\n\
\u001b[32mÀ la fin de la partie, le score de chaque joueur est diminué de la somme de ses lettres non jouées.\n\
\u001b[32mDe plus, si un joueur a utilisé toutes ses lettres, la somme des lettres non jouées des autres joueurs\n\
\u001b[32mest ajoutée au score de ce joueur.\033[0m"""


#create bag which we will pull from to get letters
bag = []
for let, nb in jetons_nbre.items():
    for i in range(nb):
        bag.append(let)
        
jetons_joueurs = {}
auto_lose = False

#DEFINITION DES FONCTIONS ---------------------------------------------------------------

def initialise_board():
    '''Adds the multiplier squares onto the board'''
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
        #give the player their starting hand
        jetons_joueurs[player] = temp_jetons
    
def mot_valide(mot):
    '''Check if a word is valid for Scrabble
    Input: mot - string of letters
    Returns: bool'''
    #our langauge dicts are in uppercase
    mot = mot.upper()
    
    if len(mot) < 2: #scrabble words need to be at least 2 chrs
        print('Le mot doit avoir au moins 2 lettres.')
        return False
    
    #we test if scrabble_words exists as it may not if they do not have the txt file
    if scrabble_words and mot not in scrabble_words:
        print("Ce mot n'est pas un mot de scrabble valide.")
        return False
        
    return True

def title_screen():
    '''Core function that initialises the game and displays the title'''
    global num_players, score_board, scrabble_words
    
    for line in title: #prints title
        print(line)
    print(('\n')*2)
    
    #Option to print the rules or simply begin the game
    print(couleur['txt_vert']+(' ')*23+"('/règles' pour lire les règles)\n"+couleur['clear'])
    begin = input((' ')*35+"Commencer ? ")
    if begin == "/règles" or begin == "/regles":
        print(regles)
        
    print(('\n')*2)
    
    #Ask if they want the wordchecker
    
    #If BOTH UNAVAILABLE
    if not scrabble_words_fr and not scrabble_words_en:
        print("Impossible de trouver '"+fr_word_list_path+"' ou '"+en_word_list_path+"'.\nLe vérificateur de mots n'est pas disponible.\n")
    else:
        #IF FR NOT AVAILABLE
        if not scrabble_words_fr:
            print("Impossible de trouver '"+fr_word_list_path+"'.\nLe vérificateur de mots français n'est pas disponible.\n")
            ans = input('Désirez-vous utiliser le vérificateur de mots anglais ? (y/n) ')
            if ans == 'n':
                scrabble_words = None
            else:
                scrabble_words = scrabble_words_en
                
        #IF EN NOT AVAILABLE
        if not scrabble_words_en:
            print("Impossible de trouver '"+en_word_list_path+"'.\nLe vérificateur de mots anglais n'est pas disponible.\n")
            ans = input('Désirez-vous utiliser le vérificateur de mots français ? (y/n) ')
            if ans == 'n':
                scrabble_words = None
            else:
                scrabble_words = scrabble_words_fr
                    
        #IF BOTH AVAILABLE
        if scrabble_words_fr and scrabble_words_en:
                ans = input('Désirez-vous utiliser le vérificateur de mots français, anglais ou nul ? (fr/en/n) ')
                if ans == 'n':
                    scrabble_words = None
                elif ans == 'en':
                    scrabble_words = scrabble_words_en
                elif ans == 'fr':
                    scrabble_words = scrabble_words_fr
    
    #we need the language dict to be upper case
    if scrabble_words and not scrabble_words[0].isupper():
        scrabble_words = [x.upper() for x in scrabble_words]
    
    #Gets number of players
    print()
    num_players = 0
    while num_players < 2 or num_players > 10:
        try:
            num_players = int(input('Combien de joueurs (2 à 10)? '))
        except:
            print("Ce n'est pas un nombre de joueurs valable.\n")
            
    #Initializes the score board with the correct number of rows and columns
    score_board = [['0' for i in range(num_players)] for i in range(2)]
    
    #Adds player names to the first row
    for i in range(num_players):
        score_board[0][i] = input('Nom du joueur '+str(i+1)+'? ')
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
    elif elt[0].isupper():
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
        
    #If second row is bigger: takes second row length
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
    ''' Calculates the score of a move
    Input: word_table - dict of tuple:string
           n_letters - int
    Returns: total - int '''
    
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
        print('BINGO !')
        total += 50
    
    return total

def get_superscript(num):
    '''Converts number to superscript
    Input: num - int
    Returns: c - chr'''
    if num == 1:
        c = chr(0x00b9)
    elif 2 <= num <= 3:
        c = chr(0x00b0 + num)
    elif num == 10:
        c = chr(0x02e3)
    else:
        c = chr(0x2070 + num)
    return c

def print_letters():
    '''Prints out the player's letters and letter count in bag'''
    
    print('Il reste',len(bag),'lettres dans le sac.\n')

    print_letters = []
    for let in jetons_joueurs[current_player-1]:
        c = get_superscript(jetons_pts.get(let))
        print_letters.append(let+c)
    
    if len(jetons_joueurs[current_player-1]) > 0:
        print("LETTRES DU JOUEUR",current_player)
        print(*print_letters)
    else:
        print(couleur["txt_rouge"]+"Vous n'avez plus de jetons!"+couleur["clear"])
    
def distrib_letters():
    global bag, jetons_joueurs
    #Distributes random letters for players
    if len(jetons_joueurs[current_player-1]) < 7:
        for i in range(7-len(jetons_joueurs[current_player-1])):
            if len(bag) > 0:
                #Picks a random jetons from the bag
                jeton_rnd = random.choice(bag)
                jetons_joueurs[current_player-1].append(jeton_rnd)
                bag.remove(jeton_rnd)

def place_let(let, cord):
    '''Places a letter on the board
    Input: let - single chr string that isalpha
           cord - tuple countaining two ints (x,y)'''
    x,y = cord
    c = get_superscript(jetons_pts.get(let))
    board[y][x] = let.upper()+c

def get_word_table(word, cord, direct):
    '''Creates a dict of all the letter's cordinates in a word
    Input: word - string
           cord - tuple countaining two ints (x,y)
           direct - bool True is right and False is down
    Returns: word_table - dict of tuple:string
             or False if it cannot'''
    word_table = {}
    x,y = cord
    length = len(word)
    
    #check that the player spells the full word when attaching to another word
    valide = True
    if direct == True: #horizontal
        if x !=0 and board[y][x-1][0].isupper():
            valide = False
        elif not x+length > 14 and board[y][x+length][0].isupper():
            valide = False
    else:
        if y !=0 and board[y-1][x][0].isupper():
            valide = False
        elif not y+length > 14 and board[y+length][x][0].isupper():
            valide = False
    
    if not valide:
        print('Épelez le mot en entier !')
        return False
    
    #create the word_table
    for i in range(length):
        word_table[x,y] = word[i]
        
        if direct:
            x += 1
        else:
            y += 1
            
    return word_table

def place_word(word, cord, direct):
    '''Input: word - string
           cord - tuple countaining two ints (x,y)
           direct - bool True is right and False is down'''
    word_table = get_word_table(word, cord, direct)
    for cord, let in word_table.items():
        place_let(let,cord)

def has_letters(letters):
    '''Tests if the current player has the required letters
    Input: letters - iterable of strings
    Returns: bool
             let - first bad letter found'''
    
    #we don't want to effect the actual player's hand until we know they can play the move
    current_jetons = jetons_joueurs[current_player-1].copy()
    
    for let in letters:
        if let in current_jetons:
            current_jetons.remove(let)
        else:
            return False, let
        
    return True, None

def test_letters(letters):
    '''Tests if the current player has the required letters
        and if they don't asks if they want to use their jokers
    Input: letters - iterable of strings
    Returns: bool'''
    global jetons_joueurs
    
    #delete extra letters
    jetons_joueurs[current_player-1] = jetons_joueurs[current_player-1][:7]
    
    valide, let = has_letters(letters)
    
    for i in range(jetons_joueurs[current_player-1].count('joker')):
        if valide:
            break
        
        ans = input('Voulez-vous utiliser un joker pour la lettre '+let+' (y/n) ? ')
        if ans == 'y':
            #I append the extra letters so that later we can decide to remove the extra letters or the jokers
            jetons_joueurs[current_player-1].append(let)
        else:
            break
        
        valide, let = has_letters(letters)
    
    if not valide:
        print("Vous n'avez pas les lettres pour ce mot.")
        #delete extra letters
        jetons_joueurs[current_player-1] = jetons_joueurs[current_player-1][:7]
            
    return valide

def remove_letters(letters):
    '''Removes letters from the player's hand
    Input: letters - iterable of strings'''
    global jetons_joueurs
    
    #remove extra jokers
    over = len(jetons_joueurs[current_player-1]) - 7
    if over > 0:
        for i in range(over):
            jetons_joueurs[current_player-1].remove('joker')
    
    for let in letters:
        jetons_joueurs[current_player-1].remove(let)
    print('Vous avez utilisé',*letters)

def replace_letters():
    '''Puts player's letters in the bag and draws 7 new ones'''
    for i in range(7):
        bag.append(jetons_joueurs[current_player-1][i])
        
    jetons_joueurs[current_player-1] = []
    
    for i in range(7):
        #Picks a random jetons from the bag
        jeton_rnd = random.choice(bag)
        jetons_joueurs[current_player-1].append(jeton_rnd)
        bag.remove(jeton_rnd)
        
    print_letters()

def preview_board(word_table):
    ''' Prints a preview of the board with the unplayed move of word_table
    Input: word_table - dict of tuple:string'''
    
    print()
    print('  ',end='')
    for i in range(15):
        print(' '+chr(i+97), end = '')
    print()
    for y,row in enumerate(board):
        print(str(y+1).rjust(2), end = '')
        for x,elt in enumerate(row):
            if (x,y) in word_table:
                let = word_table[(x,y)]
                c = get_superscript(jetons_pts.get(let))
                
                if elt[0].isupper(): #if it is a jeton
                    if elt[0] == let:
                        print(couleur['txt_noir']+couleur['bg_vert']+let+c+couleur['clear'], end='')
                    else:
                        print(couleur['txt_blanc']+couleur['bg_rouge']+'XX'+couleur['clear'], end='')
                else:
                    print(couleur['txt_noir']+couleur['bg_jaune']+let+c+couleur['clear'], end='')
            else:
                print(color_elt(elt), end='')
        print()

def add_score(pts):
    global score_board
    #Add score to scoreboard of the current player
    score = int(score_board[1][current_player-1])
    score += pts
    score_board[1][current_player-1] = str(score)

def test_word(word,cord,direct):
    ''' Tests if a move can be played or not and asks if they want to play it
    Input: word - string
           cord - tuple countaining two ints (x,y)
           direct - bool True is right and False is down
    Return: bool'''
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
                if board[y][x][0] != let: #[0] because we only need the letter
                    valide = False
                else:
                    connected = True
            else:
                new_table[(x,y)] = let
    
    #check that they have the jetons
    check = test_letters(new_table.values())
    if not check:
            return False
    
    #preview board
    preview_board(word_table)
    
    if not connected:
        valide = False
        print(couleur["txt_rouge"]+"INVALIDE"+couleur["clear"])
        print("Le mot n'est pas relié à un autre.")
    
    if off_board:
        valide = False
        print(couleur["txt_rouge"]+"INVALIDE"+couleur["clear"])
        print("Le mot ne tient pas sur le plateau.")
    
    #Calculate points
    if valide:
        pts = score(word_table,len(new_table.values()))
        print('Ce mot vous rapportera',pts,'points.')
    
        ans = input('Voulez-vous placer ce mot ? (y/n) : ')
        if ans == 'y':
          remove_letters(new_table.values())
          add_score(pts)
        else:
            valide = False
    
    return valide


def user_input():
    '''Gets the information from the player for a move
    Returns: word - string
            cord - tuple countaining two ints (x,y)
            direct - bool True is right and False is down'''
    print()
    while True:
        mot = input("Saissisez un mot que vous souhaitez placer sur le plateau : ")
        if mot.isalpha() and mot_valide(mot): #checks if the letter is not part of the alphabet
            break
    
    while True:
        range_num = range(1,16) #range of numbers from 1 to 15(since 16 is excluded)
        range_letters='abcdefghijklmno'
        location = input("Saissisez un coordonné pour la premiere lettre de votre mot (ex: a1) : ")
        if len(location)<=3:
            try:
                if range_letters.find(location[0])!=-1 and int(location[1:]) in range_num:
                    break
            except:
                pass
        
    while True:
        orientation = input("Saissisez une orientation horizontale ou verticale pour votre mot (h/v) : ")
        if len(orientation) > 0 and (orientation[0] == 'v' or orientation[0]=='h'):
            break

    word = mot.upper()
    cord = (range_letters.find(location[0]),int(location[1:])-1)
    direct = True if orientation[0] == 'h' else False
        
    return word,cord,direct

def print_round():
    print('\n')
    global current_round, current_player, score_board
    current_round += 1
    current_player = (current_player % len(score_board[0]))+1
    print("TOUR",current_round,"- JOUEUR",current_player,"|",score_board[0][current_player-1],"\n")

def print_actions():
    actions = ["1. Jouer un mot",
               "2. Tirer à nouveau les lettres",
               "3. Sauter le tour",
               "4. Abandonner",
               "5. Terminer le jeu"]
    
    print()
    # Get the maximum length of the row
    max_length = max([len(i) for i in actions])

    # Create a top and bottom border
    border = "+" + "-"*(max_length+2) + "+"
    print(border)

    # Print each item
    for el in actions:
        print("| " + el.ljust(max_length) + " |")

    # Print the bottom border
    print(border)
    
    print()
    
    #Input loop
    while True:
        try:
            act = int(input("Choisissez une action à faire (1-5) : "))
            assert act in range(1,6)
            return act
        except:
           print("Action inconnue.") 
    

def first_move():
    '''The first move is different from the others'''
    print_round()
    print_board()
    print_score()
    print_letters()
    
    while True: #input loop
        w,c,d = user_input()
        
        in_center = False
        if not test_letters(w):
            continue
        
        word_table = get_word_table(w,c,d)
        if not word_table:
            continue
        
        for cord in word_table.keys():
            if cord == (7,7):
                in_center = True
        preview_board(word_table)
        
        if not in_center:
            print("Veuillez placer le premier mot au centre du plateau (h8).")
            continue
        
        pts = score(word_table,len(w))
        print('Ce mot vous rapportera',pts,'points.')
    
        ans = input('Voulez-vous placer ce mot ? (y/n) : ')
        if ans == 'y':
            remove_letters(w)
            add_score(pts)
            place_word(w,c,d)
            break
    distrib_letters()

def game():
    global current_player
    first_move()
    skip = 0
    
    while True: #game loop
        print_round()
        print_board()
        print_score()
        print_letters()
        act = print_actions()
        
        if act == 3: #Skip
            skip += 1
            if skip >= len(score_board[0]):
                
                ans = input('All players have skipped in a row, would you like to end the game? (y/n): ')
                if ans == "y":
                    final_scores()
                    break
            continue
        else:
            skip = 0
            
        if act == 2: #Re-pull
            replace_letters()
            continue
            
        elif act == 4: #Forfeit
            print("\u001b[33mJoueur "+str(current_player)+" ("+score_board[0][current_player-1]+") a quitté le jeu.\u001b[0m")
            score_board[0].pop(current_player-1)
            score_board[1].pop(current_player-1)
            current_player -= 1
            if len(score_board[0]) == 1:
                auto_lose = True
                final_scores()
                break
            else:
                continue
            
        elif act == 5: #End game
            final_scores()
            break 
        
        #Play word
        while True: #input loop
            w,c,d = user_input()
            if test_word(w,c,d): #if the move is correct and they want to place it
                place_word(w,c,d)
                break
        distrib_letters()


def final_scores():
    '''Function called if both players skip their turn and they answer 'yes' to stopping game'''
    global auto_lose
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
    
    print(('\n')*2)
    
    for line in end_title:
        print(line)
    print(('\n')*2)
    print('Les scores ultimes sont :')
    print_score()
    
    #Finds the best score and if there is a tie
    best_score = max(scores)
    best_count = scores.count(best_score)
    
    if auto_lose == True:
        print('Le gagnant est '+score_board[0][0]+' !')
        
    else:
        #If there is a tie, find and print the winners
        if best_count > 1:
            winners = []
            for i,score in enumerate(score_board[1]):
                if int(score) == best_score:
                    winners.append(score_board[0][i])
                    
            winners[-1] = 'et '+str(winners[-1])
            print('Le jeu est à égalité. Les gagnants sont '+(", ".join(str(x) for x in winners))+' !')
        
        #If there is no tie, print the winner
        else:
            winner = score_board[0][scores.index(best_score)]
            print('Le gagnant est '+winner+' !')
            


#PROGRAMME ------------------------------------------------------------------------------

title_screen()
initialise_board()
initialise_letters()

game()
