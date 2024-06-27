import pygame
import sys
import os

def getPath(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)

def getImg(path):
    return pygame.image.load(getPath(path))

SPRITES = {
'STAND': [], 'UP': [], 'DOWN': [], 'LEFT': [], 'RIGHT': [], 'COIN': [], 'SPEED': [], 'EXPLODE': [], 'ASHES': [],
'ROBOT_0': [], 'ROBOT_1': [], 'ROBOT_2': [],'ROBOT_3': [],'ROBOT_4': [],'ROBOT_5': []}

for i in range(4): SPRITES['STAND'].append(getImg('Sprites/char_stand_' + str(i) + '.png'))
for i in range(8): SPRITES['UP'].append(getImg('Sprites/char_up_' + str(i) + '.png'))
for i in range(8): SPRITES['DOWN'].append(getImg('Sprites/char_down_' + str(i) + '.png'))
for i in range(8): SPRITES['LEFT'].append(getImg('Sprites/char_hor_' + str(i) + '.png'))
for i in range(8): SPRITES['RIGHT'].append(pygame.transform.flip(getImg('Sprites/char_hor_' + str(i) + '.png'),True,False))
for i in range(8): SPRITES['COIN'].append(getImg('Sprites/coin_' + str(i) + '.png'))
for i in range(8): SPRITES['EXPLODE'].append(getImg('Sprites/explode_' + str(i) + '.png'))
for i in range(9): SPRITES['ASHES'].append(getImg('Sprites/ashes_' + str(i) + '.png'))
for i in range(2): SPRITES['ROBOT_0'].append(getImg('Sprites/robot_0_' + str(i) + '.png'))
for i in range(4): SPRITES['ROBOT_1'].append(getImg('Sprites/robot_1_' + str(i) + '.png'))
for i in range(2): SPRITES['ROBOT_3'].append(getImg('Sprites/robot_3_' + str(i) + '.png'))
SPRITES['ROBOT_2'].append(getImg('Sprites/robot_2_0.png'))
SPRITES['ROBOT_4'].append(getImg('Sprites/robot_4_0.png'))
SPRITES['ROBOT_5'].append(getImg('Sprites/robot_5_0.png'))
SPRITES['SPEED'].append(getImg('Sprites/speed_0.png'))

pygame.mixer.init()
SOUND = {}
for j in os.listdir(getPath('SFX')):
    SOUND[j[:-4].upper()] = pygame.mixer.Sound(getPath('SFX/' + j))

PX:int = 50
PY:int = 120
MAP:int = 0
SFX:float = 1.0
MSC:float = 1.0

MONEY:int = 30
STMONEY:int = [0,30,50,70,100,120,150,200]
ENEMIES:int = [0,10]
VICTIMS:int = [1,0]
WAVES:int = [1,5]

TRAPS = []

def resetTraps():
    global TRAPS
    TRAPS = [
    {'PRICE': [10,20,30,40,50,60], 'HP': 3, 'POWER': 1},
    {'PRICE': [20,30,60,100,150,200], 'HP': 8, 'POWER': 1},
    {'PRICE': [50,40,80,120,150,180], 'HP': 5, 'POWER': 1},
    {'PRICE': [70,40,80,120,200,300], 'HP': 10, 'POWER': 2},
    {'PRICE': [150,60,100,150,300,500], 'HP': 12, 'POWER': 2},
    ]

ROBOTS = [
{'HP': 4, 'DAMAGE': 2, 'SPD': 1, 'SPRITE': 'ROBOT_2'},
{'HP': 3, 'DAMAGE': 1, 'SPD': 2, 'SPRITE': 'ROBOT_0'},
{'HP': 4, 'DAMAGE': 2, 'SPD': 2, 'SPRITE': 'ROBOT_1'},
{'HP': 8, 'DAMAGE': 2, 'SPD': 1, 'SPRITE': 'ROBOT_4'},
{'HP': 10, 'DAMAGE': 3, 'SPD': 1, 'SPRITE': 'ROBOT_3'},
{'HP': 20, 'DAMAGE': 2, 'SPD': 1, 'SPRITE': 'ROBOT_5'},
]