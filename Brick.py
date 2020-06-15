import pygame # Pour La Fenetre de jeu
import os # Pour importer des fichiers
import random # Pour le spawn des Ennemies aléatoires
import time # Pour le timer qui servira a vérifier les actions dans le jeu
pygame.init()

# Ecran
WIDTH = 1920 #Largeur Ecran
HEIGHT = 1080 # Hauteur Ecran
style = pygame.font.Font("assets/fonts/pixel.ttf", 50) #Style Ecriture
style_small = pygame.font.Font("assets/fonts/pixel.ttf", 30)

#Def Image du jeu
Background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT)) # Fond D'écran + Scale selon Largeur Longueur ecran pour cover tout l'écran
Player_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Player.png")), (100, 100))
Ennemie_G = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Ennemie_G.png")), (100, 100))
Ennemie_V = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Ennemie_V.png")), (100, 100))
Boss = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Boss.png")), (75,75))
img_Laser = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Laser.png")), (10,10))

#Def Son Du Jeu
musique_menu = pygame.mixer.Sound(os.path.join("assets", "musique_menu.wav"))
shoot_sound = pygame.mixer.Sound(os.path.join("assets", "shoot.wav"))
kill_sound = pygame.mixer.Sound(os.path.join("assets", "kill.wav"))

#Parametres
credit_joueur = 0
FPS = 60 # Nombre de tick du timer 60 = On verifie 60 fois par seconde
timer = pygame.time.Clock() # Variable contenenant le timer
level = 0
Vie = 1
kill = 0
vitesse = 20 #vitesse de déplacement
vitesse_laser = 30
vitesse_ennemie = 1
tir_rapide = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))  #pygame.FULLSCREEN) # Initialisation Fenetre
pygame.display.set_caption('Brick Shooter YNOV') #Titre Fenetre

#Classes  du jeu

class Acteur: #Classe principal dont heriteront le joueur et les ennemies
    global tir_rapide
    COUNT = 0
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.img = Player_img
        self.laser_img = img_Laser
        self.laser_list = []
    def spawn(self, screen):
        screen.blit(self.img, (self.x -30, self.y))
        for laser in self.laser_list:
            laser.spawn(screen)

    def get_height(self):
        return self.img.get_height()

    def get_width(self):
        return self.img.get_width()

    def tirer(self):
        if self.COUNT >= tir_rapide: #Boucle pour Vitesse de Tir Joueur
            self.COUNT = 0
            laser = Laser(self.x, self.y, self.laser_img)
            self.laser_list.append(laser)
            shoot_sound.play()
        else:
            self.COUNT += 1


    def move_lasers(self, vitesse, acteur):
        for laser in self.laser_list:
            laser.move(vitesse)
            if laser.off_screen(HEIGHT):
                self.laser_list.remove(laser)
            elif laser.destroy(acteur):
                acteur.health -= 50
                self.laser_list.remove(laser)
                
#Classe Joueur
class Player(Acteur):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img = Player_img
        self.laser = img_Laser
        self.mask = pygame.mask.from_surface(self.img) #Le mask est une fonction pygame qui definit la limite d'une image pour detecter des collisions au pixel près
        #self.max_health = health


    def move_lasers(self, vitesse, acteurs): #Fonction Laser Joueur qui vérifie si collision avec autre acteur(Ennemie) et supprime l'ennemie si Collision
        global credit_joueur
        global kill
        for laser in self.laser_list:
            laser.move(vitesse_laser)
            if laser.off_screen(HEIGHT):
                self.laser_list.remove(laser)
            else:
                for acteur in acteurs:
                    if laser.destroy(acteur):
                        acteurs.remove(acteur)
                        credit_joueur += 25
                        kill += 1
                        kill_sound.play()
                        self.laser_list.remove(laser)

