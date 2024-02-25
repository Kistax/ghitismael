import pyxel
import time
import random




# Fonction pour centrer le texte
def center_text(text, char_width=pyxel.FONT_WIDTH):
    text_width = len(text) * char_width
    return (pyxel.width - text_width) / 2


        



# Ajout des variables pour le chronomètre
start_time = 0
elapsed_time = 0
speed = 1
score = 0
victoire_coordinates=-600
sol_y = 108
fin_des_plateformes_atteinte = False




#===========================================
#               PLATEFORME
#===========================================
class Plateforme:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self, speed):
        # Ajuste la position en fonction de la vitesse
        self.x -= speed

    def draw(self):
        # Dessine la plateforme (à adapter selon votre ressource graphique)
        pyxel.blt(self.x, self.y,0, 0, 50, 48, 13, 12 )









#===========================================
#               DECOR
#===========================================
class Decor:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def update(self, speed):
        # Ajuste la position en fonction de la vitesse
        self.x -= speed

    def draw(self):
        # Dessine le décor
        pyxel.blt(0, pyxel.height - 16, 0, 0, 48, 16, 16, 0)


def creation_ennemis(ennemis_liste):
    """Création des ennemis avec un grand espacement au début"""
    max_espacement = 60  # Espacement maximal entre les ennemis
    min_espacement = 40  # Espacement minimal entre les ennemis
    espacement = max(max_espacement - len(ennemis_liste), min_espacement)

    if pyxel.frame_count % espacement == 0:
        ennemis_liste.append([120, sol_y - 8])  # Position fixe pour tous les ennemis

    return ennemis_liste





def ennemi_deplacement(ennemis_liste):
    """Déplacement des ennemis vers la gauche et suppression s'ils sortent du cadre"""
    for ennemi in ennemis_liste:
        ennemi[0] -= 1  # Ajuste la position en fonction de la direction (vers la gauche)
        if ennemi[0] < 0:
            ennemis_liste.remove(ennemi)  # Supprime l'ennemi s'il sort du cadre
    return ennemis_liste

distance = 0
sol_y = 108





#===========================================
#               UPDATE
#===========================================
def update():
    global personnage_x, personnage_y, is_jumping, jump_height, gravity, phase, fond_x, direction, start_time, elapsed_time, ennemis_liste, nombre_de_vies, distance, compteurennemiskill, speed

    # création d'ennemis
    ennemis_liste = creation_ennemis(ennemis_liste)

    # mise à jour des positions des ennemis
    ennemis_liste = ennemi_deplacement(ennemis_liste)

    # Calcul de la distance parcourue en fonction de la position du personnage
    distance_parcourue = personnage_x - 64  # 64 est la position initiale du personnage


    # Calcul du score en fonction de la distance parcourue et du temps
    score = int(distance_parcourue / 10 + elapsed_time)

    if phase == 0:
        if pyxel.btnp(pyxel.KEY_SPACE):
            phase = 1
            start_time = time.time()  # Enregistre le temps de début
            nombre_de_vies = 5
    elif phase == 1:
        speed = 1  # Ajustez la vitesse selon vos besoins
        
        distance += abs(speed)

        if pyxel.btn(pyxel.KEY_RIGHT):
            direction = 1  # Personnage regarde à droite
            fond_x -= speed  # Déplacement du fond vers la gauche (inverse par rapport au code précédent)
            # Mise à jour des plateformes uniquement si le personnage avance
            for platform in platforms:
                platform.update(speed)
            # Mise à jour des trous uniquement si le personnage avance

            # Mise à jour des décors uniquement si le personnage avance
            for decor in decors:
                decor.update(speed)

        elif pyxel.btn(pyxel.KEY_LEFT):
            direction = -1  # Personnage regarde à gauche
            fond_x += speed  # Déplacement du fond vers la droite (inverse par rapport au code précédent)
            # Mise à jour des plateformes uniquement si le personnage recule
            for platform in platforms:
                platform.update(-speed)

            # Mise à jour des décors uniquement si le personnage recule
            for decor in decors:
                decor.update(-speed)

        if pyxel.btnp(pyxel.KEY_SPACE):
            personnage_y = personnage_y - 2

        if pyxel.btnp(pyxel.KEY_S):
            pyxel.quit()

        # Gestion du saut
        if pyxel.btnp(pyxel.KEY_SPACE) and not is_jumping:
            is_jumping = True
            jump_height = 10  # Réinitialise la hauteur de saut

        if is_jumping:
            personnage_y -= jump_height
            jump_height -= gravity

        # Si le personnage atteint le sol, arrête le saut
        if personnage_y > sol_y:
            is_jumping = False
            jump_height = 20
            personnage_y = sol_y

        # Gestion de la gravité lorsque le personnage n'est pas en saut
        if not is_jumping and personnage_y < sol_y:
            personnage_y += gravity

        # Si le personnage a atteint la hauteur maximale du saut, arrête le saut
        if jump_height < -10:
            is_jumping = False
            jump_height = 20
        if personnage_y < 92:
            personnage_y = personnage_y + gravity
        else:
            personnage_y = 92

        if personnage_y > sol_y:
            personnage_y = sol_y

        # Ajout du chronomètre
        elapsed_time = time.time() - start_time

        # Gestion de la collision avec les plateformes
        for platform in platforms:
            if (
                personnage_x < platform.x + platform.width
                and personnage_x + 16 > platform.x
                and personnage_y + 16 > platform.y
                and personnage_y < platform.y + platform.height
            ):
                # Le personnage est sur une plateforme, ajuste sa position
                personnage_y = platform.y - 16

        for ennemi in ennemis_liste:
            if (
                    personnage_x < ennemi[0] + 8
                    and personnage_x + 16 > ennemi[0]
                    and personnage_y + 16 > ennemi[1]
                    and personnage_y < ennemi[1] + 8
            ):
                # Le personnage entre en collision avec l'ennemi
                if is_jumping:
                    # Réussite du saut, retire l'ennemi
                    ennemis_liste.remove(ennemi)
                    compteurennemiskill = compteurennemiskill + 1
                else:
                    # Échec du saut, réinitialise le jeu
                    nombre_de_vies = nombre_de_vies - 1
                    personnage_x = personnage_x - 10
                    personnage_y = personnage_y - 10

        if nombre_de_vies == 0:
            game_over()
        if fond_x == victoire_coordinates:
            phase = 3

    elif phase == 2:
        game_over()
    if phase == 3:
        victoire(elapsed_time) 


             
        



