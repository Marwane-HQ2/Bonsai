import pygame, sys
from pygame.locals import *
from random import randint

# ----------------------------- PARAMETRAGES DU JEU -----------------------------

pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
# COULEURS PREDEFINIES
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BNW = False # VERSION NOIR ET BLANC

# TEXTE 
police_titre = pygame.font.Font("Tangerine-Regular.ttf", 70) # CREER UNE POLICE
police_principale = pygame.font.Font("Tangerine-Regular.ttf", 32) # CREER UNE POLICE

# INFOS ECRAN
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # SURFACE DE JEU
DISPLAYSURFACE.fill(WHITE)
pygame.display.set_caption("Bonsaï")


# ----------------------------- CLASSES -----------------------------
class Bonsai(pygame.sprite.Sprite) :
    """
    Permet de créer des joueurs.
    """
    def __init__(self, img):
        super().__init__()
        # CHARGEMENT DE L'IMAGE
        self.image = pygame.image.load(img)
        # REDIMENSION DE L'IMAGE
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*5, self.image.get_height()*5))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2) # SPAWN POINT - ICI AU MILIEU DE L'ECRAN


        self.groupe_feuilles = pygame.sprite.Group() # LE GROUPE QUI CONTIENDRA LES FEUILLES ET QU'ON UTILISERA POUR LES COLISIONS
        self.nb_feuilles = 0
        self.nb_feuilles_max = 300 # 300 SEMBLE CORRECT

    def afficher(self, surface):
        """
        Affiche l'élément sur la surface donnée en paramètre
        pre: surface (SURFACE)
        post:
        """
        surface.blit(self.image, self.rect) 

    def ajouter_feuille(self, feuille):
        """
        Ajoute la feuille à l'arbre
        """
        self.nb_feuilles += 1
        self.groupe_feuilles.add(feuille)

    def peut_pousser(self):
        pass

class Feuille(pygame.sprite.Sprite):
    def __init__(self, zone_appartion, img):
        super().__init__()
        self.image = pygame.image.load(img) # PENSER A COLORIER LES FEUILLES EN VERT
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//3, self.image.get_height()//3))
        self.image = pygame.transform.rotate(self.image, randint(0, 360))

        x_aleatoire = randint(zone_appartion["x"][0], zone_appartion["x"][1])
        y_aleatoire = randint(zone_appartion["y"][0], zone_appartion["y"][1])

        self.rect = self.image.get_rect()
        self.rect.center = (x_aleatoire, y_aleatoire)

        self.chute = False
    
    def afficher(self, surface):
        """
        Affiche l'élément sur la surface donnée en paramètre
        pre: surface (SURFACE)
        post:
        """
        surface.blit(self.image, self.rect) 
    
    def deplacer(self, bonsai):
        if self.chute:
            if self.rect.bottom < SCREEN_HEIGHT: # SI LE LUTIN EST DANS L'ECRAN 
                self.rect.move_ip(0, 5) # LE LUTIN TOMBE
            else: 
                self.kill() # SI LE LUTIN SORT DE L'ECRAN LE LUTIN EST DETRUIT
                bonsai.nb_feuilles = len(bonsai.groupe_feuilles) # MAINTENANT QUE LA FEUILLE EST DETRUITE ON PEUT METTRE A JOUR LE NOMBRE DE FEUILLES
        

    def tomber(self):
        self.chute = True
        

class Cisailles(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()

        # CHARGEMENT DE L'IMAGE
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2) # SPAWN POINT - ICI AU MILIEU DE L'ECRAN
    
    def afficher(self, surface):
        """
        Affiche l'élément sur la surface donnée en paramètre
        pre: surface (SURFACE)
        post:
        """
        surface.blit(self.image, self.rect) 
    
    def deplacer(self):
        """
        Permet le deplacement des cisailles
        """
        self.rect.center = pygame.mouse.get_pos()
    
    def couper(self, bonsai):
        collisions_avec = pygame.sprite.spritecollideany(self, bonsai.groupe_feuilles)
        if collisions_avec != None:
            collisions_avec.tomber()
        

# ----------------------------- VARIABLES -----------------------------

# ------- LUTINS ET ASSETS -------
BONSAI = Bonsai("bonsai_1.png")

CISAILLES = Cisailles("cisaille_1.png")

# HISTOIRE D'AVOIR PLUS DE CHANCES D'AVOIR DES FEUILLES QUE DES FLEURS
images_elements = ["feuille_1.png", "feuille_2.png", "feuille_1.png", "feuille_2.png", "fleur_1.png", "fleur_2.png", "fleur_3.png"]

# VERSION NOIR ET BLANC
if BNW:
    images_elements = ["noir_et_blanc/feuille_bnw.png", "noir_et_blanc/feuille_bnw.png", "noir_et_blanc/feuille_bnw.png", "noir_et_blanc/fleur_bnw.png"] # NOIR ET BLANC
    CISAILLES = Cisailles("noir_et_blanc/cisaille_bnw.png")
    BONSAI = Bonsai("noir_et_blanc/bonsai_bnw.png")

