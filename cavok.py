import pyxel
import random

# taille de la fenetre 128x128 pixels
screen_length = 128
screen_width = 128

pyxel.init(screen_length, screen_width, title="Casse brique")

# position initiale du vaisseau
# (origine des positions : milieu bas)
plateau_x = 54
plateau_y = 120
plateau_velocity_x = 0


'''
Choix de ne mettre que 6 briques et un seul niveau car le jeu est assez dur comme ça
'''

#plateau_flrm = [plateau_x, plateau_y, plateau_x, plateau_y, plateau_x, plateau_y, plateau_x, plateau_y, plateau_x, plateau_y, ]
#plateau_flrm = [plateau_x-1, plateau_y, plateau_x-2, plateau_y+1, plateau_x-3, plateau_y+1, plateau_x-4, plateau_y-2, plateau_x-5, plateau_y+3, plateau_x-5, plateau_y+3]

#crée une liste d'entiers aléatoires entre 1 et 3 représentant les durabilités des briques
briques = [random.randint(1,3) for i in range(6)]

brk_x = [10, 25, 28, 43, 46, 61, 64, 79, 82, 97, 100, 115]
#coordonnés des briques : de x = 4, y = 30 à x = 124, y = 40; hauteur = 10 largeur = 20
#6 ,  12 ,  9
briques_x = 10
briques_y = 30


#définition des coordonnées de la balle : x = 64, y = 100; ainsi que sa vélocité en abscisse et en ordonnée qui est aléatoire, -1 ou 1 ou 0 pour x
ball_x = 64
ball_y = 100
ball_velocity_x = random.randint(-1, 1)
ball_velocity_y = random.choice([-1,1])

#définition du nombre de vie : ici 3
life = 5

#définiton du score : au début il est à 0
score = 0

#définition du temps
time = 0





def plateau_deplacement(x, plateau_velocity_x):
    """
    déplacement avec les touches de directions
    déplacement latéral du plateau avec une vitesse de 3
    sauf lorsque le plateau est en bordure
    si aucun mouvement, vitesse du plateau en x est 0
    this function return the board game's x and velocity
    """

    if pyxel.btn(pyxel.KEY_RIGHT):
        plateau_velocity_x = 3
        x = x + plateau_velocity_x
        if (x > 104):x = 103
    elif pyxel.btn(pyxel.KEY_LEFT):
        plateau_velocity_x = 3
        x = x - plateau_velocity_x
        if (x < 3) :x = 4

    else:
        plateau_velocity_x = 0

    return x, plateau_velocity_x



def ball_mvt(x, y, ball_velocity_x, ball_velocity_y, plateau_velocity_x):
    """
    Cette fonction définie la trajectoire et la position de la balle
    La vélocité de la balle ne peut diminuer donc elle augmente avec le temps
    Elle retourne les coordonnées et les velocités de la balle
    """

    x = x + ball_velocity_x
    y = y + ball_velocity_y


    if x < 0:
        ball_velocity_x = abs(ball_velocity_x)
    if x > 128:
        ball_velocity_x = -abs(ball_velocity_x)

    if y < 0:
        ball_velocity_y = abs(ball_velocity_y)
    if y > 128:
        ball_velocity_y = -abs(ball_velocity_y)

    return x, y, ball_velocity_x, ball_velocity_y




def life_is_ok(life, ball_y):
    """
    Vérification  de l'ordonnée de la balle
    retire une vie si la balle est en ordonnée supérieur à 127
    his function return the remaining lives
    >>>life_is_ok(3,129)
    2
    >>>life_is_ok(3,100)
    3
    >>>life_is_ok(0,129)
    -1
    """
    if ball_y > screen_width:
        life = life-1
    return life



