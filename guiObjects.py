import pygame,numpy, templates, os
pygame.init()
class confirm(object):
	def __init__(self,parent,surf,rect,msg,onclick):
		self.onclick = onclick
		self.surface = surf
		self.parent = parent
		self.surf = pygame.Surface((rect[2],rect[3]))
		self.surf.fill((200,200,200))
		self.pos = (rect[0],rect[1])
		self.onclick = onclick
		tx = (self.surf.get_width() - msg.get_rect()[2]) / 2
		ty = surf.get_width() * 0.05
		f = pygame.font.SysFont('Arial',12)
		self.surf.blit(msg,(tx,ty))
		b1t = f.render("Ok",False,(0,0,0))
		self.b1x = int( (self.surf.get_width() - b1t.get_rect()[2]) / 2 - 20)
		self.b1y = int(self.surf.get_height() * 0.80)
		self.b1 = button(
			self.surf,
			(
				self.b1x,
				self.b1y,
				b1t.get_rect()[2] + 20,
				b1t.get_rect()[3] + 10
			),
			(128,128,128),
			self.clickT,
			text=b1t,
			hover=(140,140,140),
			outer_offset=self.pos
			)
		b2t = f.render("Cancel",False,(0,0,0))
		self.b2x = int(self.surf.get_width() / 2 + b2t.get_rect()[2] / 2 + 20)
		self.b2y = int(self.surf.get_height() * 0.80)
		self.b2 = button(
			self.surf,
			(
				self.b2x,
				self.b2y,
				b2t.get_rect()[2] + 20,
				b2t.get_rect()[3] + 10
			),
			(128,128,128),
			self.clickF,
			text=b2t,
			hover=(140,140,140),
			outer_offset=self.pos
			)
	def clickT(self):
		self.parent.current_page = "pixel_editor"
		self.onclick(True)
	def clickF(self):
		self.parent.current_page = "pixel_editor"
		self.onclick(False)
	def check_click(self):
		self.b1.check_click()
		self.b2.check_click()
	def update(self):
		self.b1.try_hover()
		self.b2.try_hover()
		self.b1.draw()
		self.b2.draw()
	def draw(self):
		pygame.draw.rect(
			self.surf,
			(0,0,0),
			(0,0,self.surf.get_width(),self.surf.get_height()),
			1
			)
		self.surface.blit(self.surf,self.pos)
class button(object):
	def __init__(self,surf,rect,color,onclick,text=None,hover=None,text_align="center",padding=0,right_text=None,outer_offset=None,text_vertical=None):
		self.rect = rect
		self.normColor = color
		self.color = color
		self.surf = surf
		self.onclick = onclick
		self.right_text = right_text
		self.outer_offset = outer_offset
		# center text
		self.text = text
		if self.text != None:
			self.ty = rect [1] + (rect[3] - text.get_rect()[3]) / 2
			if text_align == "center":
				self.tx = rect[0] + (rect[2] - text.get_rect()[2]) / 2
			elif text_align == "left":
				self.tx = rect[0] + padding
			if text_vertical != None:
				self.ty = rect[1] + rect[3] - text.get_rect()[3] - 10
		if self.right_text != None:
			self.rtx = self.rect[0] + self.rect[2] - self.right_text.get_rect()[2] - padding
			self.rty = self.rect[1] + self.rect[3] - (self.rect[3] / 2) - self.right_text.get_rect()[3] / 2
		self.hover = hover
	def draw(self):
		try:
			pygame.draw.rect(self.surf,self.color,self.rect)
		except:
			print("GOT ERROR FOR COLOR:")
			print(self.color)
		if self.text != None:
			self.surf.blit(self.text,(self.tx,self.ty))
		if self.right_text != None:
			self.surf.blit(self.right_text,(self.rtx,self.rty))
	def try_hover(self):
		if self.get_hover():
			if self.hover != None:
				self.color = self.hover
		else:
			self.color = self.normColor
	def get_hover(self):
		mx,my = pygame.mouse.get_pos()
		if self.outer_offset == None:
			if mx in range(self.rect[0],self.rect[0] + self.rect[2] + 1) and my in range(self.rect[1],self.rect[3] + self.rect[1] + 1):
				return True
			else:
				return False
		else:
			x1 = int(self.rect[0] + self.outer_offset[0])
			x2 = int(self.rect[0] + self.rect[2] + self.outer_offset[0])
			y1 = int(self.rect[1] + self.outer_offset[1])
			y2 = int(self.rect[1] + self.rect[3] + self.outer_offset[1])
			if mx in range(x1,x2 + 1) and my in range(y1,y2 + 1):
				return True
			else:
				return False
		pass
	def check_click(self):
		if self.get_hover():
			if pygame.mouse.get_pressed()[0]:
				self.onclick()
