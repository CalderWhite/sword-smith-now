import pygame
class start_page(object):
	def __init__(self):
		self.default_font = pygame.font.SysFont("monospace", 32)
		self.play_text = self.default_font.render("Play",0,(0,0,0))
pygame.init()
start_page = start_page()