#Classe Ennemies
class Ennemie(Acteur):
    #Choisir le type d'ennemi
    ENNEMY_TYPE = {
        "green": (Ennemie_G, img_Laser),
        "violet": (Ennemie_V, img_Laser),
        "boss" : (Boss, img_Laser)
    }
    def __init__(self, x, y, type, health=100):
        super().__init__(x, y, health)
        self.health = health
        self.img, self.laser = self.ENNEMY_TYPE[type]
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, vitesse):
        global vitesse_ennemie
        self.y += vitesse

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def spawn(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self, vitesse):
        self.y -= vitesse
    def destroy(self, acteur):
        return IntersectWith(self, acteur)

    def off_screen(self, HEIGHT):
        return not(self.y <= HEIGHT and self.y >= 0)

#Fonction pour les collisions entre acteur
def IntersectWith(acteur1, acteur2):
    
    distance_x = int(acteur2.x - acteur1.x)
    distance_y = int(acteur2.y - acteur1.y)
    return acteur1.mask.overlap(acteur2.mask, (distance_x, distance_y)) != None

#Fonction Menu Principal
def main_menu():
    # musique_menu.stop() 
    # musique_menu.play() #Jouer la Musique
    run = True
    while run:
        screen.blit(Background,(0,0))
        title = style.render("MENU PRINCIPAL", 1, (255,0,0)) 
        play = style_small.render("Jouer", 1, (0,0,0))
        instruction = style_small.render("Instructions", 1, (0,0,0))
        boutique = style_small.render("Boutique", 1, (0,0,0))
        button_1 = pygame.Rect(WIDTH/3-play.get_width(), 440, play.get_width() + 20, play.get_height()) 
        button_2 = pygame.Rect(873, 440, instruction.get_width(), instruction.get_height())
        button_3 = pygame.Rect(1280, 440, boutique.get_width(), boutique.get_height())
        mx, my = pygame.mouse.get_pos() #Obtenir position Curseur Souris
        for event in pygame.event.get():
            if button_1.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN: #Si le Bouton de la souris est pressé et que le curseur est au dessus du "button_1"
                    main()
            if button_2.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Instructions()
            if button_3.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Boutique()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        #Affichage Boutton + Texte
        pygame.draw.rect(screen, (81, 101, 240), button_1)
        pygame.draw.rect(screen, (81, 101, 240), button_2)
        pygame.draw.rect(screen, (81, 101, 240), button_3)
        screen.blit(play, (WIDTH/3-play.get_width()+10, 440))
        screen.blit(instruction, (875, 440))
        screen.blit(boutique, (1280, 440))
        screen.blit(title, (960-title.get_width()/2, 200))
        pygame.display.update()

def Instructions():
    run = True
    while run:
        screen.blit(Background, (0,0))
        sous_menu_1 = style.render("Deplacements = Fleches / Espace = Tirer / Echap = Menu", 1, (255,0,0))
        sous_menu_2 = style.render("Si un Invader atteint le bas de l'écran vous avez Perdu", 1, (255,0,0))
        sous_menu_3 = style.render("Si vous touchez un Invader vous perdez une vie",1, (255,0,0))
        screen.blit(sous_menu_1, (WIDTH/2 - sous_menu_1.get_width()/2, HEIGHT/2-sous_menu_1.get_height()))
        screen.blit(sous_menu_2, (WIDTH/2 - sous_menu_2.get_width()/2, HEIGHT/2+sous_menu_1.get_height()))
        screen.blit(sous_menu_3, (WIDTH/2 - sous_menu_3.get_width()/2, HEIGHT/2+sous_menu_2.get_height()*2))
        button_1 = pygame.Rect(20, 20, 200, 50)
        back = style_small.render("Retour", 1, (0,0,0))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if button_1.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_menu()
        #Affichage Bouton + Texte
        pygame.draw.rect(screen, (81, 101, 240), button_1)
        screen.blit(back, (80, 20))
        pygame.display.update()

