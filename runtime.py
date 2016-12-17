import pygame, time, random, sys
class new_player(object):
	def __init__(self,name,parent):
		self.name = name
		self.x = 0#parent.current_chunk.get_rect()[0] / 2
		self.y = 0#parent.current_chunk.get_rect()[1] / 2
		self.speed = 10
		self.hitbox = (60,120)
		self.parent = parent
	def check_movement(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
			self.speed = 10
		elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
			self.speed = 0.5
		else:
			self.speed = 1
		# create offset variables so we aren't changing the player's x and y right away
		xoff = 0
		yoff = 0
		# set offset variables
		if keys[pygame.K_w]:
			# positive effect
			yoff+=1 * self.speed
			pass
		if keys[pygame.K_s]:
			# negative effect
			yoff-=1 * self.speed
			pass
		if keys[pygame.K_d]:
			# positive effect
			xoff+=1 * self.speed
			pass
		if keys[pygame.K_a]:
			# negative effect
			xoff-=1 * self.speed
			pass
		check = self.check_collision(xoff,yoff)
		#print(check)
		if check == True:
			self.x+= xoff
			self.y+= yoff
		else:
			self.x,self.y = check
	def check_collision(self,xoff,yoff):
		# first check outline
		useless1,useless2,w,h=self.parent.current_chunk.get_rect()
		#print(w,h)
		# at some point I may want to change this, so I'll just use these variables from the start.
		minx = (w/2) * -1
		miny = h/2 * -1
		maxx = w/2
		maxy = h/2
		newx = self.x + xoff
		newy = self.y + yoff
		rx = None
		ret = False
		print(newx,newy)
		if newy > maxy:
			newy = maxy
			ret = True
		elif newy < miny:
			newy = miny
			ret = True
		if newx > maxx:
			newx = maxx
			ret = True
		elif newx < minx:
			newx = minx
			ret = True
		if ret:
			return (newx,newy)
		# now check all the game/gui's objects
		for obj in self.parent.gui.chunk_objects:
			rx = None
			ry = None
			pass
		return True
class gui(object):
	def __init__(self,parent):
		self.parent = parent
		parent.log("Initializing pygame...",user="GUI")
		pygame.init()
		self.screen = pygame.display.set_mode( (550,550))
		pygame.display.set_caption(parent.info["name"])
		parent.log("Loading images....",user="GUI")
		self.icon = pygame.image.load("images/icon.png")
		self.icon = pygame.transform.scale(self.icon, (32,32) )
		parent.log("Setting window icon...",user="GUI")
		pygame.display.set_icon(self.icon)
		parent.log("Loading and setting cursor...",user="GUI")
		self.cursor = pygame.image.load("images/cursor1.png").convert_alpha()
		pygame.mouse.set_visible(False);
		parent.log("Loading chunks...",user="GUI")
		self.load_chunks()
		parent.log("Loading objects [trees,bushes, etc.]...")
		self.chunk_objects = []
		pass
	def load_chunks(self):
		if self.parent.mode == 1:
			# only for dev mode
			self.chunks = []
			self.chunks.append(pygame.image.load("./saves/new_chunk.png"))
class game_kernel(object):
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
		self.log("Loading player...")
	def quit(self):
		self.log("Quit event activated. Stopping game.")
		self.page = None
		self.stop == True
		pygame.quit()
	def game_loop(self):
		pass
	def run_start(self):
		self.log("Entering Start Page",user="REALMS")
		self.page = "startup"
		self.gui.screen.fill( (255,255,255) )
		clock = pygame.time.Clock()
		while self.page == "startup":
			self.stop = False
			# check events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
					break
					pass
			if self.stop == False:
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
						break
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
	def realm_explorer_init(self):
		if self.mode == 1:
			self.current_chunk = self.gui.chunks[0]
			self.player = new_player("Developer",self)
	def run_realm_explorer(self):
		self.page = "realm_1"
		self.stop = False
		self.realm_explorer_init()
		if self.mode == 1:
			self.current_chunk = self.gui.chunks[0]
		while self.page == "realm_1":
			##print(self.stop)
			if self.stop == False:
				# clear
				self.gui.screen.fill( (255,255,255) )
				# load values
				mx,my = self.mouse.get_pos()
				height,width = pygame.display.get_surface().get_size()
				# modify player's position accordingly
				# speed modification
				self.player.check_movement()
				#print(self.player.x,self.player.y)
				# load & render background according to player's xy
				crop = pygame.Surface(pygame.display.get_surface().get_size())
				# invert the y in offsets so we get a four quadrent coordinet system
				# we also add half the height and width of the chunk to create the four quadrent system
				# ---------------------------------------------------------------------------------------------
				# subtract width and height (divided by two) to accomodate for the display
				# Explanation:
				# if the offset was 0,0 (player's x and y would be (-7200,7200)) then
				# it would display the top left corner, but It wouldn't go off screen, meaning the PLAYER isn't acutally
				# at 0,0 ; they're at (width/,height/2)
				# Consequently if the player was at the very bottom of the chunk, there would be nothing since they are off the chunk.
				# DERP idk ^^^
				xo = (int(self.gui.chunks[0].get_size()[0] / 2) + self.player.x) - width / 2
				yo = (int(self.gui.chunks[0].get_size()[1] / 2 + (self.player.y * -1))) - height / 2
				crop.blit(self.current_chunk,(0,0),(xo,yo,width,height))
				self.gui.screen.blit(crop,(0,0))
				# render player
				width,height = self.player.hitbox
				dw,dh = pygame.display.get_surface().get_size()
				# the x,y definitions look weird, but that's just because I want the player to be at zero forever
				x = (dw / 2) - width / 2
				y = (dh / 2) - height / 2
				pygame.draw.rect(self.gui.screen,(255,0,0),[x,y,width,height],1)
				# render mouse
				x = mx - (self.gui.cursor.get_height() / 2)
				y = my - (self.gui.cursor.get_width() / 2)
				self.gui.screen.blit(self.gui.cursor,(x,y))
				# finally, update
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.log("Quit event activated. Stopping game.")
						self.page = None
						self.stop == True
						pygame.quit()
						break


def main(parent):
	if parent == None:
		print("Program cannot run without a launcher.")
	else:
		if parent.mode == 0:
			pass
		elif parent.mode == 1:
			parent.log("Beginning runtime boot.",user="GAME")
			g = game_kernel(parent.info,dev_window=parent)
			g.run_start()
			"""
			try:
				g = game_kernel(parent.info,dev_window=parent)
				g.run_start()
			except:
				e = sys.exc_info()
				parent.log("Exception:",level="CRITICAL",user="GAME")
				parent.log(str(e[1]),level="CRITICAL",user="GAME")
				parent.log("File: [%s]" % (str(e[2].tb_frame.f_code.co_filename)),level="CRITICAL",user="GAME")
				parent.log("Line number: [" + str(e[2].tb_lineno) + "]",level="CRITICAL",user="GAME")
				pygame.quit()
			"""
			print("Done")
		elif parent.mode == 2:
			##parent.log("Running in cheat mode.",user="GAME")
			pass