def brique_check(ball_x, ball_y, brk_x, briques, ball_velocity_y, ball_velocity_x, score):
    """
    vérification que les briques sont retirées ou laissées à leurs places
    selon :
    si la balle arrive par le bas:
        retirer la brique et rebondir vers le bas
    si la balle arrive par le haut:
        retirer la brique et rebondir vers le haut
    This funtion return the ball velocity x and y, the ball x and y, and the player's score
    """

    if (ball_y == 34 or ball_y == 33) and ball_velocity_y < 0:
        for n in range(0,12,2):
            if (brk_x[n]<=ball_x<=brk_x[n+1] or brk_x[n]<=ball_x+1<=brk_x[n+1] or brk_x[n]<=ball_x+2<=brk_x[n+1] or brk_x[n]<=ball_x+3<=brk_x[n+1]) and briques[n//2] != 0:

                ball_velocity_y = abs(ball_velocity_y)

                briques[n//2] = briques[n//2] - 1
                score = score + 10

                return int(ball_x),  int(ball_y), int(ball_velocity_x), int(ball_velocity_y), score

    if ball_y+3 == 30 and ball_velocity_y > 0:
        for n in range(0,12,2):
            if (brk_x[n]<=ball_x<=brk_x[n+1] or brk_x[n]<=ball_x+1<=brk_x[n+1] or brk_x[n]<=ball_x+2<=brk_x[n+1] or brk_x[n]<=ball_x+3<=brk_x[n+1]) and briques[n//2] != 0:

                ball_velocity_y = -abs(ball_velocity_y)

                briques[n//2] = briques[n//2] - 1
                score = score + 10

                return int(ball_x),  int(ball_y), int(ball_velocity_x), int(ball_velocity_y), score

    return int(ball_x),  int(ball_y), int(ball_velocity_x), int(ball_velocity_y), score




def plateau_check(ball_x, ball_y, ball_velocity_x, ball_velocity_y, plateau_x, plateau_y, plateau_velocity_x):
    """
    Définission des collisions et des réponses à ses collisions avec le plateau de jeu
    soit le milieu
    soit la balle est sur le bord gauche
    soit le bord droit
    soit aucun des trois
    This function return the velocity of the ball in x and y
    """

    if plateau_x<=ball_x<=plateau_x+20:

        if ball_velocity_x < 3 and ball_velocity_x > -3:
            ball_velocity_x = ball_velocity_x + (plateau_velocity_x//3)

        ball_velocity_y = -abs(ball_velocity_y)

        return int(ball_velocity_x), int(ball_velocity_y)

    elif plateau_x-1 == ball_x and plateau_y == ball_y or plateau_x-2 == ball_x and plateau_y+1 == ball_y or plateau_x-3 == ball_x and plateau_y+1 == ball_y or plateau_x-4 == ball_x and plateau_y-2 == ball_y or plateau_x-5 == ball_x and plateau_y+3 == ball_y or plateau_x-5 == ball_x and plateau_y+3 == ball_y:

        ball_velocity_x = -abs(ball_velocity_x)
        ball_velocity_y = -abs(ball_velocity_y)

        return int(ball_velocity_x), int(ball_velocity_y)


    elif plateau_x+21 == ball_x and plateau_y == ball_y or plateau_x+22 == ball_x and plateau_y+1 == ball_y or plateau_x+23 == ball_x and plateau_y+1 == ball_y or plateau_x+24 == ball_x and plateau_y-2 == ball_y or plateau_x+25 == ball_x and plateau_y+3 == ball_y or plateau_x+25 == ball_x and plateau_y+3 == ball_y:

        ball_velocity_x = abs(ball_velocity_x)
        ball_velocity_y = -abs(ball_velocity_y)

        return int(ball_velocity_x), int(ball_velocity_y)

    return int(ball_velocity_x), int(ball_velocity_y)



def timer(time, ball_velocity_x, ball_velocity_y):
    '''
    Cette fonction sert à augmenter la vitesse de la balle de au bout de 15s
    sachant de time augmente de 1 par 1/30s, à 15s ou 30s, timer sera à 450 ou 900
    la fonction n'est appelée que lorsque time est à 450 ou 900
    on augmente la vélocité de la balle y et en x si elle est toujours de 1
    This function return time, the ball's velocity x and y
    '''

    if ball_velocity_y == 1 :
        ball_velocity_y = ball_velocity_y + 1

    elif ball_velocity_y == -1:
        ball_velocity_y = ball_velocity_y-1


    if ball_velocity_x == 0 :
        ball_velocity_x = ball_velocity_x + random.choice([-1, 1])

    elif ball_velocity_x >= 1:
        ball_velocity_x = ball_velocity_x+1

    elif ball_velocity_x <= -1:
        ball_velocity_x = ball_velocity_x-1

    return time, ball_velocity_x, ball_velocity_y





# =========================================================
# == UPDATE
# =========================================================
def update():
    """
    mise à jour des variables (30 fois par seconde)
    vérification des états du jeu:
    mouvement de la balle
    selon l'ordonnée :
        collision avec une brique ?
        ou
        collision avec le plateau de jeu ?
    execution de la fonction du déplacement du plateau de jeu
    vérification du nombre de vies selon l'ordonnée de la balle
    """

    global plateau_x, plateau_y
    global briques_x, briques_y, ball_x, ball_y, ball_velocity_x, ball_velocity_y, brk_x, briques, value, plateau_velocity_x, score, time, life

    if life > 0:




        ball_x, ball_y, ball_velocity_x, ball_velocity_y = ball_mvt(ball_x, ball_y, ball_velocity_x, ball_velocity_y, plateau_velocity_x)


        if (ball_y == 34 or ball_y == 33) or ball_y+3 == 30:
            ball_x, ball_y, ball_velocity_x, ball_velocity_y, score = brique_check(ball_x, ball_y, brk_x, briques, ball_velocity_y, ball_velocity_x, score)

        elif 120<=ball_y<=123:
            ball_velocity_x, ball_velocity_y = plateau_check(ball_x, ball_y, ball_velocity_x, ball_velocity_y, plateau_x, plateau_y, plateau_velocity_x)




        # mise à jour de la position du vaisseau
        plateau_x, plateau_velocity_x = plateau_deplacement(plateau_x, plateau_velocity_x)

        life = life_is_ok(life, ball_y)


        #appel de la fonction si time est à 240 ou 40 (soit 8 et 15s)
        if time == 900 or time == 450:
            time, ball_velocity_x, ball_velocity_y = timer(time, ball_velocity_x, ball_velocity_y)
        time = time+1



# =========================================================
# == DRAW
# =========================================================
def draw():
    """
    création des objets (30 fois par seconde)
    dans l'ordre :
    afficher les vies restantes
    affichage du score
    construire les briques
    dessiner la balle
    afficher la plateau de jeu
    """

    # vide la fenetre
    pyxel.cls(0)



    if life > 0:
        if briques == [0, 0, 0, 0, 0, 0]:
            pyxel.text(50, 64, "VICTOIRE", 7)
            score_txt = "Score de " + str(score)
            pyxel.text(43, 100, score_txt, 7)

        else:

            #affiche le nombre de vies restantes
            vies_txt = 'Vies : ' + str(life)
            pyxel.text(54,1, vies_txt, 7)

            score_txt = str(score)
            pyxel.text(120,1, score_txt, 7)

            briques_x = 10
            briques_y = 30
            for i in range(len(briques)):
                if briques[i] != 0:
                    pyxel.rect(briques_x, briques_y, 15, 4, briques[i])
                briques_x = briques_x + 18

            #création de la balle de rayon 2
            pyxel.circ(ball_x, ball_y, 2, 7)

                # plateau (rect 20,4)
            pyxel.tri(plateau_x, plateau_y, plateau_x, plateau_y+3, plateau_x-4, plateau_y+3, 10)
            pyxel.rect(plateau_x, plateau_y, 20, 4, 10)
            pyxel.tri(plateau_x+20, plateau_y, plateau_x+20, plateau_y+3, plateau_x+24, plateau_y+3, 10)


    else:
        pyxel.text(50,64, 'GAME OVER', 7)



#execution des fonctions update et draw
pyxel.run(update, draw)
