import pygame
import pytmx
import random
import math
import database
import sys

class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Casa das Máquinas')
		pygame.display.set_icon(pygame.image.load('icon.ico'))
		pygame.mouse.set_visible(False)

		self.screen = pygame.display.set_mode((1200, 800))
		self.display = pygame.Surface((600, 400))
		self.monotype = pygame.font.Font('Fonts/monotype.ttf', 15)
		
		#MIXER
		self.ch_sfx = pygame.mixer.Channel(0)
		self.ch_sfx.set_volume(database.SFX)
		self.ch_ton = pygame.mixer.Channel(1)
		self.ch_ton.set_volume(database.SFX)
		self.ch_msc = pygame.mixer.Channel(2)
		self.ch_msc.set_volume(database.MSC)
		self.ch_stp = pygame.mixer.Channel(3)
		self.ch_stp.set_volume(database.SFX)
		self.rectdebug = False
		
		self.player = {'RECT': pygame.Rect(database.PX,database.PY,20,10), 'SPRITE': 'STAND', 'GIF': 0.0, 'HP': 10, 'HPLOSS': 10, 'LIFES': 3, 'DIRECTION': 0, 'SPD': 2, 'DMGTIM': 0}
		self.pause = 3
		self.text = ''
		self.txty = 0
		self.nxtlvl = 0
		self.glock = pygame.time.Clock()
		self.FPS = 60
		self.displayzw = 600
		self.displayzh = 400
		self.winbar = 210
		self.cam = pygame.Rect(0,0,600,400)
		self.speakin = 0
		self.opt = 0
		self.lopt = 0
		self.mnu = 0
		self.trapset = ''
		self.trapgif = 0.0
		self.logalpha = 0
		self.dlg = []
		self.dlgping = False
		self.ptmove = 0
		self.elevator = 430
		self.tindex = 1
		self.cursor = 0
		self.ctb = 'background1'

		self.tut = False
		self.tutfa = 0
		self.txtsrf = pygame.Surface((640,50))
		for i in range(16): self.txtsrf.blit(pygame.image.load('Sprites/pattern.png'),(i * 40, 0))
		self.tutsrf = pygame.Surface((320,160))
		for i in range(10): self.tutsrf.blit(pygame.image.load('Sprites/gradient.png'),(i * 32, 0))
		
		self.en = []
		self.encount = 0
		self.victims = []
		self.doors = []
		self.nodes = []
		self.reverse = []
		self.items = []
		self.itemcount = 0
		self.traps = []
		self.room = ''
		self.tilmap = []
		self.tilrect = []
		self.bullets = []
		self.explosions = []
		self.ashes = []
		self.trail = []
		self.area = []
		self.tilemation = 0.0
		self.etext = ''

		self.rendermap('level_0')
		for i in range(10): self.run()
		self.mnu = 1
		for i in range(180):
			self.run()
			if self.mnu == 2: break
		self.mnu = 2
		self.ch_msc.play(database.SOUND['CRICKETS'],-1)
		for i in range(30): self.run()
		self.transiction(False,55)
	
	def victim(self,i):
		if self.pause < 3: i['IMAGE'] += 0.5
		if i['IMAGE'] == 2.0: i['IMAGE'] = 0.0

		if i['CAPTURED'] != None:
			found = False
			for e in self.en:
				if e['N'] == i['CAPTURED']:
					i['RECT'].x = e['RECT'].x
					i['RECT'].y = e['RECT'].y
					found = True
			if found == False: i['CAPTURED'] = None
		if self.rectdebug == True: pygame.draw.rect(self.display, (255,0,0), i['RECT'])
		self.display.blit(pygame.image.load('Sprites/shade.png'),(i['RECT'].x - self.cam.x - 1,i['RECT'].y - self.cam.y + int(i['RECT'].height/2) - 2))
		if i['CAPTURED'] != None: ex = 6
		else: ex = 0
		self.display.blit(pygame.image.load('Sprites/victim_' + str(i['TYPE']) + '_' + str(math.floor(i['IMAGE'])) + '.png'),(i['RECT'].x - self.cam.x + 4,i['RECT'].y - self.cam.y - 19 - ex))

		for e in self.en:
			if self.colide(i['RECT'],e['RECT']) and i['CAPTURED'] == None:
				e['REVERSE'] = True
				i['CAPTURED'] = e['N']

		for s in self.area:
			if self.colide(i['RECT'],s) and self.pause == 0:
				if i['GET'] == False:
					self.ch_ton.play(database.SOUND['VICTIM'])
					database.VICTIMS[0] -= 1
					self.ashes.append({'RECT': pygame.Rect(i['RECT'].x,i['RECT'].y - 20,10,10), 'GIF': 0})
					i['GET'] = True

	def enemy(self,i):
		if self.rectdebug == True: pygame.draw.rect(self.display, (255,0,0), i['RECT'])

		#SHOT
		if i['TYPE'] == 4 and i['DMGTIM'] == 0:
			if len(self.traps) > 0:
				i['LASER'] = (self.traps[0]['RECT'].x + 10,self.traps[0]['RECT'].y + 10)
			else:
				i['LASER'] = (self.player['RECT'].x + 10,self.player['RECT'].y)
			i['DMGTIM'] = 100

		#DRAW
		if i['TYPE'] == 4:
			if i['DMGTIM'] >= 80: i['GIF'] = 1
			else: i['GIF'] = 0
		elif self.pause < 3: i['GIF'] += 1
		if i['GIF'] >= len(database.SPRITES[i['SPRITE']]): i['GIF'] = 0

		if i['SPRITE'] == 'ROBOT_1': ex = 20
		else: ex = 0
		self.display.blit(pygame.image.load('Sprites/shade.png'),(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y - ex + int(i['RECT'].height/2)))
		img = database.SPRITES[i['SPRITE']][i['GIF']]
		self.display.blit(img,(i['RECT'].x - (round(img.get_rect().width/2) - 10) - self.cam.x,i['RECT'].y - (img.get_rect().height - 12) - self.cam.y - ex))
		if i['DMGTIM'] > 50 and i['DMGTIM'] < 80 and i['TYPE'] == 4:
			pygame.draw.line(self.display, (255,10,10), (i['RECT'].x - (round(img.get_rect().width/2) - 10) - self.cam.x + 10,i['RECT'].y - (img.get_rect().height - 12) - self.cam.y + 10 - ex),i['LASER'],2)

		#MOVE
		if i['REVERSE'] == False:
			for n in self.nodes:
				if self.colide(i['RECT'],n['RECT']):
					if n['CONDITION'] == None: i['DIRECTION'] = n['DIRECTION']
					elif n['CONDITION'] == database.VICTIMS[0]: i['DIRECTION'] = n['DIRECTION']
		else:
			for n in self.reverse:
				if self.colide(i['RECT'],n['RECT']):
					if n['CONDITION'] == None: i['DIRECTION'] = n['DIRECTION']
					elif n['CONDITION'] == database.VICTIMS[0]: i['DIRECTION'] = n['DIRECTION']

		if self.colide(i,self.traps) == False and self.pause < 3:
			if i['DIRECTION'] == 1: i['RECT'].x += i['SPD']
			if i['DIRECTION'] == 2: i['RECT'].y += i['SPD']
			if i['DIRECTION'] == 3: i['RECT'].x -= i['SPD']
			if i['DIRECTION'] == 4: i['RECT'].y -= i['SPD']

		if i['DMGSHW'] > 0: i['DMGSHW'] -= 1
		if i['DMGTIM'] > 0: i['DMGTIM'] -= 1

		#PLAYER DAMAGE
		if self.colide(i['RECT'],self.player['RECT']):
			if self.player['DMGTIM'] == 0:
				self.ch_ton.play(database.SOUND['DAMAGE_PLAYER'])
				self.player['HP'] -= i['DAMAGE']
				self.player['DMGTIM'] = 50
		if i['LASER'] != None and i['DMGTIM'] > 50 and i['DMGTIM'] < 80:
			if self.colide(pygame.Rect(i['LASER'][0],i['LASER'][1],5,5),self.player['RECT']):
				if self.player['DMGTIM'] == 0:
					self.ch_ton.play(database.SOUND['DAMAGE_PLAYER'])
					self.player['HP'] -= i['DAMAGE']
					self.player['DMGTIM'] = 50

		#TRAP DAMAGE
		for j in self.traps:
			if self.colide(i['RECT'],j['RECT']):
				if i['DMGTIM'] == 0:
					if j['TYPE'] == 3:
						j['GIF'] = 1
						i['HP'] = 0
					j['HP'] -= i['DAMAGE']
					i['DMGTIM'] = 100
					if j['HP'] > 0:
						self.ch_sfx.play(database.SOUND['DAMAGE_TRAP'])
						j['DMGSHW'] = 100
						j['SHK'] = 5
					else:
						self.ch_sfx.play(database.SOUND['DESTROY_TRAP'])
						self.explosions.append({'RECT': pygame.Rect(j['RECT'].x,j['RECT'].y,10,10), 'GIF': 0})
		if i['LASER'] != None and i['DMGTIM'] > 50 and i['DMGTIM'] < 80:
			for j in self.traps:
				if self.colide(pygame.Rect(i['LASER'][0],i['LASER'][1],5,5),j['RECT']):
					if j['TYPE'] != 3:
						if j['SHK'] == 0:
							j['HP'] -= i['DAMAGE']
							if j['HP'] > 0:
								self.ch_sfx.play(database.SOUND['DAMAGE_TRAP'])
								j['DMGSHW'] = 100
								j['SHK'] = 5
							else:
								self.ch_sfx.play(database.SOUND['DESTROY_TRAP'])
								self.explosions.append({'RECT': pygame.Rect(j['RECT'].x,j['RECT'].y,10,10), 'GIF': 0})
					else: j['GIF'] = 1

		#ENEMY DAMAGE
		for b in self.bullets:
			if self.colide(b['FOLLOW'],b['RECT']) and self.colide(i['RECT'],b['RECT']):
				if b['TARGET'] == i['MOVE'] or b['TARGET'] == 2:
					if b['EXPLODE'] == True:
						explosion = pygame.Rect(b['RECT'].x - 20, b['RECT'].y - 20,40,40)
						for e in self.en:
							if self.colide(e['RECT'],explosion):
								self.ch_sfx.play(database.SOUND['DAMAGE_ENEMY'])
								i['HP'] -= b['DAMAGE']
								i['DMGSHW'] = 100
								b['DESTROY'] = True
					else:
						self.ch_sfx.play(database.SOUND['DAMAGE_ENEMY'])
						i['HP'] -= b['DAMAGE']
						i['DMGSHW'] = 100
						b['DESTROY'] = True

		if i['HP'] <= 0:
			self.items.append({'N': self.itemcount, 'TYPE': 0, 'JUMP': 5, 'GRAVITY': 4.5, 'GIF': 0.0,
				'RECT': pygame.Rect(i['RECT'].x + round(random.randint(-5,5)),i['RECT'].y + round(random.randint(-5,5)),10,10), 'GET': False})
			self.objects.append([4,self.itemcount,i['RECT'].y])
			self.itemcount += 1
			database.ENEMIES[0] += 1
			self.explosions.append({'RECT': pygame.Rect(i['RECT'].x,i['RECT'].y,10,10), 'GIF': 0})
			
	def item(self,i):
		if i['TYPE'] < 5: sprite = 'COIN'
		elif i['TYPE'] < 7:
			if self.player['SPD'] < 7: sprite = 'SPEED'
			else: sprite = 'COIN'
		else: sprite = 'COIN'

		#JUMP & GRAVITY
		i['GIF'] += 0.5
		if i['GIF'] >= len(database.SPRITES[sprite]): i['GIF'] = 0.0
		if i['GRAVITY'] > -5:
			i['JUMP'] += i['GRAVITY']
			i['GRAVITY'] -= 0.5
		
		img = database.SPRITES[sprite][math.floor(i['GIF'])]
		self.display.blit(pygame.image.load('Sprites/shade.png'),(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
		self.display.blit(img,(i['RECT'].x - self.cam.x + int(img.get_rect().width/2),i['RECT'].y - self.cam.y - i['JUMP'] - int(img.get_rect().height/2)))
		
		#GET ITEM
		if i['GRAVITY'] == -5 and i['GET'] == False:
			if sprite == 'COIN':
				self.ch_sfx.play(database.SOUND['COIN'])
				database.MONEY += 10
			if sprite == 'SPEED':
				self.ch_sfx.play(database.SOUND['SPEED'])
				self.player['SPD'] += 1
			i['GET'] = True
	
	def trap(self,i):
		#DRAW
		if self.rectdebug == True: pygame.draw.rect(self.display, (255,0,0), i['RECT'])
		if i['TYPE'] == 2:
			if len(self.en) > 0:
				xx = self.en[0]['RECT'].x - i['RECT'].x
				yy = self.en[0]['RECT'].y - i['RECT'].y
				if +xx < +yy:
					if xx < 0: d = 3
					else: d = 1
				else:
					if yy < 0: d = 4
					else: d = 2
			else: d = 2
		elif i['TYPE'] == 3:
			d = i['GIF'] + 1
		else: d = 1

		if i['SHK'] > 0: i['SHK'] = -i['SHK']
		elif i['SHK'] < 0: i['SHK'] = -i['SHK'] - 1

		img = pygame.image.load('Sprites/trap_' + str(i['TYPE']) + '_' + str(d - 1) + '.png')
		i['RECT'].width = img.get_rect().width
		i['RECT'].height = img.get_rect().height
		if i['TYPE'] != 3: self.display.blit(pygame.image.load('Sprites/shade.png'),(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y + int(img.get_rect().height) - 5))
		self.display.blit(img,(i['RECT'].x - self.cam.x + i['SHK'],i['RECT'].y - self.cam.y))

		#BULLETS
		if i['TYPE'] in [2,4,5] and self.pause < 3 and len(self.en) > 0:
			i['TIME'] -= 1
			if i['TIME'] == 0:
				if i['TYPE'] == 4: t = 1
				else: t = 0
				ru = []
				for b in self.bullets: ru.append(b['FIND'])
				if len(self.en) > 0:
					e = self.en[0]['N']
					for b in self.en:
						if b['N'] not in ru: e = b['N']; break
				else: e = self.en[0]['N']
				if i['TYPE'] == 5: explosion = True; ex = 5
				else: explosion = False; ex = 0
				self.bullets.append({'DIRECTION': d, 'DAMAGE': i['UPGRADE'] + 1 + ex, 'RECT': pygame.Rect(i['RECT'].x + 5,i['RECT'].y,10,10), 'DESTROY': False, 'TRLTIM': 10, 'TARGET': t, 'FOLLOW': self.en[0]['RECT'], 'FIND': e, 'EXPLODE': explosion})
				self.ch_ton.play(database.SOUND['BULLET'])
				i['TIME'] = 40 - (5 * i['UPGRADE'])

		#EXPLODE
		if i['HP'] <= 0:
			self.explosions.append({'RECT': pygame.Rect(i['RECT'].x,i['RECT'].y,10,10), 'GIF': 0})
	
	def door(self,i):
		if database.ENEMIES[0] >= database.ENEMIES[1]:
			i['SPAWN'] = 300
			database.WAVES[0] += 1
			if database.WAVES[0] < database.WAVES[1]:
				self.text = 'ONDA ' + str(database.WAVES[0])
				database.ENEMIES[1] += 5 * database.WAVES[0]
				self.txty = 400
			elif self.pause < 3:
				self.pause = 3
				for e in self.en:
					e['HP'] = 0
					self.explosions.append({'RECT': pygame.Rect(e['RECT'].x,e['RECT'].y,10,10), 'GIF': 0})
				self.ch_msc.fadeout(2500)
				for t in range(70): self.run()
				self.ch_msc.play(database.SOUND['VICTORY'])
				for t in range(50): self.run()
				self.pause = 4

		if i['OPNCLS'] == True: oc = True
		elif i['DRTIM'] > 0: oc = False; i['DRTIM'] -= 1
		else: oc = True
		if self.pause == 3: oc = True
		self.display.blit(pygame.image.load('Sprites/door_' + str(oc).lower() + '.png'),(i['RECT'].x - self.cam.x,i['RECT'].y - self.cam.y))
		if oc == False: self.display.blit(pygame.image.load('Sprites/door_shine.png'),(i['RECT'].x - self.cam.x + 7,i['RECT'].y - self.cam.y + 45))

		if i['OPNCLS'] == False and self.pause < 3 and len(self.en) < 10:
			i['SPAWN'] -= 1
			if i['SPAWN'] == 0:
				#self.ch_ton.play(database.SOUND['SPAWN'])
				lmt = database.MAP
				if database.WAVES[0] >= int(database.WAVES[1]/2): lmt += 1
				tp = round(random.randint(0,lmt))
				rb = database.ROBOTS[tp].copy()
				rb['HP'] *= database.WAVES[0]
				rb['N'] = self.encount
				rb['TYPE'] = tp
				rb['MAXHP'] = rb['HP']
				rb['HPLOSS'] = rb['HP']
				if tp == 2: rb['MOVE'] = 1
				else: rb['MOVE'] = 0
				rb['GIF'] = 0
				rb['RECT'] = pygame.Rect(i['RECT'].x + 5,i['RECT'].y + 50,20,12)
				rb['DIRECTION'] = 2
				if len(self.victims) > 0: rb['FOLLOW'] = self.victims[0]['RECT']
				else: rb['FOLLOW'] = self.player['RECT']
				rb['DMGSHW'] = 0
				rb['DMGTIM'] = 0
				rb['LASER'] = None
				rb['REVERSE'] = False
				self.en.append(rb)
				self.objects.append([1,self.encount,i['RECT'].y])
				self.encount += 1
				i['SPAWN'] = round(100/database.WAVES[0])
				i['DRTIM'] = 20
	
	def colide(self, i1, i2):
		cld = False
		if i2 == self.tilrect:
			for i in i2[0]:
				if i[0] == 'WALL' and self.facing(i1,i[1]) != 1:
					cld = pygame.Rect.colliderect(i1['RECT'],i[1])
					if cld == True:  break
		elif i2 == self.traps:
			for i in i2:
				cld = pygame.Rect.colliderect(i1['RECT'],i['RECT'])
				if cld == True:  break
		else:
			cld = pygame.Rect.colliderect(i1,i2)

		return cld

	def facing(self, i1, i2):
		if isinstance(i2, dict) == False: i2 = {'RECT': i2, 'DIRECTION': i1['DIRECTION']}
		if i1['DIRECTION'] == i2['DIRECTION']:
			if i1['DIRECTION'] == 1:
				if i1['RECT'].x < i2['RECT'].x: return 2
				elif i1['RECT'].x > i2['RECT'].x: return 3
				else: return 1
			elif i1['DIRECTION'] == 2:
				if i1['RECT'].y < i2['RECT'].y: return 2
				elif i1['RECT'].y > i2['RECT'].y: return 3
				else: return 1
			elif i1['DIRECTION'] == 3:
				if i1['RECT'].x > i2['RECT'].x: return 2
				elif i1['RECT'].x < i2['RECT'].x: return 3
				else: return 1
			elif i1['DIRECTION'] == 4:
				if i1['RECT'].y > i2['RECT'].y: return 2
				elif i1['RECT'].y < i2['RECT'].y: return 3
				else: return 1
		else: return 1

	def events(self):
		for event in pygame.event.get():				
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			self.pressed = pygame.key.get_pressed()
			self.mp = pygame.Rect(round(pygame.mouse.get_pos()[0]/2),round(pygame.mouse.get_pos()[1]/2),3,3)
			if self.pressed[pygame.K_DELETE]: self.rectdebug = not self.rectdebug

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1: self.cursor = 0

			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.pause == 0:
					if event.button == 4: self.tindex -= 1
					elif event.button == 5: self.tindex += 1
					if self.tindex < 1: self.tindex = 5
					if self.tindex > 5: self.tindex = 1
					
					if event.button == 1:
						up = False
						self.cursor = 1
						for i in self.traps:
							if self.colide(i['RECT'],self.mp):
								if i['UPGRADE'] < 5:
									up = True
									if database.MONEY >= database.TRAPS[i['TYPE'] - 1]['PRICE'][i['UPGRADE'] + 1]:
										self.ch_sfx.play(database.SOUND['BUY'])
										database.MONEY -= database.TRAPS[i['TYPE'] - 1]['PRICE'][i['UPGRADE'] + 1]
										i['UPGRADE'] += 1
										if i['TYPE'] == 1: i['HP'] += 5
									else: self.ch_sfx.play(database.SOUND['ERROR'])

						if self.trapset == '' and up == False:
							if database.MONEY >= database.TRAPS[self.tindex - 1]['PRICE'][0]:
								self.ch_sfx.play(database.SOUND['OK'])
								self.trapset = self.tindex
							else: self.ch_sfx.play(database.SOUND['ERROR'])
						elif self.trapset == self.tindex and up == False:
							can = False
							for s in self.area:
								if self.colide(self.mp,s): can = True
							if can == True:
								database.MONEY -= database.TRAPS[self.tindex - 1]['PRICE'][0]
								database.TRAPS[self.tindex - 1]['PRICE'][0] += int(database.TRAPS[self.tindex - 1]['PRICE'][0]/2)
								if self.mp.x > 30: xa = round((self.mp.x - 15)/30) * 30
								else: xa = 0
								if self.mp.y > 30: ya = round((self.mp.y - 15)/30) * 30
								else: ya = 0
								ref = database.TRAPS[self.tindex - 1].copy()
								self.ch_sfx.play(database.SOUND['BUY'])
								self.traps.append({'N': len(self.traps), 'RECT': pygame.Rect(xa - self.cam.x + 5,ya - self.cam.y + 5,10,10),'TYPE': self.tindex, 'HP': ref['HP'],
									'MAXHP': ref['HP'], 'HPLOSS': ref['HP'], 'DMGSHW': 0, 'SHK': 0, 'TIME': 80, 'UPGRADE': 0, 'UPGSHW': 0, 'GIF': 0})
								self.objects.append([5,len(self.traps) - 1,ya])
								self.trapset = ''
							else: self.ch_ton.play(database.SOUND['ERROR'])
					elif event.button == 2:
						if self.player['LIFES'] > 0 and self.pause == 0:
							self.player['LIFES'] -= 1
							self.ch_msc.play(database.SOUND['LOST'])
							self.pause = 3
							self.transiction(True,210)
							self.player['RECT'].x = database.PX
							self.player['RECT'].y = database.PY
							self.player['HP'] = 10
							self.player['HPLOSS'] = 10
							database.MONEY = database.STMONEY[database.WAVES[0]]
							self.pause = 2
							self.rendermap('level_' + str(database.MAP))
							self.transiction(False,0)
							self.ch_msc.play(database.SOUND['MAIN'])
							self.pause = 0

					elif event.button == 3:
						self.ch_sfx.play(database.SOUND['CANCEL'])
						self.trapset = ''

				elif self.mnu == 1:
					if event.button == 1:
						self.cursor = 1
						self.mnu = 2
				elif self.mnu == 2 and self.dlg == []:
					if event.button == 1:
						self.cursor = 1
						if self.winbar == 55:
							op1 = pygame.Rect(170,355,60,35)
							op2 = pygame.Rect(310,355,70,35)
							if self.colide(self.mp,op1):
								if self.tut == False:
									self.ch_sfx.play(database.SOUND['OK'])
									self.tut = True
									self.opt = 0
								else:
									self.ch_sfx.play(database.SOUND['OK'])
									self.tut = False
									self.ch_msc.fadeout(1500)
									self.opt = 10
									self.transiction(True,210)
									self.ctb = None
									self.opt = 0
									self.transiction(False,55)
									self.etext = 'clique com o botão direito para pular'
									for t in range(100): self.run()
									self.etext = ''
									self.dialog(['Sério que eu vou usar desenhos cagados do paint',1,'só pra pra fazer filminhos?',1,'vai ficar ó...',1])
									self.ctb = 'background2'
									self.dialog(['...uma bosta',1])
									self.ch_msc.play(database.SOUND['CINEMATIC'],-1)
									self.ctb = 'background3'
									self.dialog(['Mais um dia de trabalho...',1,'Hã? O que é isso?',1,'O laboratório está sendo invadido!',1])
									self.ctb = 'background4'
									self.dialog(['Era só o que faltava...',1,'Só podia ser um vírus!',1])
									self.ctb = 'background5'
									self.dialog(['Relaxa ae mano',1,'Não é o coronga vírus não...',1])
									self.ctb = 'background4'
									self.dialog(['Isso é causa de um vírus de computador',1,'...ele está hackeando os robôs',1,'Logo logo vão atacar geral daqui',1])
									self.ctb = 'background8'
									self.dialog(['Argh...céu azul...sol amarelo...',1,'vida...natureza...',1,'eu odeio tudo isso!',1,'e odeio mais ainda esses robôs!',1])
									self.dialog(['Eles querem nos tirar do sedentarismo',1,'E nos obrigar a sair do laboratório!',1])
									self.ctb = 'background6'
									self.dialog(['Parece que vou ter que salvar o dia',1,'Afe, mas isso vai ser difícil...',1])
									if self.mnu < 3: self.transiction(True,210,2)
									self.ch_msc.stop()
									self.dialog(['é óbvio que vou colocar máquinas para quebrar  ',0,'os próprios robôs do laboratório ao invés de  ',0,'chamar as autoridades',1])
									self.etext = 'PRIMEIRO ANDAR'
									while self.elevator > 0:
										self.elevator -= 5
										self.run()
									self.etext = ''
									self.ch_msc.play(database.SOUND['MAIN'],-1)
									self.mnu = 3
									self.transiction(False,0)
									self.pause = 0
									self.text = 'ONDA 1'
									self.txty = 400
							elif self.colide(self.mp,op2):
								if self.tut == False:
									self.ch_sfx.play(database.SOUND['OK'])
									self.tut = True
									self.opt = 1
								else:
									self.ch_sfx.play(database.SOUND['CANCEL'])
									self.tut = False
						elif self.ctb == 'background1' and self.opt != 10:
							self.logalpha = 255
							self.winbar = 55
				elif self.mnu == 4:
					if event.button == 1:
						self.cursor = 1
						self.mnu = 5
						self.ch_msc.fadeout(5000)
						self.transiction(True,210)
						for i in range(30): self.run()
						while self.logalpha > 0:
							self.logalpha -= 5
							self.run()
						self.__init__()
 
		self.pressed = pygame.key.get_pressed()
		if self.pause == 0:
			'''if self.pressed[pygame.K_w]:
				self.player['DIRECTION'] = 4
			elif self.pressed[pygame.K_s]:
				self.player['DIRECTION'] = 2
			elif self.pressed[pygame.K_a]:
				self.player['DIRECTION'] = 3
			elif self.pressed[pygame.K_d]:
				self.player['DIRECTION'] = 1
			else: self.player['DIRECTION'] = 0

			if self.colide(self.player, self.tilrect) == False:
				if self.player['DIRECTION'] == 4:
					self.player['SPRITE'] = 'UP'; self.player['RECT'].y -= self.player['SPD']
				elif self.player['DIRECTION'] == 2:
					self.player['SPRITE'] = 'DOWN'; self.player['RECT'].y += self.player['SPD']
				elif self.player['DIRECTION'] == 3:
					self.player['SPRITE'] = 'LEFT'; self.player['RECT'].x -= self.player['SPD']
				elif self.player['DIRECTION'] == 1:
					self.player['SPRITE'] = 'RIGHT'; self.player['RECT'].x += self.player['SPD']
			else: self.player['DIRECTION'] = 0
			if self.player['DIRECTION'] == 0:
				self.player['SPRITE'] = 'STAND'''

		if self.cursor == 1 and self.mnu == 2 and self.opt == 1:
			sb1 = pygame.Rect(260,165,110,15)
			sb2 = pygame.Rect(260,195,110,15)
			if self.colide(self.mp,sb1): database.SFX = (self.mp.x - 260)/100
			if self.colide(self.mp,sb2): database.MSC = (self.mp.x - 260)/100

			if database.SFX < 0.0: database.SFX = 0.0
			if database.SFX > 1.0: database.SFX = 1.0
			if database.MSC < 0.0: database.MSC = 0.0
			if database.MSC > 1.0: database.MSC = 1.0
			self.ch_sfx.set_volume(database.SFX)
			self.ch_ton.set_volume(database.SFX)
			self.ch_msc.set_volume(database.MSC)
			self.ch_stp.set_volume(database.SFX)
	
	def dialog(self, tx):
		self.dlg = []
		txt = tx
		tid = 0
		did = 0
		spd = 10

		while tid < len(txt) and self.mnu < 3:
			if isinstance(txt[tid], str):
				self.dlg.append('')
				for i in txt[tid]:
					while True:
						if spd > 0: spd = 0
						else:
							self.ch_sfx.play(database.SOUND['TEXT'])
							self.dlg[0] += i
							spd = 10
							break
						self.run()
			elif txt[tid] == 1:
				self.dlg.append(1)
				self.wait()
				self.ch_ton.play(database.SOUND['OK'])
			elif txt[tid] == 0:
				self.dlg.append(0)
				self.dlg = []
			tid += 1

		self.dlg = []

	def wait(self):
		waiting = True
		blkspd = 6
		while waiting == True:
			blkspd -= 1
			if blkspd == 0: blkspd = 6
			if blkspd > 3: self.dlgping = True
			else: self.dlgping = False
			self.mp = pygame.Rect(round(pygame.mouse.get_pos()[0]/2),round(pygame.mouse.get_pos()[1]/2),3,3)
			self.run()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					waiting = False
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.dlg = []
					self.dlgping = False
					waiting = False
					self.cursor = 1
					if event.button == 3:
						self.winbar = 210
						self.mnu = 3

	def transiction(self, fade, limit, spd=5):
		if fade == False:
			while self.winbar > limit:
				self.winbar -= spd
				self.run()
		else:
			while self.winbar < limit:
				self.winbar += spd
				self.run()
				
	def rendermap(self, mp):
		self.map = pytmx.load_pygame('Maps/' + mp + '.tmx')
		self.room = mp
		self.cam.x = 0
		self.cam.y = 0
		self.tilmap = []
		#self.objects = [[0,0,self.player['RECT'].y]]
		self.objects = []
		self.tilrect = []
		self.en = []
		self.encount = 0
		self.victims = []
		self.traps = []
		self.items = []
		self.itemcount = 0
		self.doors = []
		self.reverse = []
		self.nodes = []
		self.bullets = []
		self.explosions = []
		self.area = []
		database.ENEMIES = [0,10]
		database.WAVES = [1,6 * (database.MAP + 1)]
		database.MONEY = database.VICTIMS[0] * 20
		database.TRAPS = [
		{'PRICE': [10,20,30,40,50,60], 'HP': 3},
		{'PRICE': [20,40,60,80,100,120], 'HP': 8},
		{'PRICE': [50,30,60,90,120,150], 'HP': 5},
		{'PRICE': [70,20,30,40,50,60], 'HP': 10},
		{'PRICE': [150,50,100,150,200,250], 'HP': 12},
		]

		#DRAW MAP
		for i in range(3):
			self.tilmap.append([])
			self.tilrect.append([])
			for a in range(2):
				self.tilmap[i].append(pygame.Surface((self.map.width * self.map.tilewidth,self.map.height * self.map.tileheight), pygame.SRCALPHA, 32))
				for x in range(0, self.map.width):
					for y in range(0, self.map.height):
						try: gid = self.map.get_tile_gid(x, y, i)
						except: gid = None
						if gid != None:
							tl = self.map.get_tile_properties_by_gid(gid)
							if tl != None:
								if tl['frames'] != []: image = self.map.get_tile_image_by_gid(tl['frames'][a].gid)
								else: image = self.map.get_tile_image_by_gid(gid)
								image.convert()
								self.tilmap[i][a].blit(image, (x * self.map.tilewidth - self.cam.x, y * self.map.tileheight - self.cam.y))
								self.tilrect[i].append([self.map.get_tile_properties(x, y, i)['TYPE'].upper(),pygame.Rect(x * self.map.tilewidth, y * self.map.tileheight,self.map.tilewidth,self.map.tileheight)])
						elif i == 0: self.tilrect[i].append(['WALL',pygame.Rect(x * 30, y * 30,30,30)])
		#VICTIMS
		ind = 0
		for i in range(len(self.map.layers[5])):
			obj = self.map.get_object_by_name('victim_' + str(i))
			self.victims.append({'N': ind, 'RECT': pygame.Rect(int(obj.x), int(obj.y), 20, 15), 'TYPE': int(obj.type),
			'IMAGE': 0.0,'MOVE': 'horizontal','DIRECTION': 0,'SPD': 1, 'TIME': 20,'FOLLOW': None,'FOLLEND': 0,'GET': False,'CAPTURED': None})
			self.objects.append([2,ind,int(obj.y)])
			ind += 1
		database.VICTIMS = [len(self.victims),len(self.victims)]

		#DOORS
		ind = 0
		for i in range(len(self.map.layers[7])):
			obj = self.map.get_object_by_name('door_' + str(i))
			self.doors.append({'N': ind, 'OPNCLS': False, 'SPAWN': 150, 'DRTIM': 0,'RECT': pygame.Rect(int(obj.x),int(obj.y),30,60)})
			self.objects.append([3,ind,int(obj.y)])
			ind += 1

		#NODES
		ind = 0
		for i in range(len(self.map.layers[3])):
			obj = self.map.get_object_by_name('node_' + str(i))
			if len(obj.properties) > 0: prp = obj.properties['TRIGGER']
			else: prp = None
			self.nodes.append({'N': ind, 'DIRECTION': int(obj.type), 'RECT': pygame.Rect(int(obj.x),int(obj.y),int(obj.width),int(obj.height)), 'CONDITION': prp})
			ind += 1

		#REVERSE
		ind = 0
		for i in range(len(self.map.layers[4])):
			obj = self.map.get_object_by_name('reverse_' + str(i))
			if len(obj.properties) > 0: prp = obj.properties['TRIGGER']
			else: prp = None
			self.reverse.append({'N': ind, 'DIRECTION': int(obj.type), 'RECT': pygame.Rect(int(obj.x),int(obj.y),int(obj.width),int(obj.height)), 'CONDITION': prp})
			ind += 1

		#AREA
		ind = 0
		for i in range(len(self.map.layers[6])):
			obj = self.map.get_object_by_name('area_' + str(i))
			self.area.append(pygame.Rect(int(obj.x),int(obj.y),int(obj.width),int(obj.height)))
			ind += 1
				
	def draw(self):
		self.display.fill((0,0,0))

		#ANIMATION
		if self.pause < 2: self.player['GIF'] += 0.5
		if self.player['GIF'] >= len(database.SPRITES[self.player['SPRITE']]): self.player['GIF'] = 0.0
		if self.pause < 2: self.tilemation += 0.1
		if self.tilemation >= 2.0: self.tilemation = 0.0

		#RESET
		if database.VICTIMS[0] == 0: self.player['HP'] = 0
		if self.player['HPLOSS'] <= 0 and self.pause == 0:
			self.player['LIFES'] -= 1
			if self.player['LIFES'] > 0:
				self.ch_msc.play(database.SOUND['LOST'])
				self.pause = 3
				self.transiction(True,210)
				self.player['RECT'].x = database.PX
				self.player['RECT'].y = database.PY
				self.player['HP'] = 10
				self.player['HPLOSS'] = 10
				database.MONEY = database.STMONEY[database.WAVES[0]]
				self.pause = 2
				database.VICTIMS = [1,0]
				self.rendermap('level_' + str(database.MAP))
				self.transiction(False,0)
				self.ch_msc.play(database.SOUND['MAIN'])
				self.pause = 0
			else:
				self.ch_msc.play(database.SOUND['GAMEOVER'],-1)
				self.pause = 3
				self.mnu = 4
				self.text = 'Fim de Jogo'
				self.txty = 400

		#VICTORY
		if self.pause == 4:
			self.pause = 5
			database.MAP += 1
			self.transiction(True,210)
			if database.MAP < 2:
				if database.MAP == 1: self.etext = 'SEGUNDO ANDAR'
				if database.MAP == 2: self.etext = 'TERCEIRO ANDAR'
				if database.MAP == 3: self.etext = 'QUARTO ANDAR'
				if database.MAP == 4: self.etext = 'QUINTO ANDAR'
				if database.MAP == 5: self.etext = 'SEXTO ANDAR'
				if database.MAP == 6: self.etext = 'SÉTIMO ANDAR'
				while self.elevator > 0:
					self.elevator -= 5
					self.run()
				self.etext = ''
				self.elevator = 430
				self.rendermap('level_' + str(database.MAP))
				self.ch_msc.play(database.SOUND['MAIN'])
				self.transiction(False,0)
				self.text = 'ONDA 1'
				self.txty = 400
				self.pause = 0
			elif self.mnu < 4:
				self.mnu = 2
				self.ctb = 'background3'
				self.ch_msc.play(database.SOUND['CINEMATIC'],-1)
				self.transiction(False,55)
				self.dialog(['Finalmente salvei todos os cientistas',1])
				self.ctb = 'background5'
				self.dialog(['Bom...',1,'Pelo menos os que eu pude salvar',1])
				self.ctb = 'background3'
				self.dialog(['Mas o que importa é que eu nunca mais',1,'vou correr riscos outra vez',1])
				self.ctb = 'background6'
				self.dialog(['Agora vou sair pra comprar paçoca',1])
				self.ctb = 'background7'
				self.ch_msc.play(database.SOUND['EGG_RAP'],-1)
				self.player['LIFES'] = 0
				self.mnu = 4
				self.text = 'Parabéns meu consagrado!!'
				self.txty = 400

		#TILED MAP
		self.display.blit(self.tilmap[0][math.floor(self.tilemation)], (0 - self.cam.x, 0 - self.cam.y))
		self.display.blit(self.tilmap[1][math.floor(self.tilemation)], (0 - self.cam.x, 0 - self.cam.y))
		self.display.blit(self.tilmap[2][math.floor(self.tilemation)], (0 - self.cam.x, 0 - self.cam.y))
		
		#DEPTH
		dpth = 0
		for i in range(len(self.objects)):
			if i!= len(self.objects) - 1:
				if self.objects[i][2] > self.objects[i + 1][2]:
					self.objects.insert(i, self.objects[i + 1])
					del self.objects[i + 2]
		
		y = 0
		while y < len(self.objects):
			if self.objects[y][0] == 0:
				#PLAYER
				if self.player['DMGTIM'] > 0:
					self.player['DMGTIM'] -= 1
				if self.pause == 3: self.player['DMGTIM'] = 0
				if self.player['DMGTIM'] % 2 == 0:
					if self.rectdebug == True: pygame.draw.rect(self.display, (255,0,0), self.player['RECT'])
					self.display.blit(pygame.image.load('Sprites/shade.png'),(self.player['RECT'].x - self.cam.x - 1,self.player['RECT'].y - self.cam.y + int(self.player['RECT'].height/2) - 2))
					self.display.blit(database.SPRITES[self.player['SPRITE']][math.floor(self.player['GIF'])],(self.player['RECT'].x - self.cam.x,self.player['RECT'].y - self.cam.y - 25))
					self.objects[y][2] = self.player['RECT'].y

				#TILE COLISION
				'''for t in range(2):
					for i in self.tilrect[t]:
						if self.colide(self.player['RECT'],i[1]) and self.pause == 0:
							if i[0] != 'WALL' and i[0] != 'NONE' and self.player['DIRECTION'] != 0:
								self.ch_stp.stop()
								self.ch_stp.play(database.SOUND['STEP_' + i[0]])
							if i[0] == 'GRASS':
								if self.player['DMGTIM'] == 0: self.player['HP'] -= 1; self.player['DMGTIM'] = 20'''
		
			#OBJECTS
			elif self.objects[y][0] == 1:
				for i in range(len(self.en)):
					if self.en[i]['N'] == self.objects[y][1]:
						if self.en[i]['HP'] > 0: self.enemy(self.en[i]); self.objects[y][2] = self.en[i]['RECT'].y
						else:
							del self.en[i]
							del self.objects[y]
							y -= 1
							break
			elif self.objects[y][0] == 2:
				for i in range(len(self.victims)):
					if self.victims[i]['N'] == self.objects[y][1]:
						if self.victims[i]['GET'] == False: self.victim(self.victims[i]); self.objects[y][2] = self.victims[i]['RECT'].y
						else:
							del self.victims[i]
							del self.objects[y]
							y -= 1
							break
			elif self.objects[y][0] == 3:
				for i in self.doors:
					if i['N'] == self.objects[y][1]: self.door(i); self.objects[y][2] = i['RECT'].y
			elif self.objects[y][0] == 5:
				for i in range(len(self.traps)):
					if self.traps[i]['N'] == self.objects[y][1]:
						if self.traps[i]['HP'] > 0: self.trap(self.traps[i]); self.objects[y][2] = self.traps[i]['RECT'].y
						else:
							del self.traps[i]
							del self.objects[y]
							y -= 1
							break
			y += 1

		y = 0
		while y < len(self.objects):
			if self.objects[y][0] == 4:
				for i in range(len(self.items)):
					if self.items[i]['N'] == self.objects[y][1]:
						if self.items[i]['GET'] == False: self.item(self.items[i]); self.objects[y][2] = self.items[i]['RECT'].y
						else:
							del self.items[i]
							del self.objects[y]
							y -= 1
							break
			y += 1

		for n in self.nodes:
			if self.rectdebug == True: pygame.draw.rect(self.display,(255,255,0),n['RECT'])

		#BULLETS & EXPLOSIONS
		for i in range(len(self.bullets)):
			if self.bullets[i]['DESTROY'] == False and len(self.en) > 0:
				get = False
				for e in range(len(self.en)):
					if self.en[e]['MOVE'] == self.bullets[i]['TARGET'] and self.en[e]['N'] == self.bullets[i]['FIND']: self.bullets[i]['FOLLOW'] = self.en[e]['RECT']; get = True; break
				if get == False:
					self.bullets[i]['DESTROY'] = True
				if self.bullets[i]['FOLLOW'] == None: self.bullets[i]['FOLLOW'] = self.en[0]['RECT']
				if self.pause < 3:
					if self.bullets[i]['RECT'].x < self.bullets[i]['FOLLOW'].x: self.bullets[i]['RECT'].x += 5
					if self.bullets[i]['RECT'].y < self.bullets[i]['FOLLOW'].y: self.bullets[i]['RECT'].y += 5
					if self.bullets[i]['RECT'].x > self.bullets[i]['FOLLOW'].x: self.bullets[i]['RECT'].x -= 5
					if self.bullets[i]['RECT'].y > self.bullets[i]['FOLLOW'].y: self.bullets[i]['RECT'].y -= 5
				self.bullets[i]['TRLTIM'] -= 1
				if self.bullets[i]['TRLTIM'] == 0:
					self.bullets[i]['TRLTIM'] = 3
					#self.trail.append({'RECT': pygame.Rect(self.bullets[i]['RECT'].x - self.cam.x, self.bullets[i]['RECT'].y - self.cam.y,10,10), 'SCALE': 5})
				self.display.blit(pygame.image.load('Sprites/bullet.png'), (self.bullets[i]['RECT'].x - self.cam.x, self.bullets[i]['RECT'].y - self.cam.y))
			else: del self.bullets[i]; break
		for i in range(len(self.trail)):
			if self.trail[i]['SCALE'] > 0:
				pygame.draw.circle(self.display, (10,10,10), (self.trail[i]['RECT'].x - self.cam.x, self.trail[i]['RECT'].y - self.cam.y), math.floor(self.trail[i]['SCALE']))
				self.trail[i]['SCALE'] -= 0.1
			else: del self.trail[i]; break
		for i in range(len(self.explosions)):
			if self.explosions[i]['GIF'] < 8:
				self.display.blit(database.SPRITES['EXPLODE'][self.explosions[i]['GIF']], (self.explosions[i]['RECT'].x - self.cam.x, self.explosions[i]['RECT'].y - self.cam.y))
				self.explosions[i]['GIF'] += 1
			else: del self.explosions[i]; break
		for i in range(len(self.ashes)):
			if self.ashes[i]['GIF'] < 9:
				self.display.blit(database.SPRITES['ASHES'][self.ashes[i]['GIF']], (self.ashes[i]['RECT'].x - self.cam.x, self.ashes[i]['RECT'].y - self.cam.y))
				self.ashes[i]['GIF'] += 1
			else: del self.ashes[i]; break

		#TRAP SET
		if self.trapset != '' and self.pause < 3:
			self.trapgif += 0.1
			if self.trapgif >= 2.0: self.trapgif = 0.0
			if self.mp.x > 30: xa = round((self.mp.x - 15)/30) * 30
			else: xa = 0
			if self.mp.y > 30: ya = round((self.mp.y - 15)/30) * 30
			else: ya = 0
			srf = pygame.Surface((20,20), pygame.SRCALPHA).convert()
			img = pygame.image.load('Sprites/trap_' + str(self.trapset) + '_0.png').convert()
			srf.blit(img,(0,0))
			srf.set_alpha(150)
			can = False
			for s in self.area:
				if self.colide(self.mp,s): can = True
			self.display.blit(pygame.image.load('Sprites/trapset_' + str(math.floor(self.trapgif)) + '.png'),(xa - self.cam.x, ya - self.cam.y))
			if can == True: self.display.blit(srf,(xa - self.cam.x + 5, ya - self.cam.y))

		#DAMAGE & UPGRADES
		if len(self.en) > 0:
			for i in self.en:
				if i['HPLOSS'] > i['HP']: i['HPLOSS'] -= 0.1
				if i['DMGSHW'] > 0:
					if i['DMGSHW'] < 10: a = (i['DMGSHW']/10) * 255
					else: a = 255
					pygame.draw.rect(self.display,(10,10,10,a),pygame.Rect(i['RECT'].x - self.cam.x - 5, i['RECT'].y - self.cam.y - 25,40,10))
					if i['HPLOSS'] > 0: pygame.draw.rect(self.display,(245,245,0,a),pygame.Rect(i['RECT'].x - self.cam.x - 10, i['RECT'].y - self.cam.y - 25,int(40/(i['MAXHP']/i['HPLOSS'])),10))
					if i['HP'] > 0: pygame.draw.rect(self.display,(245,78,65,a),pygame.Rect(i['RECT'].x - self.cam.x - 10, i['RECT'].y - self.cam.y - 25,int(40/(i['MAXHP']/i['HP'])),10))
					i['DMGSHW'] -= 1
		if len(self.traps) > 0:
			for i in self.traps:
				if i['HPLOSS'] > i['HP']: i['HPLOSS'] -= 0.1
				if i['DMGSHW'] > 0:
					if i['DMGSHW'] < 10: a = (i['DMGSHW']/10) * 255
					else: a = 255
					pygame.draw.rect(self.display,(10,10,10,a),pygame.Rect(i['RECT'].x - self.cam.x - 5, i['RECT'].y - self.cam.y - 25,40,10))
					if i['HPLOSS'] > 0: pygame.draw.rect(self.display,(245,245,0,a),pygame.Rect(i['RECT'].x - self.cam.x - 10, i['RECT'].y - self.cam.y - 25,int(40/(i['MAXHP']/i['HPLOSS'])),10))
					if i['HP'] > 0: pygame.draw.rect(self.display,(245,78,65,a),pygame.Rect(i['RECT'].x - self.cam.x - 10, i['RECT'].y - self.cam.y - 25,int(40/(i['MAXHP']/i['HP'])),10))
					i['DMGSHW'] -= 1

				if self.colide(i['RECT'], self.mp): i['UPGSHW'] = 1
				else: i['UPGSHW'] = 0
				if i['UPGSHW'] > 0:
					pygame.draw.rect(self.display,(10,10,10),pygame.Rect(i['RECT'].x - self.cam.x - 5, i['RECT'].y - self.cam.y - 25,60,15))
					self.display.blit(self.monotype.render('nível '+ str(i['UPGRADE']),True,(250,250,250)),(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y - 30))
					if i['UPGRADE'] < 5:
						if database.MONEY >= database.TRAPS[i['TYPE'] - 1]['PRICE'][i['UPGRADE'] + 1]:
							pygame.draw.rect(self.display,(10,250,10),pygame.Rect(i['RECT'].x - self.cam.x - 5, i['RECT'].y - self.cam.y - 10,60,15))
						else: pygame.draw.rect(self.display,(250,10,10),pygame.Rect(i['RECT'].x - self.cam.x - 5, i['RECT'].y - self.cam.y - 10,60,15))
						self.display.blit(self.monotype.render('$' + str(database.TRAPS[i['TYPE'] - 1]['PRICE'][i['UPGRADE'] + 1]),True,(10,10,10)),(i['RECT'].x - self.cam.x, i['RECT'].y - self.cam.y - 17))

		#MONEY & LIFE
		pygame.draw.rect(self.display, (10,10,10), pygame.Rect(0,0,self.displayzw,55))
		self.display.blit(self.monotype.render('$' + str(database.MONEY), True, (250,250,250)),(10, 30))

		if self.player['HPLOSS'] > self.player['HP']: self.player['HPLOSS'] -= 0.1
		pygame.draw.rect(self.display, (250,250,250), pygame.Rect(10,10,80,20))
		if self.player['HPLOSS'] > 0:
			pygame.draw.rect(self.display, (245,245,0), pygame.Rect(10,10,int(80/(10/self.player['HPLOSS'])),15))
			pygame.draw.rect(self.display, (216,151,30), pygame.Rect(10,25,int(80/(10/self.player['HPLOSS'])),5))
		if self.player['HP'] > 0:
			pygame.draw.rect(self.display, (245,78,65), pygame.Rect(10,10,int(80/(10/self.player['HP'])),15))
			pygame.draw.rect(self.display, (216,67,92), pygame.Rect(10,25,int(80/(10/self.player['HP'])),5))
		if self.player['LIFES'] > 0:
			for i in range(self.player['LIFES']):
				self.display.blit(pygame.image.load('Sprites/life.png'),(520 + (i * 20), 20))

		#ENEMIES & VICTIMS
		self.display.blit(pygame.image.load('Sprites/robot_0_0.png'),(300, 20))
		self.display.blit(self.monotype.render(str(database.ENEMIES[0]) + '/' + str(database.ENEMIES[1]), True, (250,250,250)),(330, 15))
		self.display.blit(pygame.image.load('Sprites/victim_0_0.png'),(400, 15))
		self.display.blit(self.monotype.render(str(database.VICTIMS[0]) + '/' + str(database.VICTIMS[1]), True, (250,250,250)),(430, 15))

		#TRAPS
		for i in range(0,5):
			if database.MONEY >= database.TRAPS[i]['PRICE'][0]:
				pygame.draw.rect(self.display, (250,250,250), pygame.Rect(100 + ((i) * 35),5,30,30))
			else: pygame.draw.rect(self.display, (165,165,165), pygame.Rect(100 + ((i) * 35),5,30,30))
			self.display.blit(pygame.image.load('Sprites/icon_' + str(i + 1) + '.png'),(100 + ((i) * 35),5))
			if self.tindex == i + 1:
				pygame.draw.rect(self.display, (250,250,250), pygame.Rect(100 + ((i) * 35),35,30,20))
				self.display.blit(self.monotype.render(str(database.TRAPS[i]['PRICE'][0]), True, (10,10,10)),(105 + ((i) * 35), 30))
			else: self.display.blit(self.monotype.render(str(database.TRAPS[i]['PRICE'][0]), True, (250,250,250)),(105 + ((i) * 35), 30))
		i += 1

		#BACKGROUND
		if self.mnu != 3:
			if self.ctb != None: self.display.blit(pygame.image.load('Sprites/' + self.ctb + '.png'),(0,0))
			else: pygame.draw.rect(self.display,(0,0,0),pygame.Rect(0,0,600,400))
		if self.opt == 10:
			if self.logalpha < 255: self.logalpha += 10
			srf = pygame.Surface((355,172), pygame.SRCALPHA, 32)
			srf.convert_alpha()
			img = pygame.image.load('Sprites/logo.png')
			img.set_alpha(self.logalpha)
			srf.blit(img,(0,0))
			self.display.blit(srf,(120, 100))
		
		#BLACK BARS
		pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(0,0,600,self.winbar))
		pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(0,400,600,-self.winbar))
			
		#ELEVATOR
		if self.etext != '':
			l1 = 0
			for l in self.text:
				if l in ['m','w','M','Q','T','U','V','W','Y','?']: l1 += 8
				elif l in ['f','r']: l1 += 6
				elif l in ['J']: l1 += 5
				elif l in ['l']: l1 += 4
				elif l in ['i','I','!','.',',']: l1 += 2
				else: l1 += 7
			self.display.blit(self.monotype.render(self.etext, True, (250,250,250)),(250 - l1, 180))
		if self.elevator > 0 and self.elevator < 430:
			self.display.blit(pygame.image.load('Sprites/elevator.png'),(250,self.elevator - 25))
			if database.MAP > 0:
				for v in range(database.VICTIMS[0]): self.display.blit(pygame.image.load('Sprites/victim_0_0.png'),(265 + (v * 15),self.elevator - 43))
			self.display.blit(pygame.image.load('Sprites/char_stand_0.png'),(290,self.elevator - 40))
			
		#TEXT
		if self.text != '':
			l1 = 0
			for l in self.text:
				if l in ['m','w','M','Q','T','U','V','W','Y','?']: l1 += 8
				elif l in ['f','r']: l1 += 6
				elif l in ['J']: l1 += 5
				elif l in ['l']: l1 += 4
				elif l in ['i','I','!','.',',']: l1 += 2
				else: l1 += 7

			srf = pygame.Surface((600,10))
			srf.set_alpha(100)
			srf.fill((0, 0, 0))
			self.txtsrf.set_alpha(self.logalpha)
			self.display.blit(srf, (0,70 + self.txty))
			self.display.blit(self.txtsrf,(-40 + self.ptmove, 20 + self.txty))
			self.ptmove += 1
			if self.ptmove > 40: self.ptmove = 0
			rct = pygame.Surface((l1 + 20,50))
			rct.set_alpha(self.logalpha)
			rct.fill((250, 250, 250))
			self.display.blit(rct,(329 - l1,20 + self.txty))
			#pygame.draw.rect(self.display, (250, 250, 250), pygame.Rect(329 - l1,20 + self.txty,l1 + 20,50))
			self.display.blit(self.monotype.render(self.text, True, (10,10,10)),(339 - l1, 30 + self.txty))
			if self.txty > 150 and self.txty < 240: self.txty -= 2
			elif self.txty >= 240: self.txty -= 20
			elif self.player['LIFES'] != 0: self.txty -= 20
			if self.txty == -100:
				self.text = ''
				if self.mnu == 3:
					self.pause = 0

		#TITLE
		if self.mnu == 1:
			self.display.blit(self.monotype.render('Criado por Matt Kai', True, (250,250,250)),(200,150))
			self.display.blit(self.monotype.render('Twitter/GitHub: @KaiXtr', True, (250,250,250)),(200,170))
			self.display.blit(self.monotype.render('Feito em Python', True, (250,250,250)),(200,190))
			self.display.blit(self.monotype.render('Para #corona_jam (2020)', True, (250,250,250)),(200,210))
		if self.mnu == 2 and self.dlg == [] and self.opt != 10 and self.ctb == 'background1':
			if self.logalpha < 255: self.logalpha += 10
			srf = pygame.Surface((355,172), pygame.SRCALPHA, 32)
			srf.convert_alpha()
			img = pygame.image.load('Sprites/logo.png')
			img.set_alpha(self.logalpha)
			srf.blit(img,(0,0))
			self.display.blit(srf,(120, 100))
			if self.winbar == 55:
				op1 = pygame.Rect(170,355,60,35)
				op2 = pygame.Rect(310,355,70,35)
				if self.tut == False:
					if self.colide(self.mp,op1): pygame.draw.rect(self.display,(145,35,254),op1)
					if self.colide(self.mp,op2): pygame.draw.rect(self.display,(145,35,254),op2)
					self.display.blit(self.monotype.render('jogar', True, (250,250,250)),(180,360))
					self.display.blit(self.monotype.render('ajustes', True, (250,250,250)),(320,360))
				elif self.opt == 0:
					if self.colide(self.mp,op1): pygame.draw.rect(self.display,(145,35,254),op1)
					self.display.blit(self.monotype.render('ok', True, (250,250,250)),(180,360))
				elif self.opt == 1:
					if self.colide(self.mp,op2): pygame.draw.rect(self.display,(145,35,254),op2)
					self.display.blit(self.monotype.render('voltar', True, (250,250,250)),(320,360))

		#DIALOGS
		if self.dlg != []:
			self.display.blit(self.monotype.render(self.dlg[0], True, (250,250,250)),(100,360))
			if self.dlgping == True: self.display.blit(pygame.image.load('Sprites/ping.png'),(480,365))

		#TUTORIAL
		if self.tutfa > 0:
			pygame.draw.rect(self.display, (10,10,10), pygame.Rect(290 - int(self.tutfa/2), 185 - int(self.tutfa/4), 10 + self.tutfa, 10 + int(self.tutfa/2)))
			srf = pygame.Surface((self.tutfa,int(self.tutfa/2)))
			srf.blit(self.tutsrf,(0,0))
			self.display.blit(srf, (295 - int(self.tutfa/2), 190 - int(self.tutfa/4)))
		if self.tut == True:
			if self.opt == 0 and self.tutfa < 320: self.tutfa += 20
			if self.opt == 1 and self.tutfa < 220: self.tutfa += 20
			if self.tutfa == 320 and self.opt == 0:
				self.display.blit(self.monotype.render('Use a roda do mouse para escolher', True, (10,10,10)),(165,120))
				self.display.blit(self.monotype.render('a arma que deseja comprar, e clique', True, (10,10,10)),(165,140))
				self.display.blit(self.monotype.render('com o botão esquerdo, aperte o botão', True, (10,10,10)),(165,160))
				self.display.blit(self.monotype.render('direito para cancelar. Use as', True, (10,10,10)),(165,180))
				self.display.blit(self.monotype.render('armadilhas para atacar os robôs', True, (10,10,10)),(165,200))
				self.display.blit(self.monotype.render('e ganhar dinheiro. Seu objetivo é', True, (10,10,10)),(165,220))
				self.display.blit(self.monotype.render('enfrentar todas as ondas do andar.', True, (10,10,10)),(165,240))
			elif self.tutfa == 220 and self.opt == 1:
				sb1 = pygame.Rect(260,165,110,15)
				sb2 = pygame.Rect(260,195,110,15)
				self.display.blit(self.monotype.render('sfx: ', True, (10,10,10)),(205,160))
				if self.colide(self.mp,sb1): pygame.draw.rect(self.display, (250,250,10), sb1)
				else: pygame.draw.rect(self.display, (130,130,130), sb1)
				pygame.draw.rect(self.display, (10,10,10), pygame.Rect(260 + int(database.SFX * 100),165,10,15))
				self.display.blit(self.monotype.render('música:', True, (10,10,10)),(205,190))
				if self.colide(self.mp,sb2): pygame.draw.rect(self.display, (250,250,10), sb2)
				else: pygame.draw.rect(self.display, (130,130,130), sb2)
				pygame.draw.rect(self.display, (10,10,10), pygame.Rect(260 + int(database.MSC * 100),195,10,15))

		else:
			if self.tutfa > 0: self.tutfa -= 20
			
		#CAMERA
		'''if self.speakin == 0:
			self.cam.x += int((self.player['RECT'].x  - self.cam.x - self.displayzw/2)/15)
			self.cam.y += int((self.player['RECT'].y  - self.cam.y - self.displayzh/2)/15)
		else:
			self.cam.x += int((self.speakin.x  - self.cam.x - self.displayzw/2)/15)
			self.cam.y += int((self.speakin.y  - self.cam.y - self.displayzh/2)/15)

		if self.cam.x < 0: self.cam.x = 0
		if self.cam.y < 0: self.cam.y = 0
		if self.cam.x > (self.map.width * self.map.tilewidth) - self.displayzw: self.cam.x = (self.map.width * self.map.tilewidth) - self.displayzw
		if self.cam.y > (self.map.height * self.map.tileheight) - self.displayzh: self.cam.y = (self.map.height * self.map.tileheight) - self.displayzh'''

		self.display.blit(pygame.image.load('Sprites/cursor_' + str(self.cursor) + '.png'),(self.mp.x,self.mp.y))
		self.screen.blit(pygame.transform.scale(self.display, (1200, 800)), (0, 0))
		pygame.display.update()
		pygame.display.flip()
	
	def run(self):
		self.glock.tick(self.FPS)
		self.events()
		self.draw()

g = Game()
while True:
	g.run()