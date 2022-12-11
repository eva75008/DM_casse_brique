import pyxel
import random


class App:
    def __init__(self):
        """
        fonction d'initialisation des variables
        taille de l'écran, nombre de briques, vies, score, durabilité des briques,...
        """
        self.screen_length = 300
        self.screen_width = 300
        pyxel.init(self.screen_length, self.screen_width, title="K ç Brique")
        self.score = 0
        self.life = 5
        self.is_alive = True

        self.ball_x = self.screen_width//2-1
        self.ball_y = self.screen_length//2-1

        self.ball_velocity_x = random.randint(-1, 1)
        self.ball_velocity_y = random.choice([-1,1])


        self.player_dy = 0


        # position initiale du vaisseau
        # (origine des positions : milieu bas)
        self.plateau_x = (self.screen_width//2)-7
        self.plateau_y = 280
        self.plateau_velocity_x = 0



        self.nb_briques = (self.screen_width-10)//18
        #crée deux listes de n nombre entiers aléatoires entre 1 et 3 représentant les durabilités des briques dans une liste
        self.briques = [[random.randint(1,3) for i in range(self.nb_briques)], [random.randint(1,3) for i in range(self.nb_briques)]]


        """self.brk_x = [10, 25, 28, 43, 46, 61, 64, 79, 82, 97, 100, 115]"""
        #coordonnés des briques : de x = 4, y = 30 à x = 124, y = 40; hauteur = 10 largeur = 20
        #6 ,  12 ,  9
        self.briques_x = 10
        self.briques_y = 50

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        """
        s'actualise 30 fois par secondes,

        permet de quitter le jeu en appuyant sur la touche Q

        calcul le déplacement de la balle et du plateau
        et calcul d'une éventuelle collision entre balle, briques ou balle, plateau selon l'ordonnée de la balle
        """

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_plateau()

        self.update_ball()

#appel de la fontion qui permet de gerer une collion avec le plateau lorsque la balle est en bas
        if 278<=self.ball_y<=282:
            self.update_coll_plateau()

#appel de la fontion qui permet de gerer une collion avec les briques lorsque la balle est en haut
        if 73<=self.ball_y<=76 or 69<=self.ball_y<=72 or 53<=self.ball_y<=56 or 48<=self.ball_y<=52:
            self.update_coll_briques()



    def update_plateau(self):
        """
        déplacement avec les touches de directions
        déplacement latéral du plateau avec une vitesse de 3
        sauf lorsque le plateau est en bordure
        si aucun mouvement, vitesse du plateau en x est 0
        """
        if pyxel.btn(pyxel.KEY_LEFT):
            self.plateau_velocity_x = -(self.screen_width//60)
            self.plateau_x += self.plateau_velocity_x
            if (self.plateau_x < 3) :self.plateau_x = 3
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.plateau_velocity_x = self.screen_width//60
            self.plateau_x += self.plateau_velocity_x

            if (self.plateau_x > self.screen_length-23):self.plateau_x = self.screen_length-23
        else:
            plateau_velocity_x = 0




    def update_coll_plateau(self):
        """
        Définission des collisions et des réponses à ses collisions avec le plateau de jeu
        soit le milieu
        soit la balle est sur le bord gauche
        soit le bord droit
        soit aucun des trois
        """

        if self.plateau_x<=self.ball_x<=self.plateau_x+20:

            if self.ball_velocity_x < 5 and self.ball_velocity_x > -5 and (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT)):
                self.ball_velocity_x = self.ball_velocity_x + (self.plateau_velocity_x//5)

            self.ball_velocity_y = -abs(self.ball_velocity_y)

#lors d'une collision avec le bord gauche, rebond vers le haut et la gauche
        #elif self.plateau_x-1 == self.ball_x and self.plateau_y == self.ball_y or self.plateau_x-2 == self.ball_x and self.plateau_y+1 == self.ball_y or self.plateau_x-3 == self.ball_x and self.plateau_y+1 == self.ball_y or self.plateau_x-4 == self.ball_x and self.plateau_y-2 == self.ball_y or self.plateau_x-5 == self.ball_x and self.plateau_y+3 == self.ball_y or self.plateau_x-5 == self.ball_x and self.plateau_y+3 == self.ball_y:

        elif self.plateau_x-4 <= self.ball_x <= self.plateau_x and self.plateau_y <= self.ball_y <= self.plateau_y+4:


            self.ball_velocity_x = -abs(self.ball_velocity_y)
            self.ball_velocity_y = -abs(self.ball_velocity_x)



#lors d'une collision avec le bord droit, rebond vers le haut et la droite
        #elif self.plateau_x+21 == self.ball_x and self.plateau_y == self.ball_y or self.plateau_x+22 == self.ball_x and self.plateau_y+1 == self.ball_y or self.plateau_x+23 == self.ball_x and self.plateau_y+1 == self.ball_y or self.plateau_x+24 == self.ball_x and self.plateau_y-2 == self.ball_y or self.plateau_x+25 == self.ball_x and self.plateau_y+3 == self.ball_y or self.plateau_x+25 == self.ball_x and self.plateau_y+3 == self.ball_y:

        elif self.plateau_x+20 <= self.ball_x <= self.plateau_x+24 and self.plateau_y <= self.ball_y <= self.plateau_y+4:

            self.ball_velocity_x = abs(self.ball_velocity_y)
            self.ball_velocity_y = -abs(self.ball_velocity_x)






    def update_coll_briques(self):
        """
        vérification que les briques sont retirées ou laissées à leurs places
        selon :
        si la balle arrive par le bas:
            retirer la brique et rebondir vers le bas
        si la balle arrive par le haut:
            retirer la brique et rebondir vers le haut
            
        La balle peut passer entre les briques 
        """

        #calcul la brique touchée
        coll = int((self.ball_x - 10) / 18)
        #test si la balle arrive par le bas sur la 2eme ligne et réduit la durabilité de la brique
        if self.ball_velocity_y < 0 and 73<=self.ball_y<=76 and self.ball_x < self.screen_width-2 and self.briques[1][coll] != 0:


            if 10+18*(coll)<=self.ball_x<=10+18*(coll)+15:

                self.ball_velocity_y = abs(self.ball_velocity_y)
                if self.ball_velocity_y < 4:
                    #augmente la vitesse verticale de la balle
                    self.ball_velocity_y+= 1
#diminue la durabilité de la brique de 1
                self.briques[1][coll] = self.briques[1][coll] - 1
                #augmente le score de 10 suite à la collision
                self.score = self.score + 10


        #test si la balle arrive par le haut sur la 2eme ligne et réduit la durabilité de la brique
        elif self.ball_velocity_y > 0 and 69<=self.ball_y<=72 and self.ball_x < self.screen_width-2 and self.briques[1][coll] != 0:

            if 10+18*(coll)<=self.ball_x<=10+18*(coll)+15:

                self.ball_velocity_y = -abs(self.ball_velocity_y)

                self.briques[1][coll] = self.briques[1][coll] - 1
                self.score = self.score + 10



        #test si la balle arrive par le bas sur la 1ere ligne et réduit la durabilité de la brique
        elif self.ball_velocity_y < 0 and 53<=self.ball_y<=56 and self.ball_x < self.screen_width-2 and self.briques[0][coll] != 0:
            if 10+18*(coll)<=self.ball_x<=10+18*(coll)+15:

                self.ball_velocity_y = abs(self.ball_velocity_y)

                self.briques[0][coll] = self.briques[0][coll] - 1
                self.score = self.score + 10


        #test si la balle arrive par le haut sur la 1ere ligne et réduit la durabilité de la brique
        elif self.ball_velocity_y > 0 and 48<=self.ball_y<=52 and self.ball_x < self.screen_width-2 and self.briques[0][coll] != 0:

            if 10+18*(coll)<=self.ball_x<=10+18*(coll)+15:

                self.ball_velocity_y = -abs(self.ball_velocity_y)

                self.briques[0][coll] = self.briques[0][coll] - 1
                self.score = self.score + 10









    def update_ball(self):
        """
        Cette fonction définie la trajectoire et la position de la balle
        La vélocité de la balle ne peut diminuer donc elle augmente avec le temps
        Elle retourne les coordonnées et les velocités de la balle
        """
#change les coordonnées de la balle selon la vitesse indiquée
        self.ball_x = self.ball_x + self.ball_velocity_x
        self.ball_y = self.ball_y + self.ball_velocity_y


        if self.ball_x < 0:
            #gestion de la collision avec le bord gauche
            self.ball_velocity_x = abs(self.ball_velocity_x)

        elif self.ball_x > self.screen_width:
            #gestion de la collision avec le bord droit
            self.ball_velocity_x = -abs(self.ball_velocity_x)

        if self.ball_y < 0:
            #gestion de la collision avec le haut
            self.ball_velocity_y = abs(self.ball_velocity_y)

        elif self.ball_y > self.screen_length:
            #gestion de la collision avec le bas
            self.ball_velocity_y = -abs(self.ball_velocity_y)
            #retire de la vie car la balle n'a pas été renvoiée par le joueur
            self.life -= 1
            if self.life == 0:
                #définie la défaite du joueur car in n'a plus de vie
                self.is_alive = False


    def draw(self):
        """
        Dessin des objets:

        affichage de la victoire ou de la défaite

        ou de la vie et du score en haut
           puis construction des briques
           consruction de la balle
           du plateau avec les triangles sur les cotés et le rectangle du centre
        """
        pyxel.cls(0)

        if self.is_alive:
            if self.briques == [0, 0, 0, 0, 0, 0]:
                pyxel.text(50, 64, "VICTOIRE", 7)
                score_txt = "Score de " + str(self.score)
                pyxel.text(43, 100, score_txt, 7)

            else:

                #affiche le nombre de vies restantes
                vies_txt = 'Vies : ' + str(self.life)
                pyxel.text(54,1, vies_txt, 7)
                #affiche le score en temps réel
                score_txt = str(self.score)
                pyxel.text(120,1, score_txt, 7)

                #construction des briques
                self.briques_x = 10
                self.briques_y = 50
                for j in range(len(self.briques)):

                    for i in range(len(self.briques[j])):
                        color = [0, 1, 5, 12]
                        if self.briques[j][i] != 0:
                            pyxel.rect(self.briques_x, self.briques_y, 15, 4, color[self.briques[j][i]])
                        self.briques_x = self.briques_x + 18
                    self.briques_x = 10
                    self.briques_y = 70


                #création de la balle de rayon 2
                pyxel.circ(self.ball_x, self.ball_y, 2, 7)

                    #création du plateau (rect 20,4) dont deux triangles autours
                pyxel.tri(self.plateau_x, self.plateau_y, self.plateau_x, self.plateau_y+3, self.plateau_x-4, self.plateau_y+3, 10)
                pyxel.rect(self.plateau_x, self.plateau_y, 20, 4, 10)
                pyxel.tri(self.plateau_x+20, self.plateau_y, self.plateau_x+20, self.plateau_y+3, self.plateau_x+24, self.plateau_y+3, 10)


        else:
            #affiche l'écran de fin
            pyxel.text(self.screen_width//2-20,self.screen_length//2-4, 'GAME OVER', 7)

App()