#===========================================
#               DRAW
#===========================================
def draw():
    global  fin_des_plateformes_atteinte 
    # Vide la fenêtre avec un fond bleu
    fin_des_plateformes_atteinte = False
    pyxel.cls(12)
    # Dessine l'image de fond

    if phase == 0:
        title = "ATTEIGNEZ LA MONTAGNE BLEUE !"
        press_enter_text = "Appuies ESPACE"
        pyxel.text(center_text(title), pyxel.height / 3, title, 7)
        pyxel.text(center_text(press_enter_text), pyxel.height / 2, press_enter_text, 7)
    elif phase == 1:

        # Dessine le sol
       
        pyxel.rect(200, sol_y, 20, 20, 7)  # Carré spécifique qui deviendra noir et blanc
        
        # Calcul de la distance parcourue en fonction de la position du personnage
        distance_parcourue = personnage_x - 64  # 64 est la position initiale du personnage

        # Calcul du score en fonction de la distance parcourue et du temps
        score = int(distance_parcourue / 10 + elapsed_time)

        
        

        # Dessine la montagne grise qui avance de la droite vers la gauche
        pyxel.line(0 + fond_x, 120, 64 + fond_x, 60, 11)  # Ligne gauche
        pyxel.line(64 + fond_x, 60, 128 + fond_x, 120, 11)  # Ligne droite
        pyxel.tri(0 + fond_x, 120, 64 + fond_x, 60, 128 + fond_x, 120, 11)  # Triangle pour remplir l'intérieur

        # Dessine la deuxième montagne
        pyxel.line(50 + fond_x, 120, 100 + fond_x, 80, 11)
        pyxel.line(100 + fond_x, 80, 150 + fond_x, 120, 11)
        pyxel.tri(50 + fond_x, 120, 100 + fond_x, 80, 150 + fond_x, 120, 11)

        pyxel.line(120 + fond_x, 120, 170 + fond_x, 90, 11)
        pyxel.line(170 + fond_x, 90, 220 + fond_x, 120, 11)
        pyxel.tri(120 + fond_x, 120, 170 + fond_x, 90, 220 + fond_x, 120, 11)

        # Dessine la quatrième montagne
        pyxel.line(180 + fond_x, 120, 230 + fond_x, 100, 11)
        pyxel.line(230 + fond_x, 100, 280 + fond_x, 120, 11)
        pyxel.tri(180 + fond_x, 120, 230 + fond_x, 100, 280 + fond_x, 120, 11)

        # Dessine la cinquième montagne (nouvelle)
        pyxel.line(240 + fond_x, 120, 290 + fond_x, 80,  11)
        pyxel.line(290 + fond_x, 80, 340 + fond_x, 120, 11)
        pyxel.tri(240 + fond_x, 120, 290 + fond_x, 80, 340 + fond_x, 120, 11)

        # Dessine la sixième montagne (nouvelle)
        pyxel.line(300 + fond_x, 120, 350 + fond_x, 90, 11)
        pyxel.line(350 + fond_x, 90, 400 + fond_x, 120, 11)
        pyxel.tri(300 + fond_x, 120, 350 + fond_x, 90, 400 + fond_x, 120, 11)

        # Dessine la septième montagne (nouvelle)
        pyxel.line(360 + fond_x, 120, 410 + fond_x, 100, 11)
        pyxel.line(410 + fond_x, 100, 460 + fond_x, 120, 11)
        pyxel.tri(360 + fond_x, 120, 410 + fond_x, 100, 460 + fond_x, 120, 11)

        # Dessine la huitième montagne
        pyxel.line(420 + fond_x, 120, 470 + fond_x, 80, 11)
        pyxel.line(470 + fond_x, 80, 520 + fond_x, 120, 11)
        pyxel.tri(420 + fond_x, 120, 470 + fond_x, 80, 520 + fond_x, 120, 11)

        # Dessine la neuvième montagne
        pyxel.line(480 + fond_x, 120, 530 + fond_x, 90, 11)
        pyxel.line(530 + fond_x, 90, 580 + fond_x, 120, 11)
        pyxel.tri(480 + fond_x, 120, 530 + fond_x, 90, 580 + fond_x, 120, 11)

        # Dessine la dixième montagne
        pyxel.line(540 + fond_x, 120, 590 + fond_x, 100, 11)
        pyxel.line(590 + fond_x, 100, 640 + fond_x, 120, 11)
        pyxel.tri(540 + fond_x, 120, 590 + fond_x, 100, 640 + fond_x, 120, 11) 

        # Dessine la dixième montagne
        pyxel.line(580 + fond_x, 120, 640 + fond_x, 110, 11)
        pyxel.line(650 + fond_x, 110, 700 + fond_x, 150, 11)
        pyxel.tri(600 + fond_x, 120, 650 + fond_x, 110, 640 + fond_x, 120, 11)

        # Dessine la dixième montagne
        pyxel.line(580 + fond_x, 120, 640 + fond_x, 110, 11)
        pyxel.line(650 + fond_x, 110, 700 + fond_x, 150, 11)
        pyxel.tri(600 + fond_x, 120, 650 + fond_x, 110, 640 + fond_x, 120, 11)

        # Dessine la nouvelle montagne grise qui avance de la droite vers la gauche
        pyxel.line(620 + fond_x, 120, 670 + fond_x, 80, 5)
        pyxel.line(670 + fond_x, 80, 720 + fond_x, 120, 5)
        pyxel.tri(620 + fond_x, 120, 670 + fond_x, 80, 720 + fond_x, 120, 5)




        # Dessine le sol vert
        pyxel.rect(sol_x, sol_y, 256, 20, 3)

        # Dessine les plateformes
        for platform in platforms:
            platform.draw()

        


          
        
         
        

        # Dessine le personnage centré avec des limites pour éviter les dépassements
        personnage_x_clipped = max(0, min(120 - 14, personnage_x))
        personnage_y_clipped = max(0, min(128 - 16, personnage_y))
        pyxel.blt(personnage_x_clipped, personnage_y_clipped, 0, 0, 0, direction * 16, 16, 0)
        
        # Dessine le soleil dans le coin gauche
        pyxel.circ(16, 16, 8, 10)

        # dessine l'ennemi
        for ennemi in ennemis_liste:
            pyxel.blt(ennemi[0], ennemi[1], 0, 0, 17, 31, 13, 0 )

        # Affiche le chronomètre à droite
        chrono_text = f"Temps : {int(elapsed_time)}s"
        text_x = pyxel.width - len(chrono_text) * pyxel.FONT_WIDTH - 5
        pyxel.text(text_x, 5, chrono_text, 7)

        score_text = f"Score : {score}"
        score_text_x = pyxel.width - len(score_text) * pyxel.FONT_WIDTH - 5
        pyxel.text(score_text_x, 20, score_text, 7)


        pyxel.text(5, 5, f"Vies: {nombre_de_vies}", 7) #Affichage compteur de vies
        ennemis_killed_text = f"Ennemis tués : {compteurennemiskill}"
        ennemis_killed_text_x = pyxel.width - len(ennemis_killed_text) * pyxel.FONT_WIDTH - 5
        pyxel.text(ennemis_killed_text_x, 50, ennemis_killed_text, 7) #Affiche compteur d'ennemis tuées
    elif phase == 2:
        game_over()
    if phase == 3:
        victoire(elapsed_time) 