class weapon_load_window(object):
	def __init__(self,parent,surface):
		self.parent = parent
		self.surface = surface
		self.surf = pygame.Surface((500,500))
		self.xoff = (self.parent.gui.screen.get_width() - self.surf.get_width()) / 2
		self.yoff = (self.parent.gui.screen.get_width() - self.surf.get_height()) / 2
		self.display = True
		self.buttons = []
		self.old_color = [None]
		bfont = pygame.font.SysFont("Arial",14)
		b1t = bfont.render("Load",False,(0,0,0))
		b1 = button(
			self.surf,
			(
				(self.surf.get_width() - (b1t.get_rect()[2] + 6)) / 2 - b1t.get_rect()[2] - 10,
				self.surf.get_height() - (b1t.get_rect()[3] + 6) - 10,
				b1t.get_rect()[2] + 6,
				b1t.get_rect()[3] + 6,
			),
			(200,200,200),
			self.parent.load_select,
			text=b1t,
			hover=(230,230,230),
			outer_offset=(self.xoff,self.yoff)
			)
		self.buttons.append(b1)
		b2t = bfont.render("Cancel",False,(0,0,0))
		b2t = button(
			self.surf,
			(
				(self.surf.get_width() - (b2t.get_rect()[2] + 6)) / 2 + b2t.get_rect()[2] + 10,
				self.surf.get_height() - (b2t.get_rect()[3] + 6) - 10,
				b2t.get_rect()[2] + 6,
				b2t.get_rect()[3] + 6,
			),
			(200,200,200),
			self.hide,
			text=b2t,
			hover=(230,230,230),
			outer_offset=(self.xoff,self.yoff)
			)
		self.buttons.append(b2t)
		self.items = self.build_weapon_index()
		for i in self.selection:
			self.selection[i].draw()
	def select_current(self):
		c = None
		for i in self.selection:
			if self.selection[i].get_hover():
				if self.old_color[0] != None:
					self.old_color[1].normColor = self.old_color[0]
					self.old_color[1].hover = self.old_color[2]
				c = i
				self.old_color = [self.selection[i].normColor,self.selection[i],self.selection[i].hover]
				self.selection[i].normColor = (self.selection[i].hover[0] + 10,self.selection[i].hover[1] + 10,self.selection[i].hover[2] + 10)
				self.selection[i].hover = (self.selection[i].hover[0] + 10,self.selection[i].hover[1] + 10,self.selection[i].hover[2] + 10)
		self.parent.current = c
	def show(self):
		self.parent.current_page = "popup"
		self.display = True
	def hide(self):
		self.display = False
		self.parent.current_page = "pixel_editor"
	def build_weapon_index(self):
		l = os.listdir("./user/weapons")
		self.mini_surf = pygame.Surface((420,400))
		self.mini_surf.fill((210,210,210))
		row = 0
		column = 0
		items = []
		buttons = {}
		f = pygame.font.SysFont('Arial',11)##pygame.font.Font("./fonts/courbd.ttf",14)
		for i in l:
			if i != "Thumbs.db":
				if len(i.split(".")[0]) > 16:
					n = i.split(".")[0][:16] + "..."
				else:
					n = i.split(".")[0]
				bx = column * 130 + (column + 1) * 10
				by = row * 100 + (row + 1) * 30
				bw = 120
				bh = 100
				b = button(
					self.mini_surf,
					(
						bx,
						by,
						bw,
						bh
					),
					(170,170,170),
					self.select_current,
					text=f.render(n,False,(0,0,0)),
					hover=(180,180,180),
					outer_offset=(self.xoff + 50,self.yoff + 50),
					text_vertical="bottom"
				)
				img = pygame.image.load("user/weapons/" + i).convert_alpha()
				img = pygame.transform.scale(img,(48,48))
				items.append(
					(
						img,
						(
							bx + (bw - img.get_width()) / 2,
							by + (bh - img.get_height()) / 2
						)
					)
					)
				buttons[i] = b
				# update row and column
				column+=1
				if column == 3:
					row += 1
					column = 0
		self.selection = buttons
		return items
	def update(self):
		if self.display:
			for b in self.buttons:
				b.try_hover()
			for b in self.selection:
				self.selection[b].try_hover()
	def check_click(self):
		if self.display:
			for b in self.buttons:
				b.check_click()
			for b in self.selection:
				self.selection[b].check_click()
	def draw(self):
		if self.display:
			# clear surf
			self.surf.fill((240,240,240))
			# render buttons
			for b in self.buttons:
				b.draw()
			for b in self.selection:
				self.selection[b].draw()
			for i in self.items:
				self.mini_surf.blit(i[0],i[1])
			# draw border
			pygame.draw.rect(
				self.surf,
				(0,0,0),
				(0,0,self.surf.get_width(),self.surf.get_height()),
				1
				)
			self.surf.blit(self.mini_surf,(50,50))
			self.surface.blit(self.surf,(self.xoff,self.yoff))
