# OpenStreetMap art drawing project
# Project was done at Electric Wonderland camp
# Authors: Goran Mahovlić, Igor Brkić, Ana Horvat, Paula Bučar, Mark Bilandžić, Jurica Zrna, Tomislav Mikić
# How it works?
# Show random water surfaces from random cities (currently from list) on random location of the graf(picture)


from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import matplotlib.pyplot as plt
from matplotlib import pyplot, transforms
import time
import random
import numpy as np
import cv2
from pygame.locals import *
from random import randint
import pygame
import sys

pygame.init()

screen_size_x = 1024
screen_size_y = 768
img_resize_x = 512
img_resize_y = 384
counter = 1
pic_ready = False
pic_generated = False

"Set screen"
#screen = pygame.display.set_mode((screen_size_x,screen_size_y),0,32)
screen = pygame.display.set_mode((screen_size_x,screen_size_y),pygame.FULLSCREEN)

base = pyplot.gca().transData
#Selecting few cities we want to get water surface from
cities = ["Vukovar", "Grad Ogulin","Grad Delnice","Knin", "Grad Sisak" ,"Grad Zaprešić" ,"Petrinja", "Zagreb", "Karlovac", "Split", "Varaždin", "Čakovec", "Koprivnica", "Lipine", "Garešnica"]

while True:
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif evt.type == KEYDOWN:
			#if evt.key == K_RETURN:
			print(evt.key)
			pygame.quit()
			sys.exit()

	numCity = []
	# Get random cites from our list 
	for CityX in range(random.randint(2,len(cities))):
		numCity.append(cities[CityX])
	# Used for random rotatio of water object
	rndRotation = random.randint(0,360)
	print("Rotation: ", rndRotation)
	# How many times to run main loop
	rndTimes = random.randint(1,3)
	print("MaxTimes: ", rndTimes)   
	# Random for displacing obects from centar
	rndNear = random.randint(1,1000)
	print("Near: ", rndNear)
	# Random do not inculde some object size
	rndRivers = random.randint(1,500)
	print("Rivers: ", rndRivers)
	for i in range(rndTimes):
		print("Times: ",i)
		for city in numCity:
			# Print each used city
			print(city)
			pygame.time.wait(100)
			try:
				areaUsed = Nominatim().query(city)
				# Query openstreetmap for all water surfaces in given area
				query = overpassQueryBuilder(area=areaUsed.areaId(), elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
				result = Overpass().query(query)
				# For all water surfaces in Cities
				for waters in result.elements():
					# Give object 1% of chance to be draw
					if random.randint(0,100) <= 10:
						continue
					try:
						# Add water poligon to map
						datastring = waters.geometry()
						x = [xx[0] for xx in datastring.coordinates[0]]
						y = [xx[1] for xx in datastring.coordinates[0]]
						xc = sum(x)/len(x)+random.random()/rndNear
						yc = sum(y)/len(y)+random.random()/rndNear
						x = [xx-xc for xx in x]
						y = [yy-yc for yy in y]
						# Add object rotation
						rot = transforms.Affine2D().rotate_deg(random.randint(0,rndRotation))
						# Cut random sizes
						if (len(x) < rndRivers and len(y) < rndRivers):
							# Plot each poligon with random line width
							if pic_generated:
								pic_generated = False
							else:
								plt.plot(x, y,linewidth=random.randint(1,7), transform = rot + base)
								print("Picture ready")
								#pic_ready = True
					except:
						pic_ready = False
						print("except Picture false")
						pass
					print("Picture ready2")	
			except ZeroDivisionError:
				pic_ready = False
				print("except Picture ready")
				pass
	print("Picture ready3")
	pic_ready = True
		
	# Get min and max graph
	if pic_ready == True:
		axes = plt.gca()
		x_min, x_max = axes.get_xlim()
		print("Xmax: ",x_min, x_max)
		y_min, y_max = axes.get_ylim()
		print("Ymax: ",y_min, y_max)
		# Do not print axis
		plt.axis('off')
		#Random zoom to graph 
		rndZoomX = random.randint(1,5)
		print("zoomX: ", rndZoomX)
		rndZoomY = random.randint(1,5)
		print("zoomY: ", rndZoomY)
		# Liit axis to get zoom
		plt.xlim(x_min/rndZoomX, x_max/rndZoomX)
		plt.xlim(y_min/rndZoomY, y_max/rndZoomY)
		plt.ion()
		plt.savefig('pic/generated.png', bbox_inches='tight')
		# Save as png - remove whitening
		# OpenCv convert to gray scale
		img = cv2.imread('pic/generated.png', cv2.IMREAD_GRAYSCALE)
		# Get number of white pixels
		n_white_pix = np.sum(img == 255)
		print('Number of white pixels:', n_white_pix)
		# What number of white is accepted
		if n_white_pix > 100000 and n_white_pix < 200000:
			# Show graph
			#plt.show()
			#plt.figure(dpi=300)
			if counter == 4:
				plt.savefig('pic/four.png', bbox_inches='tight')
				counter = counter + 1
				pic_generated = True
				plt.cla()
			elif counter == 3:
				plt.savefig('pic/three.png', bbox_inches='tight')
				counter = counter + 1
				pic_generated = True
				plt.cla()				
			elif counter == 2:
				plt.savefig('pic/two.png', bbox_inches='tight')
				counter = counter + 1
				pic_generated = True
				plt.cla()				
			elif counter == 1:
				plt.savefig('pic/one.png', bbox_inches='tight')
				counter = counter + 1
				pic_generated = True
				plt.cla()				
			else:
				counter = 1
				plt.cla()			
			#mng = plt.get_current_fig_manager()
			# Maximise windows
			#mng.window.showMaximized()
			#mng.window.state("normal")
			# Pause to check picture     
			#plt.pause(10)
			#plt.close('all')
	#    try:
		"Load images"
		img_one = pygame.image.load("pic/one.png").convert_alpha()
		img_two = pygame.image.load("pic/two.png").convert_alpha()
		img_three = pygame.image.load("pic/three.png").convert_alpha()
		img_four = pygame.image.load("pic/four.png").convert_alpha()

		"Resize images"
		img_one_resized = pygame.transform.scale(img_one, (img_resize_x, img_resize_y))
		img_two_resized = pygame.transform.scale(img_two, (img_resize_x, img_resize_y))
		img_three_resized = pygame.transform.scale(img_three, (img_resize_x, img_resize_y))
		img_four_resized = pygame.transform.scale(img_four, (img_resize_x, img_resize_y))

		"Fill background"
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((0, 0, 0))

		pygame.display.update()
		#pygame.time.wait(10000)

		screen.blit(background, (0, 0))
		screen.blit(img_one,(0,0))
		screen.blit(img_two,(0,img_resize_y))
		screen.blit(img_three,(img_resize_x,0))
		screen.blit(img_four,(img_resize_x,img_resize_y))

		pygame.display.update()
		pygame.time.wait(10000)
		pic_ready = False

#    except:
#        pass        