all_sprites = pygame.sprite.Group() # GROUPE UTILISE POUR AFFICHER CHAQUE ELEMENT
all_sprites.add(BONSAI)
all_sprites.add(CISAILLES)

# ------- ZONES D'APPARITION DES FEUILLES -------
zones_apparition = {
    "Zone_1": {"x": (205, 360), "y": (290, 410)}, # CHAQUE TUPLE DONNE LES COORDONNEES DE DEUX POINT DU RECTANGLE CONSTITUANT LA ZONE
    "Zone_2": {"x": (230, 350), "y": (170, 290)}, 
    "Zone_3": {"x": (310, 390), "y": (50, 150)},
    "Zone_4": {"x": (420, 520), "y": (40, 140)},
    "Zone_5": {"x": (420, 520), "y": (40, 140)},
    "Zone_6": {"x": (530, 630), "y": (50, 140)},
    "Zone_7": {"x": (530, 690), "y": (140, 200)},
    "Zone_8": {"x": (620, 800), "y": (240, 330)}
}

liste_zones = ["Zone_1", "Zone_2", "Zone_3", "Zone_4", "Zone_5", "Zone_6", "Zone_7", "Zone_8"]


# ------- TEMPS -------
horloge_globale = pygame.time.get_ticks()
horloge_feuille = pygame.time.get_ticks()
delais_apparition_feuille = 400

# ----------------------------- FONCTIONS -----------------------------

# ------- TEXTE -------

def afficher_titre(surface):
    titre = police_titre.render("Bonsaï", True, BLACK) # CREER UNE SURFACE CONTENANT DU TEXTE
    surface.blit(titre, (5, 10)) # AFFICHER LE TEXTE SUR LA SURFACE DE JEU AUX COORDONNEES DONNEES

def afficher_indications(surface):
    ligne_1 = police_principale.render("Utilisez la souris pour manipuler les cisailles", True, BLACK)
    ligne_2 = police_principale.render("Cliquez pour couper les feuilles", True, BLACK)
    surface.blit(ligne_1, (8, SCREEN_HEIGHT - 85))
    surface.blit(ligne_2, (8, SCREEN_HEIGHT - 130))


# ----------------------------- BOUCLE DU JEU -----------------------------
while True:
    # OBTENIR L'HEURE QU'IL EST A CHAQUE ITERATION
    heure = pygame.time.get_ticks()

    # ----------------- QUITTER JEU -----------------
    
    # SI APPUI SUR LA CROIX
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # QUITTE LE JEU SI APPUI SUR ESC
    if pygame.key.get_pressed()[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # ----------------- JEU -----------------
    
    # FEUILLES

    # CREATION DE NOUVELLE FEUILLE A INTERVALLE REGULIER ET SI L'ARBRE PEUT ENCORE AVOIR DES FEUILLES
    if heure - horloge_feuille > delais_apparition_feuille and BONSAI.nb_feuilles < BONSAI.nb_feuilles_max:
        zone_aleatoire = liste_zones[randint(0, len(liste_zones)-1)]
        image = images_elements[randint(0, len(images_elements) -1)]
        feuille = Feuille(zones_apparition[zone_aleatoire], image)

        # GESTION DE L'ENREGISTREMENT DE LA FEUILLE DANS LES GROUPES POUR AFFICHER ET GERER LES COLLISIONS
        BONSAI.ajouter_feuille(feuille)
        all_sprites.add(feuille)
        horloge_feuille = heure

    for feuille in BONSAI.groupe_feuilles:
        feuille.deplacer(BONSAI)

    # DEPLACEMENT CISAILLES
    CISAILLES.deplacer()

    # UTILISATION CISAILLES
    if event.type == pygame.MOUSEBUTTONDOWN:
        CISAILLES.couper(BONSAI)

    # MISE A JOUR DU DELAIS D'APPARITION
    # AUGMENTER/DIMINUER MANUELLEMENT LE DELAIS D'APPARITION
    if pygame.key.get_pressed()[K_UP]:
        if delais_apparition_feuille < 10000:
            delais_apparition_feuille += 50
    if pygame.key.get_pressed()[K_DOWN]:
        if delais_apparition_feuille > 50:
            delais_apparition_feuille -= 50
    # ----------------- AFFICHAGE -----------------

    # REPEINDRE L'ECRAN EN BLANC
    DISPLAYSURFACE.fill(WHITE)

    # AFFICHER CHAQUE ELEMENT
    for lutin in all_sprites:
        lutin.afficher(DISPLAYSURFACE)
    CISAILLES.afficher(DISPLAYSURFACE) # POUR QUE LES CISAILLES SOIENT AU PREMIER PLAN
    
    # AFFICHER LES TEXTES
    afficher_titre(DISPLAYSURFACE)
    afficher_indications(DISPLAYSURFACE)

    # REAFFICHER L'ECRAN
    pygame.display.update()
    FramePerSec.tick(FPS)