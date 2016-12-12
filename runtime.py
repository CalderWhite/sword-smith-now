import pygame, time, random, sys
class new_player(object):
	def __init__(self,name):
		self.name = name
		self.x = 0
		self.y = 0
		self.speed = 10
class gui(object):
	def __init__(self,parent):
		self.parent = parent
		parent.log("Initializing pygame...",user="GUI")
		pygame.init()
		self.screen = pygame.display.set_mode( (450,450))
		pygame.display.set_caption(parent.info["name"])
		parent.log("Loading images....",user="GUI")
		self.icon = pygame.image.load("images/icon.png")
		self.icon = pygame.transform.scale(self.icon, (32,32) )
		parent.log("Setting window icon...")
		pygame.display.set_icon(self.icon)
		parent.log("Loading and setting cursor...",user="GUI")
		self.cursor = pygame.image.load("images/cursor1.png").convert_alpha()
		pygame.mouse.set_visible(False);
		parent.log("Loading chunks...",user="GUI")
		self.load_chunks()
		pass
	def load_chunks(self):
		if self.parent.mode == 1:
			# only for dev mode
			self.chunks = []
			self.chunks.append(pygame.image.load("./saves/chunk_1.png"))
class game(object):
	def log(self,msg,level="INFO",user="GAME"):
		if self.mode == 1:
			# will only log stuff if in developer mode
			self.dev.log(msg,level=level,user=user)
	def __init__(self,info,dev_window=None,mode=0):
		self.mode = mode
		#automatically change mode to 1 if a dev window is supplied
		if dev_window != None:
			self.mode = 1
			self.dev = dev_window
			self.player = new_player("Developer")
		self.info = info
		self.log("Building gui...")
		self.gui = gui(self)
		self.page = None
		self.mouse = pygame.mouse
		self.log("Loading player...")
	def game_loop(self):
		pass
	def run_start(self):
		self.log("Entering Start Page",user="REALMS")
		self.page = "startup"
		self.gui.screen.fill( (255,255,255) )
		clock = pygame.time.Clock()
		while self.page == "startup":
			# check events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.log("Quit event activated. Stopping game.")
					self.page = None
					pygame.quit()
					pass
			self.gui.screen.fill( (255,255,255) )
			mx,my = self.mouse.get_pos()
			height,width = pygame.display.get_surface().get_size()
			# load all the rectangles
			# load all the text
			# play button/text
			x,y = self.gui.screen.get_size()
			x = x/2 - 20
			y=  y - (height/3.6)
			##print(mx,my)
			default_font = pygame.font.SysFont("monospace", 32,bold=True)
			play_text = default_font.render("Play",0,(0,0,0))
			#use the text rectangle
			empyty1,empty2,tw,th = tuple(play_text.get_rect())
			if mx > x and mx < (x + tw) and my > y and my < (y + th):
				color = (0,128,0)
				#play_text.set_colorkey(color)
				if self.mouse.get_pressed()[0]:
					self.log("Entering Realm 1...",user="REALMS")
					self.page = "realm_1"
					self.run_realm_explorer()
			else:
				color = (0,0,0)
				#play_text.set_colorkey(color)
				pass
			new_text = default_font.render("Play",0,color)
			self.gui.screen.blit(new_text,(x,y))
			# blit mouse last
			x = mx - (self.gui.cursor.get_height() / 2)
			y = my - (self.gui.cursor.get_width() / 2)
			self.gui.screen.blit(self.gui.cursor,(x,y))
			# refresh
			pygame.display.update()
	def run_realm_explorer(self):
		self.page = "realm_1"
		while self.page == "realm_1":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.log("Quit event activated. Stopping game.")
					self.page = None
					pygame.quit()
			# clear
			self.gui.screen.fill( (255,255,255) )
			# load values
			mx,my = self.mouse.get_pos()
			height,width = pygame.display.get_surface().get_size()
			# modify player's position accordingly
			# speed modification
			keys = pygame.key.get_pressed()
			if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
				self.player.speed = 10
			elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
				self.player.speed = 0.5
			else:
				self.player.speed = 1
			# movement keys
			if keys[pygame.K_w]:
				# positive effect
				self.player.y+=1 * self.player.speed
				pass
			if keys[pygame.K_s]:
				# negative effect
				self.player.y-=1 * self.player.speed
				pass
			if keys[pygame.K_d]:
				# positive effect
				self.player.x+=1 * self.player.speed
				pass
			if keys[pygame.K_a]:
				# negative effect
				self.player.x-=1 * self.player.speed
				pass
			#print(self.player.x,self.player.y)
			# load & render background according to player's xy
			crop = pygame.Surface(pygame.display.get_surface().get_size())
			# invert the y in offsets so we get a four quadrent coordinet system
			# we also add half the height and width of the chunk to create the four quadrent system

			crop.blit(self.gui.chunks[0],(0,0),(int(self.gui.chunks[0].get_size()[0] / 2) + self.player.x,int(self.gui.chunks[0].get_size()[1] / 2) + (self.player.y * -1),width,height))
			self.gui.screen.blit(crop,(-1,-1))
			# render mouse
			x = mx - (self.gui.cursor.get_height() / 2)
			y = my - (self.gui.cursor.get_width() / 2)
			self.gui.screen.blit(self.gui.cursor,(x,y))
			# finally, update
			pygame.display.update()


def main(parent):
	if parent == None:
		print("Program cannot run without a launcher.")
	else:
		if parent.mode == 0:
			pass
		elif parent.mode == 1:
			parent.log("Beginning runtime boot.",user="GAME")
			g = game(parent.info,dev_window=parent)
			g.run_start()
		elif parent.mode == 2:
			##parent.log("Running in cheat mode.",user="GAME")
			pass
