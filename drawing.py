from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import matplotlib.pyplot as plt
from matplotlib import pyplot, transforms
import time
import random
import numpy as np
import cv2

base = pyplot.gca().transData
cities = ["Vukovar", "Grad Ogulin","Grad Delnice","Knin", "Grad Sisak" ,"Grad Zaprešić", "Berlin","New York", "London","Petrinja", "Zagreb", "Karlovac", "Split", "Varaždin", "Čakovec", "Koprivnica", "Lipine", "Garešnica"]

while 1:
	numCity = [] 
	for CityX in range(random.randint(2,len(cities))):
		numCity.append(cities[CityX])
	rndRotation = random.randint(0,360)
	rndTimes = 1#random.randint(1,3)
	rndNear = random.randint(1,1000)
	rndRivers = random.randint(1,500)
	print("Rotation: ", rndRotation)
	print("MaxTimes", rndTimes)
	for i in range(rndTimes):
		print("Times: ",i)
		for city in numCity:
			print(city)
			try:
				vienna = Nominatim().query(city)
				query = overpassQueryBuilder(area=vienna.areaId(), elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
				result = Overpass().query(query)
				#print(result.elements()[4].geometry())
			    # spremiti na sliku - preklopiti više slika 
				for waters in result.elements():
					if random.randint(0,100) > 1:
						continue
					try:
						datastring = waters.geometry()
						x = [xx[0] for xx in datastring.coordinates[0]]
						y = [xx[1] for xx in datastring.coordinates[0]]
						xc = sum(x)/len(x)+random.random()/rndNear
						yc = sum(y)/len(y)+random.random()/rndNear
						x = [xx-xc for xx in x]
						y = [yy-yc for yy in y]
						rot = transforms.Affine2D().rotate_deg(random.randint(0,rndRotation))
						if (len(x) < rndRivers and len(y) < rndRivers):
							#fig = plt.figure()
							plt.plot(x, y,linewidth=random.randint(1,7), transform = rot + base)
							#fig.set_axis_bgcolor("lightslategray")
					except:
						pass
			except ZeroDivisionError:
				pass
	axes = plt.gca()
	x_min, x_max = axes.get_xlim()
	y_min, y_max = axes.get_ylim()

	print("Xmax: ",x_min, x_max)
	print("Ymax: ",y_min, y_max)
	plt.axis('off')
	rndZoomX = random.randint(1,5)
	rndZoomY = random.randint(1,5)
	print("zoomX: ", rndZoomX)
	print("zoomY: ", rndZoomY)
	plt.xlim(x_min/rndZoomX, x_max/rndZoomX)
	plt.xlim(y_min/rndZoomY, y_max/rndZoomY)
	plt.ion()
	#plt.savefig("test.svg")
	plt.savefig('generated.png', bbox_inches='tight')
	img = cv2.imread('generated.png', cv2.IMREAD_GRAYSCALE)
	n_white_pix = np.sum(img == 255)
	print('Number of white pixels:', n_white_pix)
	if n_white_pix > 100000 and n_white_pix < 300000:
		plt.show()
		mng = plt.get_current_fig_manager()
		#mng.window.showMaximized()
		mng.window.state("normal")
		print("Pausing 10 sec...")	
		plt.pause(10)
		plt.close('all')