class mineral_window(object):
	def __init__(self,parent,gui,mineral_list):
		self.gui = gui
		self.surface = pygame.Surface((400,500))
		self.display = True
		self.scroll = 0
		self.parent = parent
		self.minerals = mineral_list
		self.generate_buttons()
		self.xoff = (self.gui.screen.get_width() - self.surface.get_width()) / 2
		self.yoff = (self.gui.screen.get_height() - self.surface.get_height()) / 2
		self.parent.current_mineral = self.minerals[0]
	def generate_buttons(self):
		self.buttons = []
		font = pygame.font.Font("fonts/comic.ttf",16)
		cfont = pygame.font.Font("fonts/courbd.ttf",16)
		for m in self.minerals:
			if self.minerals.index(m) == self.scroll:
				color = (26, 140, 255)
				x = int(10 / 2)
				y = self.minerals.index(m) * 31 - self.scroll * 31 + self.surface.get_height()/2 - int(5/2)
				height = 35
				width = self.surface.get_width() - 10
				self.current_button = button(
						self.surface,
						(
							x,
							y,
							width,
							height
						),
						color,
						self.p,
						text=font.render(m.name,False,(0,0,0)),
						text_align="left",
						padding=4,
						right_text=cfont.render(str(m.count),False,(0,0,0))
						)
			else:
				color = (170,170,170)
				x = 20/2
				y = self.minerals.index(m) * 31 - self.scroll * 31 + self.surface.get_height()/2
				height = 30
				width = self.surface.get_width() - 20
				self.buttons.append(button(
					self.surface,
					(
						x,
						y,
						width,
						height
					),
					color,
					self.p,
					text=font.render(m.name,False,(0,0,0)),
					text_align="left",
					padding=4,
					right_text=cfont.render(str(m.count),False,(0,0,0))
					))
	def p(self):
		# this is a pass function, since all the list items are actually buttons. (To cut down code size)
		pass
	def show(self):
		self.display = True
	def hide(self):
		self.display = False
	def try_scroll(self,event):
		if self.display:
			minn = 0
			maxx = len(self.minerals) - 1
			increment = 0
			if event.button == 4:
				increment = -1
			elif event.button == 5:
				increment = 1
			if self.scroll + increment >= minn and self.scroll + increment <= maxx:
				self.scroll+= increment
	def update(self):
		self.surface.fill((200,200,200))
		# refresh the button positions
		self.generate_buttons()
		for b in self.buttons:
			b.draw()
		self.current_button.draw()
		self.parent.current_mineral = self.minerals[self.scroll]
	def draw(self,surf):
		if self.display:
			surf.blit(self.surface,(self.xoff,self.yoff))
