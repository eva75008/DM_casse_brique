import pyxel

# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(128, 128, title="Casse brique")

# position initiale du vaisseau
# (origine des positions : milieu bas)
plateau_x = 54
plateau_y = 120
plateau_flrm = [plateau_x, plateau_y, plateau_x, plateau_y, plateau_x, plateau_y, plateau_x, plateau_y, plateau_x, plateau_y, ]
plateau_flrm = [plateau_x-1, plateau_y, plateau_x-2, plateau_y+1, plateau_x-3, plateau_y+1, plateau_x-4, plateau_y-2, plateau_x-5, plateau_y+3, plateau_x-5, plateau_y+3]

briques = [1, 2, 3, 3, 2, 3]
brk_x = [10, 25, 28, 43, 46, 61, 64, 79, 82, 97, 100, 115]
#coordonnés des briques : de x = 4, y = 30 à x = 124, y = 40; hauteur = 10 largeur = 20
#6 ,  12 ,  9
briques_x = 10
briques_y = 30

ball_x = 64
ball_y = 100
ball_velocity_x = 1
ball_velocity_y = 1

life = 5


def plateau_deplacement(x):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        x = x + 3
        if (x > 108):x = 108
    if pyxel.btn(pyxel.KEY_LEFT):
        x = x - 3
        if (x < 0) :x = 0

    return x

def ball_mvt(x, y, ball_velocity_x, ball_velocity_y):
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
    """
    if ball_y > 128:
        life = life-1
    return life



def brique_check(ball_x, ball_y, brk_x, briques, ball_velocity_y, ball_velocity_x):
    """vérification que les briques sont retirées ou laissées à leurs places"""

    for n in range(0,10,2):

        if brk_x[n]<=ball_x<=brk_x[n+1] and briques[n//2] != 0:

            ball_velocity_y = abs(ball_velocity_y)

            briques[n//2] = briques[n//2] - 1
            print(ball_x,  ball_y, ball_velocity_x, ball_velocity_y)
            return int(ball_x),  int(ball_y), int(ball_velocity_x), int(ball_velocity_y)


          
def plateau_check(ball_x, ball_y, ball_velocity_x, ball_velocity_y, plateau_x, plateau_y):
    """
    Définission des collisions et des réponses à ses collisions avec le plateau de jeu
    """
    
  if plateau_x<=ball_x<=plateau_x+20:
    ball_velocity_y = -abs(ball_velocity_y)
    return int(ball_velocity_x), int(ball_velocity_y)
    
  elif plateau_x-1 == ball_x and plateau_y == ball_y or plateau_x-2 == ball_x and plateau_y+1 == ball_y or plateau_x-3 == ball_x and plateau_y+1 == ball_y or plateau_x-4 == ball_x and plateau_y-2 == ball_y or plateau_x-5 == ball_x and plateau_y+3 == ball_y or plateau_x-5 == ball_x and plateau_y+3 == ball_y:       
    ball_velocity_x = -abs(ball_velocity_x)    
    return int(ball_velocity_x), int(ball_velocity_y)
   
  #elif plateau_x-1, plateau_y == ball_x, ball_y or plateau_x-2, plateau_y+1 == ball_x, ball_y or plateau_x-3, plateau_y+1 == ball_x, ball_y or plateau_x-4, plateau_y-2 == ball_x, ball_y or plateau_x-5, plateau_y+3 == ball_x, ball_y or plateau_x-5, plateau_y+3:
 #   ball_velocity_x = -abs(ball_velocity_x)   
  
#  elif plateau_x+21, plateau_y == ball_x, ball_y or plateau_x+22, plateau_y+1 == ball_x, ball_y or plateau_x+23, plateau_y+1 == ball_x, ball_y or plateau_x+24, plateau_y-2 == ball_x, ball_y or plateau_x+25, plateau_y+3 == ball_x, ball_y or plateau_x+25, plateau_y+3:
 #   ball_velocity_x = abs(ball_velocity_x)         
          

        
        
        


# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global plateau_x, plateau_y
    global briques_x, briques_y, ball_x, ball_y, ball_velocity_x, ball_velocity_y, life, brk_x, briques


    if ball_y == 30 or ball_y == 34:
        ball_x, ball_y, ball_velocity_x, ball_velocity_y = brique_check(ball_x, ball_y, brk_x, briques, ball_velocity_y, ball_velocity_x)
    elif 120<=ball_y<=123: 
        ball_velocity_x, ball_velocity_y = plateau_check(ball_x, ball_y, ball_velocity_x, ball_velocity_y, plateau_x, plateau_y)


    ball_x, ball_y, ball_velocity_x, ball_velocity_y = ball_mvt(ball_x, ball_y, ball_velocity_x, ball_velocity_y)

    # mise à jour de la position du vaisseau
    plateau_x = plateau_deplacement(plateau_x)

    life = life_is_ok(life, ball_y)




# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)
    if life > 0:
        briques_x = 10
        briques_y = 30
        for i in range(len(briques)):
            if briques[i] != 0:
                pyxel.rect(briques_x, briques_y, 15, 4, briques[i])
            briques_x = briques_x + 18

        pyxel.circ(ball_x, ball_y, 3, 7)

            # plateau (rect 20,4)
        pyxel.tri(plateau_x, plateau_y, plateau_x, plateau_y+4, plateau_x-4, plateau_y+4, 10)
        pyxel.rect(plateau_x, plateau_y, 20, 4, 10)
        pyxel.tri(plateau_x+20, plateau_y, plateau_x+20, plateau_y+4, plateau_x+24, plateau_y+4, 10)


    else:
        pyxel.text(50,64, 'GAME OVER', 7)





pyxel.run(update, draw)
