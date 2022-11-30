import pyxel

# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(128, 128, title="Casse brique")

# position initiale du vaisseau
# (origine des positions : milieu bas)
plateau_x = 54
plateau_y = 120
briques = [1, 2, 3, 1, 2, 3]
#coordonnés des briques : de x = 4, y = 30 à x = 124, y = 40; hauteur = 10 largeur = 20
briques_x = 4
briques_y = 30

def plateau_deplacement(x):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        x = x + 3
        if (x > 108):
            x = 108
    if pyxel.btn(pyxel.KEY_LEFT):
        x = x - 3
        if (x < 0) :
            x = 0
   
    return x


# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global plateau_x, plateau_y, briques_x, briques_y

    # mise à jour de la position du vaisseau
    plateau_x = plateau_deplacement(plateau_x)


# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)

    # vaisseau (rect 20,4)
    pyxel.rect(plateau_x, plateau_y, 20, 4, 10)
    
    pyxel.rect(briques_x, briques_y, 20, 4, 9)

pyxel.run(update, draw)