#Fonction Boutique
def Boutique():
    global credit_joueur
    global vitesse
    global Vie
    global tir_rapide
    run = True
    while run:
        mx, my = pygame.mouse.get_pos()

        title_boutique = style.render("Boutique", 1, (255,0,0))
        back = style_small.render("Retour", 1, (0,0,0))
        credit_boutique = style.render(f"Credit: {credit_joueur}", 1, (255,0,0))
        menu_boutique_1 = style.render("Vitesse de deplacement Acceleree(Joueur) -100 Credits",1 , (255,0,0))
        menu_boutique_2 = style.render("1 Vie 50 Credits", 1, (255,0,0))
        menu_boutique_3 = style.render("Tir GIGA RAPIDE", 1, (255,0,0))

        button_1 = pygame.Rect(WIDTH/2-menu_boutique_1.get_width()/2,HEIGHT/2,menu_boutique_1.get_width(), menu_boutique_1.get_height())
        button_back = pygame.Rect(20, 20, back.get_width(), back.get_height())
        button_2 = pygame.Rect(WIDTH/2-menu_boutique_2.get_width()/2,HEIGHT/2+menu_boutique_1.get_height()*2,menu_boutique_2.get_width(), menu_boutique_2.get_height())
        button_3 = pygame.Rect(WIDTH/2-menu_boutique_3.get_width()/2, HEIGHT/2+menu_boutique_1.get_height()*4, menu_boutique_3.get_width(), menu_boutique_3.get_height())

        screen.blit(Background,(0,0))
        for event in pygame.event.get():
            if button_back.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_menu()
            if button_1.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if credit_joueur >= 100:
                        credit_joueur -= 100
                        vitesse+= 10
                        Achat()
                    else: Cancel()
            if button_2.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if credit_joueur >= 50:
                        credit_joueur -= 50
                        Vie += 1
                        Achat()
                    else:
                        Cancel()
            if button_3.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if credit_joueur >= 150:
                        credit_joueur -= 150
                        tir_rapide -= 10
                        Achat()
                    else:
                        Cancel()

        pygame.draw.rect(screen, (81, 101, 240), button_1)
        pygame.draw.rect(screen, (81, 101, 240), button_2)
        pygame.draw.rect(screen, (81, 101, 240), button_3)
        pygame.draw.rect(screen, (81, 101, 240), button_back)
        screen.blit(title_boutique, (WIDTH/2 - title_boutique.get_width()/2, 100))
        screen.blit(credit_boutique, (WIDTH/2 - credit_boutique.get_width()/2, 340))
        screen.blit(menu_boutique_1,(WIDTH/2-menu_boutique_1.get_width()/2,HEIGHT/2))
        screen.blit(menu_boutique_2,(WIDTH/2-menu_boutique_2.get_width()/2,HEIGHT/2 + menu_boutique_1.get_height()*2))
        screen.blit(menu_boutique_3,(WIDTH/2-menu_boutique_3.get_width()/2,HEIGHT/2 + menu_boutique_1.get_height()*4))
        screen.blit(back, (20,20))
        pygame.display.update()

#Achat Effectué
def Achat():
    run = True
    while run:
        screen.blit(Background, (0,0))
        achat_1 = style.render("Achat effectue",1 ,(255,0,0))
        button_1 = pygame.Rect(20, 20, 200, 50)
        back = style_small.render("Retour", 1, (0,0,0))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if button_1.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_menu()
        
        pygame.draw.rect(screen, (81, 101, 240), button_1)
        screen.blit(back, (80, 20))
        screen.blit(achat_1,(WIDTH/2 - achat_1.get_width()/2, 340))
        pygame.display.update()

#Pas assez de crédit
def Cancel():
    global credit_joueur
    run = True
    keys = pygame.key.get_pressed()
    while run:
        screen.blit(Background, (0,0))
        cancel_1 = style.render(f"Pas Assez de credit Credit: {credit_joueur}", 1, (255,0,0))
        button_1 = pygame.Rect(20, 20, 200, 50)
        back = style_small.render("Retour", 1, (0,0,0))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if button_1.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_menu()
        
        pygame.draw.rect(screen, (81, 101, 240), button_1)
        screen.blit(back, (80, 20))
        screen.blit(cancel_1,(WIDTH/2 - cancel_1.get_width()/2, 340))
        pygame.display.update()