pyxel.init(128, 128, title="Nuit du code")

sol_x = 0
sol_y = 108

personnage_x = 64
personnage_y = 92
fond_x = 0
direction = 1  # Direction initiale (droite)
pyxel.load("mario.pyxres")
is_jumping = False
jump_height = 10
gravity = 1
phase = 0  # Menu 0, jeu 1 , def
nombre_de_vies = 0
victoire_coordinates = -600
drapeau_x = 600
drapeau_y = sol_y - 60
maisonnette_x = drapeau_x + 20
maisonnette_y = sol_y - 20        
compteurennemiskill = 0
 


# Plateformes
platforms = [
    # Plateforme(200, sol_y - 30, 50, 5),
    # Plateforme(300, sol_y - 30, 40, 5),
    Plateforme(220, sol_y - 30, 50, 5),
    Plateforme(400, sol_y - 30, 40, 5),
    Plateforme(500, sol_y - 30, 40, 5),
]





# Décors
decors = []

# Liste des ennemis
ennemis_liste = []

# Fonction pour réinitialiser le jeu
def game_over():
    global phase
    phase = 2  # Change la phase pour indiquer que le jeu est terminé
    
    

    messages = [
        "Vous avez ete ",
        "capture par l'armee",
        "de GALVAX"
        
    ]
    y_position = 35
    for message in messages:
        pyxel.text(10, y_position, message, 8)
        y_position += 10
    pyxel.text(7,20, 'Clique R pour recommencer', 1)
    if pyxel.btnp(pyxel.KEY_R):
        reset_game()
    

