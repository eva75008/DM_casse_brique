import pyxel

# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(128, 128, title="Casse brique")

# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 54
vaisseau_y = 120

def vaisseau_deplacement(x):
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

    global vaisseau_x, vaisseau_y, 

    # mise à jour de la position du vaisseau
    vaisseau_x = vaisseau_deplacement(vaisseau_x)


# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)

    # vaisseau (rect 20,4)
    pyxel.rect(vaisseau_x, vaisseau_y, 20, 4, 10)

pyxel.run(update, draw)
