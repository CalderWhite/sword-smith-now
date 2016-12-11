import pygame, time, random, sys
class gui(object):
	def __init__(self,parent):
		self.parent = parent
		parent.log("Initializing pygame...",user="GUI")
		pygame.init()
		self.screen = pygame.display.set_mode( (960,720))
		pygame.display.set_caption(parent.info["name"])
		parent.log("Loading images....")
		self.icon = pygame.image.load("images/icon.png")
		self.icon = pygame.transform.scale(self.icon, (32,32) )
		parent.log("Setting window icon...")
		pygame.display.set_icon(self.icon)
		parent.log("Loading and setting cursor...")
		self.cursor = pygame.image.load("images/cursor1.png").convert_alpha()
		pygame.mouse.set_visible(False);
		pass
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
		self.info = info
		self.log("Building gui...")
		self.gui = gui(self)
		self.page = None
		self.mouse = pygame.mouse
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
			# load all the rectangles
			# load all the text
			# play button/text
			x,y = self.gui.screen.get_size()
			x = x/2 - 20
			y=  y - 200
			##print(mx,my)
			if mx > 469 and mx < 543 and my > 521 and my < 541:
				color = (0,128,0)
				if self.mouse.get_pressed()[0]:
					self.log("Entering Realm 1...",user="REALMS")
					self.page = "realm_1"
					self.run_realm_explorer()
			else:
				color = (0,0,0)
			default_font = pygame.font.SysFont("monospace", 32,bold=True)
			play_text = default_font.render("Play",0,color)
			self.gui.screen.blit(play_text,(x,y))
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