# Ajoute la fonction reset_game() pour réinitialiser le jeu après un Game Over
def reset_game():
    global personnage_x, personnage_y, is_jumping, jump_height, start_time, elapsed_time, phase,fond_x,platforms,decors,ennemis_liste,sol_x,sol_y
    sol_x = 0
    sol_y = 108
    personnage_x = 64
    personnage_y = 92
    fond_x = 0
    direction = 1  # Direction initiale (droite)
    pyxel.load("Mario.pyxres")
    is_jumping = False
    jump_height = 10
    gravity = 1
    phase = 0  # Menu 0, jeu 1 , def
    nombre_de_vies = 0
    victoire_coordinates = -600
    compteurennemiskill = 0
    


      

    # Décors
    decors = []

    # Liste des ennemis
    ennemis_liste = []
    phase = 0  # Revient à l'écran de menu


def victoire(elapsed_time):
    global phase
    phase = 3  # Changer la phase du jeu pour l'écran de victoire
    pyxel.cls(12)  # Effacer l'écran

    pyxel.text(10, 25, "VICTOIRE !", 5)

    messages = [
        "SAID LE CONQUERENT a reussi",
        "a rentrer chez lui",
        "il a retrouve sa famille",
        "et a cree une armee",
        "et a vaincu l'armée de Valvax",
        
    ]

    y_position = 35
    for message in messages:
        pyxel.text(10, y_position, message, 8)
        y_position += 10

    elapsed_time_text = f"Temps écoulé : {int(elapsed_time)}s"
    pyxel.text(10, y_position, elapsed_time_text, 8)  # Utiliser une couleur différente pour le temps

    
    
    if pyxel.btnp(pyxel.KEY_SPACE):
        phase = 0  # Revenir au menu principal
        reset_game()  # Réinitialiser le jeu



# Lancer la boucle principale
pyxel.run(update, draw)