def GameOver():
    global Vie
    global kill
    global credit_joueur
    run = True
    while run:
        screen.blit(Background, (0,0))
        game_over = style.render("GAME OVER !", 1, (255,0,0))
        elimination = style.render(f"Ennemie Tué= {kill}", 1, (255,0,0))
        back = style_small.render("Menu Principal", 1, (0,0,0))
        button_1 = pygame.Rect(20, 20, back.get_width(), back.get_height())
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if button_1.collidepoint((mx, my)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Vie = 1
                    main_menu()
        pygame.draw.rect(screen, (81, 101, 240), button_1)
        screen.blit(back, (20, 20))
        screen.blit(game_over, (WIDTH/2 - game_over.get_width()/2, 540))
        screen.blit(elimination, (WIDTH/2-elimination.get_width()/2, 600))
        pygame.display.update()


#Fonction Jeu
def main():
    global level
    level = 0
    global credit_joueur
    global vitesse_ennemie
    global Vie
    global kill
    nb_ennemies = 3
    ennemies = []

    Run = True 

    player = Player(300,650,100)

    def refresh():
        global level
        screen.blit(Background,(0,0))
        title = style.render(f"Level: {level}", 1, (255,0,0)) #Definir le text a ecrire + style + couleur
        cre = style.render(f"Credit: {credit_joueur}", 1, (255,0,0))
        Vie_restant = style.render(f"Vie = {Vie}", 1, (255,0,0))
        e_eliminé = style.render(f"Ennemie Tué= {kill}", 1, (255,0,0))
        screen.blit(cre, (10,60))
        screen.blit(Vie_restant, (1700, 0))
        screen.blit(title, (10,0)) 
        screen.blit(e_eliminé, (1500, 50))

        for enemy in ennemies:
            enemy.spawn(screen)

        player.spawn(screen)
        pygame.display.update()


    while Run:
        timer.tick(FPS)
        if Vie <= 0 or player.health <=0:
            credit_joueur = 0
            GameOver()
        if level == 1:
            if len(ennemies) == 0:
                for i in range(nb_ennemies):
                    enemy = Ennemie(random.randrange(50, WIDTH-50), random.randrange(-1000, -100), random.choice(["green", "violet"]))
                    ennemies.append(enemy)
                nb_ennemies = 1
                vitesse_ennemie += 0.5
                level += 1
        else:
            if len(ennemies) == 0:
                for i in range(nb_ennemies):
                    enemy = Ennemie(random.randrange(50, WIDTH-50), random.randrange(-1000, -100), random.choice(["boss"]))
                    ennemies.append(enemy)
                nb_ennemies += 2
                vitesse_ennemie += 0.5
                level += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
        keys = pygame.key.get_pressed()#Bind touches si pressées
        if keys[pygame.K_UP] and player.y - vitesse > -30: #Haut
            player.y -= vitesse
        if keys[pygame.K_DOWN] and player.y + vitesse + 60 < HEIGHT: #Bas
            player.y += vitesse
        if keys[pygame.K_RIGHT] and player.x + vitesse + 30 < WIDTH: #Droite
            player.x += vitesse
        if keys[pygame.K_LEFT] and player.x - vitesse > -40: #Gauche
            player.x -= vitesse
        if keys[pygame.K_SPACE]:
            player.tirer()
        if  keys[pygame.K_ESCAPE]: #Quitter
            main_menu()

        for enemy in ennemies:
            enemy.move(vitesse_ennemie)
            enemy.move_lasers(vitesse_ennemie*-2, player)

            if random.randrange(0, 200) == 1:
                enemy.tirer()
            if IntersectWith(enemy, player):
                Vie -= 1
                ennemies.remove(enemy)
            if enemy.y + enemy.get_height() > HEIGHT:
                Vie -= 1
                ennemies.remove(enemy)
        player.move_lasers(vitesse_laser, ennemies)
        refresh()
main_menu()