import random

# Charger les listes des mots du Scrabble français et anglais à partir d'un fichier
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

#Dictionnaires avec séquence d'échappement des couleur ANSI
couleur = {"bg_noir":'\u001b[40m',"bg_rouge":"\u001b[41m","bg_jaune":"\u001b[43m","bg_vert":"\u001b[42m",'bg_blanc':'\u001b[47m',"bg_magenta":"\u001b[45m","bg_cyan":"\u001b[46m","bg_bleu":"\u001b[44m",
           'txt_noir':'\u001b[30m',"txt_blanc":"\u001b[37m","txt_rouge":"\u001b[31m","txt_vert":"\u001b[32m","clear":"\033[0m"}
couleurs_loc= {"m2":couleur['bg_magenta'],"m3":couleur['bg_rouge'],"l2":couleur['bg_cyan'],"l3":couleur['bg_bleu']}

current_round = 0
current_player = 0

#Initialisation du plateau avec les couleurs
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
\u001b[32mjouer en anglais, le score et le nombre de lettres seront déséquilibrés à cause de la différence de \n\
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
\u001b[32ml’arrière ou les deux à la fois (Attention ! Cela nécessite d'écrire le mot en entier.)\n\
\u001b[32m[•] Afin d'utiliser un joker, épelez le mot que vous souhaitez placer et le jeu vous demandera si \n\
\u001b[32mvous souhaitez utiliser votre joker.\n\n\
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
\u001b[32mLes cases, selon leur couleur peuvent multiplier la valeur des lettres ou des mots :\n\
\u001b[32m[•] l2 (bleue claire) : double la valeur de la lettre (x2)\n\
\u001b[32m[•] l3 (bleue foncée) : triple la valeur de la lettre (x3)\n\
\u001b[32m[•] m2 (rose) : double la valeur du mot (x2)\n\
\u001b[32m[•] m3 (rouge) : triple la valeur du mot (x3)\n\n\
\u001b[32mDès qu’une case de couleur est recouverte, elle perd son effet multiplicateur.\n\n\
\u001b[32m[•] Mots formés simultanément : Lorsque deux ou plusieurs mots sont formés lors d’un même coup, les\n\
\u001b[32mvaleurs de chacun de ces mots se cumulent.\n\
\u001b[32m[•] Le bonus « Bingo » : Si un joueur plaçe ses sept lettres en un seul coup (« Bingo »), il reçoit une\n\
\u001b[32mbonification de 50 points.\n\n\
\u001b[32m\033[1mCalcul du gagnant\033[0m\n\n\
\u001b[32mÀ la fin de la partie, le score de chaque joueur est diminué de la somme de ses lettres non jouées.\n\
\u001b[32mDe plus, si un joueur a utilisé toutes ses lettres, la somme des lettres non jouées des autres joueurs\n\
\u001b[32mest ajoutée au score de ce joueur.\033[0m"""


#creation du sac pour piocher des lettres
bag = []
for let, nb in jetons_nbre.items():
    for i in range(nb):
        bag.append(let)

jetons_joueurs = {}
auto_lose = False

#DEFINITION DES FONCTIONS ---------------------------------------------------------------

def initialise_board():
    '''Place les carrés multiplicateurs sur le plateau de jeu'''
    for cord, value in plateau.items():
        i, j = cord
        val = value[0]+str(value[1]) #le multiplicateur consiste d'un int et d'une string
        board[i][j] = val

def initialise_letters():
    '''Distribution aléatoire des jetons au départ'''
    for player in range(len(score_board[0])):
        temp_jetons = []
        for i in range(7):
            #Pioche un jeton au hasard dans le sac
            jeton_rnd = random.choice(bag)
            temp_jetons.append(jeton_rnd)
            bag.remove(jeton_rnd)
        #donner au joueur sa main de départ
        jetons_joueurs[player] = temp_jetons
    
def mot_valide(mot):
    '''Vérifier si un mot est valide pour le Scrabble
    Input: mot - string de letters
    Returns: bool'''
    mot = mot.upper() #nos dictionnaires de langue txt sont en majuscules
    
    if not mot.isalpha(): #vérifie que le mot ne fait pas partie de l'alphabet
        return False
    
    if len(mot) < 2: #les mots du scrabble doivent être composés d'au moins 2 chrs
        print('Le mot doit avoir au moins 2 lettres.')
        return False
    
    #nous testons si scrabble_words existe car il peut ne pas exister s'ils n'ont pas le fichier txt
    if scrabble_words and mot not in scrabble_words:
        print("Ce mot n'est pas un mot de scrabble valide.")
        return False
        
    return True

def title_screen():
    '''Fonction principale qui initialise le jeu et affiche le titre'''
    global num_players, score_board, scrabble_words
    
    for line in title: #imprime le titre
        print(line)
    print(('\n')*2)
    
    #Possibilité d'imprimer les règles ou de commencer le jeu
    print(couleur['txt_vert']+(' ')*28+"('/r' pour lire les règles)\n"+couleur['clear'])
    begin = input((' ')*35+"Commencer ? ")
    if '/r' in begin:
        print(regles)
        
    print(('\n')*2)
    
    #Demander s'ils veulent le vérificateur de mots vvvvv
    
    #Si LES DEUX NE SONT PAS DISPONIBLES
    if not scrabble_words_fr and not scrabble_words_en:
        print("Impossible de trouver '"+fr_word_list_path+"' ou '"+en_word_list_path+"'.\nLe vérificateur de mots n'est pas disponible.\n")
    else:
        #SI FR N'EST PAS DISPONIBLE
        if not scrabble_words_fr:
            print("Impossible de trouver '"+fr_word_list_path+"'.\nLe vérificateur de mots français n'est pas disponible.\n")
            ans = input('Désirez-vous utiliser le vérificateur de mots anglais ? (y/n) ')
            if ans == 'n':
                scrabble_words = None
            else:
                scrabble_words = scrabble_words_en
                
        #SI EN N'EST PAS DISPONIBLE
        if not scrabble_words_en:
            print("Impossible de trouver '"+en_word_list_path+"'.\nLe vérificateur de mots anglais n'est pas disponible.\n")
            ans = input('Désirez-vous utiliser le vérificateur de mots français ? (y/n) ')
            if ans == 'n':
                scrabble_words = None
            else:
                scrabble_words = scrabble_words_fr
                    
        #SI LES DEUX SONT DISPONIBLES
        if scrabble_words_fr and scrabble_words_en:
                ans = input('Désirez-vous utiliser le vérificateur de mots français, anglais ou nul ? (fr/en/n) ')
                if ans == 'n':
                    scrabble_words = None
                elif ans == 'en':
                    scrabble_words = scrabble_words_en
                elif ans == 'fr':
                    scrabble_words = scrabble_words_fr
    
    #nous avons besoin que le dict de langue soit en majuscules
    if scrabble_words and not scrabble_words[0].isupper():
        scrabble_words = [x.upper() for x in scrabble_words]
    
    #Obtient le nombre de joueurs
    print()
    num_players = 0
    while num_players < 2 or num_players > 10:
        try:
            num_players = int(input('Combien de joueurs (2 à 10)? '))
        except:
            print("Ce n'est pas un nombre de joueurs valable.\n")
            
    #Initialise le tableau de score avec le nombre de lignes et de colonnes.
    score_board = [['0' for i in range(num_players)] for i in range(2)]
    
    #Ajoute les noms des joueurs à la première ligne
    for i in range(num_players):
        score_board[0][i] = input('Nom du joueur '+str(i+1)+'? ')
    print(('\n')*2)

def color_elt(elt):
    '''Ajoute de la couleur à un élément du tableau
    Input: elt - string
    Returns: new_elt - string'''
    new_elt = ''
    
    if elt.isspace(): #fond (background)
        new_elt = new_elt= couleur['bg_noir']+elt+couleur['clear']
    elif elt.islower(): #multiplicateurs
        new_elt = couleur['txt_blanc']+couleurs_loc[elt]+elt+couleur['clear']
    elif elt[0].isupper(): #jeton / lettre
        new_elt = couleur['txt_noir']+couleur['bg_blanc']+elt+couleur['clear']
    return new_elt
        

def print_board():
    '''Imprime le plateau'''
    print('  ',end='')
    for i in range(15):
        print(' '+chr(i+97), end = '') #chr(i+97) transforme i en lettre ex: 0->a
    print()
    for i,row in enumerate(board):
        print(str(i+1).rjust(2), end = '')
        for element in row:
            print(color_elt(element), end='')
        print()

def print_score():
    '''Imprime le tableau des scores'''
    print()
    #Détermine la longueur du tableau d'affichage
    len_row = 0
    temp_len = 0

    #Vérifie la longueur de la première rangée
    for i in range(len(score_board[0])):
        len_row += len(score_board[0][i])
        
    #Vérifie la longueur de la deuxième rangée
    for i in range(len(score_board[1])):
        temp_len += len(score_board[1][i])
        
    #Si la deuxième rangée est plus grande : prend la longueur de la deuxième rangée
    if temp_len > len_row:
        len_row = temp_len

    len_row += (len(score_board[0])*3)
    line = (('+')+('-')*(len_row-1)+('+'))

    #Trouve la longueur de chaque colonne
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
                
    #Imprime le tableau d'affichage
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
    ''' Calcule le score d'un mot
    Input: word_table - dict de tuple:string
           n_letters - int
    Returns: total - int '''
    
    total = 0
    for cord,let in word_table.items(): #score de lettres
        num = jetons_pts[let]
        x,y = cord
        if not board[y][x][0].isupper(): #s'il y a déjà un jeton on n'utilise pas le multiplicateur
            if cord in plateau and plateau[cord][0] == 'l':
                num *= plateau[cord][1]
        total = total + num
        
    for cord in word_table.keys(): #multiplicateurs de mots
        x,y = cord
        if not board[y][x][0].isupper(): #s'il y a déjà un jeton on n'utilise pas le multiplicateur
            if cord in plateau and plateau[cord][0] == 'm':
                total *= plateau[cord][1]
            
    if n_letters >=7: #bonus pour l'utilisation des 7 jetons
        print('BINGO !')
        total += 50
    
    return total

def get_superscript(num):
    '''Convertit un nombre en chr superscript
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
    '''Imprime les lettres du joueur et le nombre de lettres dans le sac.'''
    
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
    '''Remplit la main du joueur avec des nouveaux jetons aléatoires.'''
    global bag, jetons_joueurs
    #Calcul de jeton manquant max 7
    for i in range(7-len(jetons_joueurs[current_player-1])):
        if len(bag) > 0:
            #Pioche un jeton au hasard dans le sac
            jeton_rnd = random.choice(bag)
            jetons_joueurs[current_player-1].append(jeton_rnd)
            bag.remove(jeton_rnd)

def place_let(let, cord):
    '''Place une lettre sur le plateau
    Input: let - chr (lettre de scrabble)
           cord - tuple de deux ints (x,y)'''
    x,y = cord
    c = get_superscript(jetons_pts.get(let))
    board[y][x] = let.upper()+c

def get_word_table(word, cord, direct):
    '''Crée un dict de toutes les coordonnées des lettres dans un mot
    Input: word - string
           cord - tuple de deux ints (x,y)
           direct - bool: True = horizontal et False = vertical
    Returns: word_table - dict of tuple:string
             or False if it cannot'''
    word_table = {}
    x,y = cord
    length = len(word)
    
    #Vérifie que le joueur épelle le mot complet lorsqu'il l'attache à un autre mot
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
    
    #Remplit le dict word_table
    for i in range(length):
        word_table[x,y] = word[i]
        
        if direct:
            x += 1
        else:
            y += 1
            
    return word_table

def place_word(word, cord, direct):
    '''Place un mot sur le plateau
        Input: word - string
           cord - tuple countaining two ints (x,y)
           direct - bool True is right and False is down'''
    word_table = get_word_table(word, cord, direct)
    for cord, let in word_table.items():
        place_let(let,cord)

def has_letters(letters):
    '''Teste si le joueur possède les lettres nécessaires
    Input: letters - iterable of chr (ex: liste de chr ou string)
    Returns: bool
             let - première lettre manquante trouvée'''
    
    #nous ne voulons pas affecter la main du joueur tant que nous ne savons pas si il peut jouer le mot
    current_jetons = jetons_joueurs[current_player-1].copy()
    
    for let in letters:
        if let in current_jetons:
            current_jetons.remove(let)
        else:
            return False, let
        
    return True, None

def test_letters(letters):
    '''Teste si le joueur a les lettres nécessaires
        et s'il n'en a pas, lui demande s'il veut utiliser ses jokers
    Input: letters - iterable of chr (ex: liste de chr ou string)
    Returns: bool'''
    global jetons_joueurs
    
    #supprimer les lettres supplémentaires
    jetons_joueurs[current_player-1] = jetons_joueurs[current_player-1][:7]
    
    valide, let = has_letters(letters)
    
    for i in range(jetons_joueurs[current_player-1].count('joker')):
        if valide:
            break
        
        ans = input('Voulez-vous utiliser un joker pour la lettre '+let+' (y/n) ? ')
        if ans == 'y':
            #Ajoute les lettres supplémentaires afin que nous puissions
            #décider plus tard de supprimer les lettres supplémentaires ou les jokers.
            jetons_joueurs[current_player-1].append(let)
        else:
            break
        
        valide, let = has_letters(letters)
    
    if not valide:
        print("Vous n'avez pas les lettres pour ce mot.")
        #supprimer les lettres supplémentaires
        jetons_joueurs[current_player-1] = jetons_joueurs[current_player-1][:7]
            
    return valide

def remove_letters(letters):
    '''Retire les lettres utilisées de la main du joueur
    Input: letters - iterable of chr (ex: liste de chr ou string)'''
    global jetons_joueurs
    
    #supprimer les jokers supplémentaires
    over = len(jetons_joueurs[current_player-1]) - 7
    if over > 0:
        for i in range(over):
            jetons_joueurs[current_player-1].remove('joker')
    
    for let in letters:
        jetons_joueurs[current_player-1].remove(let)
    print('Vous avez utilisé',*letters)

def replace_letters():
    '''Met les lettres du joueur dans le sac et en tire 7 nouvelles.'''
    for i in range(7):
        bag.append(jetons_joueurs[current_player-1][i])
        
    jetons_joueurs[current_player-1] = []
    
    for i in range(7):
        #Pioche un jeton au hasard dans le sac
        jeton_rnd = random.choice(bag)
        jetons_joueurs[current_player-1].append(jeton_rnd)
        bag.remove(jeton_rnd)
        
    print_letters()

def preview_board(word_table):
    '''Imprime un aperçu du plateau avec le mot non joué de word_table
    Input: word_table - dict of tuple:string'''
    
    print()
    print('  ',end='')
    for i in range(15):
        print(' '+chr(i+97), end = '') #chr(i+97) transforme i en lettre ex: 0->a
    print()
    for y,row in enumerate(board):
        print(str(y+1).rjust(2), end = '')
        for x,elt in enumerate(row):
            if (x,y) in word_table:
                let = word_table[(x,y)]
                c = get_superscript(jetons_pts.get(let))
                
                #couleur du jeton vvv
                if elt[0].isupper(): #s'il y a une intersection
                    if elt[0] == let: #et si la lettre correspond
                        print(couleur['txt_noir']+couleur['bg_vert']+let+c+couleur['clear'], end='')
                    else: #et la lettre ne correspond pas
                        print(couleur['txt_blanc']+couleur['bg_rouge']+'XX'+couleur['clear'], end='')
                else: #defaut
                    print(couleur['txt_noir']+couleur['bg_jaune']+let+c+couleur['clear'], end='')
            else:
                print(color_elt(elt), end='')
        print()

def add_score(pts):
    '''Met à jour le score du joueur sur le tableau de score'''
    global score_board
    score = int(score_board[1][current_player-1])
    score += pts
    score_board[1][current_player-1] = str(score)

def test_word(word,cord,direct):
    ''' Teste si un mot peut être joué ou non et demande s'il veut le jouer.
    Input: word - string
           cord - tuple de deux int (x,y)
           direct - bool True is right and False is down
    Return: bool'''
    word_table = get_word_table(word,cord,direct)
    if not word_table: 
        return False
    
    valide = True
    off_board = False
    connected = False
    
    #tester l'emplacement du mot et créer une nouvelle table contenant tous les jetons nécessaires pour jouer le mouvement
    #vérifiez également qu'il y a au moins une connexion
    new_table = {}
    for cord,let in word_table.items():
        x,y = cord
        
        if x < 0 or x > 14: #Vérifier que le placement est sur le plateau
            off_board = True
        elif y < 0 or y > 14:
            off_board = True
        else:
            if board[y][x][0].isupper(): #si c'est un jeton
                if board[y][x][0] != let: #[0] car on a que besoin de la lettre
                    valide = False
                else:
                    connected = True
            else:
                new_table[(x,y)] = let #this letter is required add it too new_table
    
    #vérifier qu'ils ont les jetons
    check = test_letters(new_table.values())
    if not check:
        return False
    
    preview_board(word_table) #imprimer l'aperçu du plateau
    
    if not connected:
        valide = False
        print(couleur["txt_rouge"]+"INVALIDE"+couleur["clear"])
        print("Le mot n'est pas relié à un autre.")
    
    if off_board:
        valide = False
        print(couleur["txt_rouge"]+"INVALIDE"+couleur["clear"])
        print("Le mot ne tient pas sur le plateau.")
    
    #Calculer les points
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
    '''Obtient les informations du joueur pour un mot
    Returns: word - string
            cord - tuple de deux int (x,y)
            direct - bool True is right and False is down'''
    print()
    while True:
        mot = input("Saissisez un mot que vous souhaitez placer sur le plateau : ")
        if mot_valide(mot): 
            break
    
    while True:
        range_num = range(1,16) #intervalle de nombres de 1 à 15 (puisque 16 est exclu)
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
    '''Imprimer les données du tour'''
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
    # Obtient la longueur maximale de la rangée
    max_length = max([len(i) for i in actions])

    # Crée une bordure sous forme de string
    border = "+" + "-"*(max_length+2) + "+"
    print(border) #bordure du haut

    # Imprime chaque élément
    for el in actions:
        print("| " + el.ljust(max_length) + " |")

    print(border) #bordure du bas
    
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
    '''La première action est différente des autres'''
    print_round()
    print_board()
    print_score()
    print_letters()
    
    while True: #boucle d'entrée
        w,c,d = user_input()
        
        in_center = False
        if not test_letters(w):
            continue
        
        word_table = get_word_table(w,c,d)
        if not word_table:
            continue
        
        for cord in word_table.keys():
            if cord == (7,7): #vérifie qu'au moins une lettre se trouve au centre
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
    
    while True: #Boucle de jeu
        print_round()
        print_board()
        print_score()
        print_letters()
        act = print_actions()
        
        if act == 3: #Skip
            skip += 1
            if skip >= len(score_board[0]):
                
                ans = input('Tous les joueurs ont sauté leur tour consécutivement, voulez-vous terminer le jeu ? (y/n): ')
                if ans == "y":
                    final_scores()
                    break
            continue
        else:
            skip = 0
            
        if act == 2: #Reprendre ses lettres
            replace_letters()
            continue
            
        elif act == 4: #Quitte 
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
            
        elif act == 5: #Termine le jeu
            final_scores()
            break 
        
        #joue un mot
        while True: #boucle de saisie
            w,c,d = user_input()
            if test_word(w,c,d): #si le mouvement est correct et que le joueur veut le placer
                place_word(w,c,d)
                break
        distrib_letters()


def final_scores():
    '''Fonction appelée si les deux joueurs passent leur tour et qu'ils répondent "oui" à l'arrêt du jeu.'''
    global auto_lose
    #Crée une nouvelle liste avec les scores sous forme d'ints
    scores = [int(x) for x in score_board[1]]
    
    #Soustrait le nombre de lettres restantes des joueurs de leur score
    for i in range(len(score_board[0])):
        #Si un joueur a utilisé toutes ses lettres, la somme des lettres non jouées des autres joueurs est ajoutée au score de ce joueur
        if len(jetons_joueurs[i]) == 0:
            for j in range(len(jetons_joueurs)):
                if i != j:
                    scores[i] += len(jetons_joueurs[j])
            else:
                if scores[i] > 0:
                    scores[i] -= len(jetons_joueurs[i])
    
    #Remettre les nouvelles notes dans le tableau et les imprimer
    for i in range(len(score_board[0])):
        score_board[1][i] = str(scores[i])
    
    print(('\n')*2)
    
    for line in end_title:
        print(line)
    print(('\n')*2)
    print('Les scores ultimes sont :')
    print_score()
    
    #Détermine le meilleur score et en cas d'égalité
    best_score = max(scores)
    best_count = scores.count(best_score)
    
    if auto_lose == True:
        print('Le gagnant est '+score_board[0][0]+' !')
        
    else:
        #En cas d'égalité, détermine et imprime les gagnants
        if best_count > 1:
            winners = []
            for i,score in enumerate(score_board[1]):
                if int(score) == best_score:
                    winners.append(score_board[0][i])
                    
            winners[-1] = 'et '+str(winners[-1])
            print('Le jeu est à égalité. Les gagnants sont '+(", ".join(str(x) for x in winners))+' !')
        
        #S'il n'y a pas d'égalité, imprime le gagnant
        else:
            winner = score_board[0][scores.index(best_score)]
            print('Le gagnant est '+winner+' !')
            


#PROGRAMME ------------------------------------------------------------------------------

title_screen()
initialise_board()
initialise_letters()

game()
