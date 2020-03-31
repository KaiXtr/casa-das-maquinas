import pygame
import os

SPRITES = {
'STAND': [], 'UP': [], 'DOWN': [], 'LEFT': [], 'RIGHT': [], 'COIN': [], 'SPEED': [], 'EXPLODE': [], 'ASHES': [],
'ROBOT_0': [], 'ROBOT_1': [], 'ROBOT_2': [],'ROBOT_3': [],'ROBOT_4': [],'ROBOT_5': []}

for i in range(4): SPRITES['STAND'].append(pygame.image.load('Sprites/char_stand_' + str(i) + '.png'))
for i in range(8): SPRITES['UP'].append(pygame.image.load('Sprites/char_up_' + str(i) + '.png'))
for i in range(8): SPRITES['DOWN'].append(pygame.image.load('Sprites/char_down_' + str(i) + '.png'))
for i in range(8): SPRITES['LEFT'].append(pygame.image.load('Sprites/char_hor_' + str(i) + '.png'))
for i in range(8): SPRITES['RIGHT'].append(pygame.transform.flip(pygame.image.load('Sprites/char_hor_' + str(i) + '.png'),True,False))
for i in range(8): SPRITES['COIN'].append(pygame.image.load('Sprites/coin_' + str(i) + '.png'))
for i in range(8): SPRITES['EXPLODE'].append(pygame.image.load('Sprites/explode_' + str(i) + '.png'))
for i in range(9): SPRITES['ASHES'].append(pygame.image.load('Sprites/ashes_' + str(i) + '.png'))
for i in range(2): SPRITES['ROBOT_0'].append(pygame.image.load('Sprites/robot_0_' + str(i) + '.png'))
for i in range(4): SPRITES['ROBOT_1'].append(pygame.image.load('Sprites/robot_1_' + str(i) + '.png'))
for i in range(2): SPRITES['ROBOT_3'].append(pygame.image.load('Sprites/robot_3_' + str(i) + '.png'))
SPRITES['ROBOT_2'].append(pygame.image.load('Sprites/robot_2_0.png'))
SPRITES['ROBOT_4'].append(pygame.image.load('Sprites/robot_4_0.png'))
SPRITES['ROBOT_5'].append(pygame.image.load('Sprites/robot_5_0.png'))
SPRITES['SPEED'].append(pygame.image.load('Sprites/speed_0.png'))

pygame.mixer.init()
SOUND = {}
for j in os.listdir('SFX'): SOUND[j[:-4].upper()] = pygame.mixer.Sound('SFX/' + j)

PX = 50
PY = 120
MAP = 0
SFX = 1.0
MSC = 1.0

MONEY = 30
STMONEY = [0,30,50,70,100,120,150,200]
ENEMIES = [0,10]
VICTIMS = [1,0]
WAVES = [1,5]

TRAPS = [
{'PRICE': [10,20,30,40,50,60], 'HP': 3},
{'PRICE': [20,30,60,90,120,150], 'HP': 8},
{'PRICE': [50,40,80,120,150,180], 'HP': 5},
{'PRICE': [70,30,60,90,120,150], 'HP': 10},
{'PRICE': [150,50,100,150,200,250], 'HP': 12},
]

ROBOTS = [
{'HP': 5, 'DAMAGE': 2, 'SPD': 2, 'SPRITE': 'ROBOT_2'},
{'HP': 3, 'DAMAGE': 1, 'SPD': 4, 'SPRITE': 'ROBOT_0'},
{'HP': 8, 'DAMAGE': 2, 'SPD': 2, 'SPRITE': 'ROBOT_1'},
{'HP': 8, 'DAMAGE': 2, 'SPD': 2, 'SPRITE': 'ROBOT_4'},
{'HP': 10, 'DAMAGE': 3, 'SPD': 1, 'SPRITE': 'ROBOT_3'},
{'HP': 20, 'DAMAGE': 2, 'SPD': 1, 'SPRITE': 'ROBOT_5'},
]