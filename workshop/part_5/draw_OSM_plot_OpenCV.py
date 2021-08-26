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

#Selecting few cities we want to get water surface from
cities = ["Grad Ogulin","Grad Delnice","Petrinja", "Zagreb", "Karlovac"]

while 1:
	numCity = []
	# Get random cites from our list 
	for CityX in range(random.randint(2,len(cities))):
		numCity.append(cities[CityX])
	base = pyplot.gca().transData
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
			try:
				areaUsed = Nominatim().query(city)
				# Query openstreetmap for all water surfaces in given area
				query = overpassQueryBuilder(area=areaUsed.areaId(), elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
				result = Overpass().query(query)
				# For all water surfaces in Cities
				for waters in result.elements():
					# Give object 2% of chance to be draw
					if random.randint(0,100) > 50:
						continue
					else:
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
								plt.plot(x, y,linewidth=random.randint(1,7), transform = rot + base)
						except:
							pass
			except ZeroDivisionError:
				pass
	# Get min and max graph
	axes = plt.gca()
	x_min, x_max = axes.get_xlim()
	print("Xmax: ",x_min, x_max)	
	y_min, y_max = axes.get_ylim()
	print("Ymax: ",y_min, y_max)
	# Do not print axis
	plt.axis('off')
	#Random zoom to graph 
	rndZoomX = random.randint(1,10)
	print("zoomX: ", rndZoomX)
	rndZoomY = random.randint(1,15)
	print("zoomY: ", rndZoomY)
	# Liit axis to get zoom
	plt.xlim(x_min/rndZoomX, x_max/rndZoomX)
	plt.xlim(y_min/rndZoomY, y_max/rndZoomY)
	plt.ion()
	# Save as png - remove whitening
	plt.savefig('generated.png', bbox_inches='tight')
	# OpenCv convert to gray scale
	img = cv2.imread('generated.png', cv2.IMREAD_GRAYSCALE)
	# Get number of white pixels
	n_white_pix = np.sum(img == 255)
	print('Number of white pixels:', n_white_pix)
	# What number of white is accepted
	if n_white_pix > 140000 and n_white_pix < 2000000:
		# Show graph
		plt.show()
		mng = plt.get_current_fig_manager()
		# Maximise windows
		#mng.window.showMaximized()
		#mng.window.state("normal")
		# Pause to check picture
		print("Pausing 1 sec...")
		plt.pause(1)
		plt.close('all')