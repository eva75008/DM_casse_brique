import pyxel

# taille de la fenetre 128x128 pixels
pyxel.init(128, 128, title="Jeu de Casse Brique")

# position initiale du palet
# (origine des positions : milieu en bas)
plateau_x = 60
plateau_y = 120
briques = [1, 2, 3, 1, 2, 3]
#coordonnés des briques : de x = 4, y = 30 à x = 124, y = 40; hauteur = 10 largeur = 20
briques_x = 4
briques_y = 30

def plateau_deplacement(x):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 120) :
            x = x + 1
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 0) :
            x = x - 1
    return x


# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global plateau_x, plateau_y, brique_x, brique_y

    # mise à jour de la position du plateau
    plateau_x, plateau_y = plateau_deplacement(plateau_x, plateau_y)


# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)

    # plateau (carre 8x8)
    pyxel.rect(plateau_x, plateau_y, 8, 8, 1)
    # briques
    pyxel.rect(briques_x, briques_y, 19, 10, 9)

pyxel.run(update, draw)