class pixel_editor(object):
	def __init__(self,parent,surf,dimensions,scale=18,background=(170,170,170)):
		self.screen = surf
		self.scale = scale
		self.background = background
		self.parent = parent
		self.surf = pygame.Surface((dimensions[0] * scale + dimensions[0] + 1,dimensions[1] * scale + dimensions[1] + 1))
		self.matrixX = int(self.screen.get_width() / 30)##self.screen.get_width() / 2 - (dimensions[0] * scale)/ 2
		self.matrixY = int(self.screen.get_height() / 20)##self.screen.get_height() / 2 - (dimensions[1] * scale)/ 2
		self.matrix_cache = numpy.empty(dimensions,dtype=object)
		for y in range(len(self.matrix_cache)):
			for x in range(len(self.matrix_cache[y])):
				self.matrix_cache[y][x] = background
		self.weapon_cache = numpy.empty(dimensions,dtype=object)
		for y in range(len(self.weapon_cache)):
			for x in range(len(self.weapon_cache[y])):
				self.weapon_cache[y][x] = None
		self.weapon_template = templates.weapons.sword
	def update(self):
		for y in range(len(self.matrix_cache)):
			for x in range(len(self.matrix_cache[y])):
				##print(self.matrix_cache[y][x])
				pygame.draw.rect(
					self.surf,
					self.matrix_cache[y][x],
					(
						# add x, add y to leave room for grid lines inbetween
						x * self.scale + (x + 1),
						y * self.scale + (y + 1),
						self.scale,
						self.scale
					)
					)
		pass
	def refresh(self):
		for y in range(len(self.matrix_cache)):
			for x in range(len(self.matrix_cache[y])):
				if self.weapon_cache[y][x] == None:
					if self.weapon_template[y][x]:
						self.matrix_cache[y][x] = self.background
					else:
						self.matrix_cache[y][x] = (self.background[0] - 60,self.background[1] - 60,self.background[2] - 60)
				else:
					self.matrix_cache[y][x] = self.weapon_cache[y][x].color
	def find_mouse_over_block(self):
		# for now, we're doing this the hard way
		for y in range(len(self.matrix_cache)):
			for x in range(len(self.matrix_cache[y])):
				x1 = x * self.scale + self.matrixX + x
				x2 = x1 + self.scale
				y1 = y * self.scale + self.matrixY + y
				y2 = y1 + self.scale
				mx,my = pygame.mouse.get_pos()
				if mx > x1 and mx < x2 and my > y1 and my < y2:
					return (x,y)
		return None
	def try_hover(self):
		block = self.find_mouse_over_block()
		if block != None:
			if self.weapon_template[block[1]][block[0]]:
				# brightens square when mouse is over
				# also has an overflow system if one of the colors reaches 255
				if self.weapon_cache[block[1]][block[0]] != None:
					R = self.weapon_cache[block[1]][block[0]].color[0] + 40
					G = self.weapon_cache[block[1]][block[0]].color[1] + 40
					B = self.weapon_cache[block[1]][block[0]].color[2] + 40
				else:
					R = self.background[0] + 40
					G = self.background[1] + 40
					B = self.background[2] + 40
				if R > 255:
					G +=R - 255
					R = 255
				if G > 255:
					B +=G - 255
					G = 255
				if B > 255:
					B = 255
				self.set_pixel(
					(
						block[0],
						block[1]
					),
					(
						R,
						G,
						B
						)
					)
	def check_click(self):
		block = self.find_mouse_over_block()
		if block != None:
			if pygame.mouse.get_pressed()[0]:
				self.try_place(
					(
						block[0],
						block[1]
					),
					self.parent.current_mineral
					)
	def set_pixel(self,xy,color):
		self.matrix_cache[xy[1]][xy[0]] = color
	def draw(self,surface):
		surface.blit(self.surf,(self.matrixX,self.matrixY))
	def try_place(self,pos,mineral):
		if self.parent.current_page == "pixel_editor":
			if self.weapon_template[pos[1]][pos[0]]:
				if self.parent.figurative_minerals[mineral.name].count > 0:
					if self.weapon_cache[pos[1]][pos[0]] != None:
						self.parent.figurative_minerals[self.weapon_cache[pos[1]][pos[0]].name].count+=1
					self.parent.figurative_minerals[mineral.name].count-=1
					self.weapon_cache[pos[1]][pos[0]] = mineral
	def clear(self):
		for y in range(len(self.weapon_cache)):
			for x in range(len(self.weapon_cache[y])):
				if self.weapon_cache[y][x] != None:
					# return that mineral to the user
					self.parent.parent.player.possesions.give(0,self.weapon_cache[y][x],1)
					# now reset that square/pixel
					self.weapon_cache[y][x] = None
				# if it is already <None>, it's fine. Leave it.
