from PIL import Image
import random, os, numpy
class builder(object):
	def __init__(self):
		pass
	def get_floors(self):
		floor_dir = os.listdir("./images/world_pieces/sized/floors")
		##floors = {}
		##for i in floors:
		##	floors[i.split(".")[-1]] = i
		##self.floors = floors
		return floor_dir
	def generate(self):
		chunk_matrix = numpy.empty([6,6],dtype=object)
		width = random.randrange(2,5)
		height = random.randrange(2,5)
		floor_index = self.get_floors()
		biome = random.randrange(0,len(floor_index))
		for y in range(0,height):
			for x in range(0,width):
				chunk_matrix[x][y] = floor_index[biome]
		print(chunk_matrix)
if __name__ == '__main__':
	b = builder()
	b.generate()
