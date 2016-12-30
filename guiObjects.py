import pygame
pygame.init()
class button(object):
	def __init__(self,surf,rect,color,onclick,text=None,hover=None):
		self.rect = rect
		self.normColor = color
		self.color = color
		self.surf = surf
		self.onclick = onclick
		# center text
		self.text = text
		if self.text != None:
			self.tx = rect[0] + (rect[2] - text.get_rect()[2]) / 2
			self.ty = rect [1] + (rect[3] - text.get_rect()[3]) / 2
		self.hover = hover
	def draw(self):
		pygame.draw.rect(self.surf,self.color,self.rect)
		if self.text != None:
			self.surf.blit(self.text,(self.tx,self.ty))
	def try_hover(self):
		if self.get_hover():
			if self.hover != None:
				self.color = self.hover
		else:
			self.color = self.normColor
	def get_hover(self):
		mx,my = pygame.mouse.get_pos()
		if mx in range(self.rect[0],self.rect[0] + self.rect[2] + 1) and my in range(self.rect[1],self.rect[3] + self.rect[1] + 1):
			return True
		else:
			return False
		pass
	def check_click(self):
		if self.get_hover():
			if pygame.mouse.get_pressed()[0]:
				self.onclick()