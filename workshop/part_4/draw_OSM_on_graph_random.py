# OpenStreetMap art drawing project
# Project was done at Electric Wonderland camp
# Authors: Goran Mahovlić, Igor Brkić, Ana Horvat, Paula Bučar, Mark Bilandžić, Jurica Zrna, Tomislav Mikić
# How it works?
# Show random water surfaces from random cities (currently from list) on random location of the graf(picture)

# https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide
# https://github.com/mocnik-science/osm-python-tools/blob/master/docs/element.md
# https://pythonawesome.com/a-library-to-access-openstreetmap-related-services/

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import matplotlib.pyplot as plt
from matplotlib import pyplot, transforms
import time
import random

# Selecting few cities we want to get data from
city = "Sisak" # Zagreb has 146 water objects - on error select smaller City
# Use area of the city
areaUsed = Nominatim().query(city)
# Check more natural: https://wiki.openstreetmap.org/wiki/Key:natural
# Create Query openstreetmap for all water surfaces in given area

try:
	query = overpassQueryBuilder(area=areaUsed.areaId(), elementType=['way', 'relation'], selector='"natural"="scrub"', includeGeometry=True)
	#query = overpassQueryBuilder(area=areaUsed.areaId(), elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
except:
	print("Query builder failed!")
# Get results
try:
	result = Overpass().query(query)
except:
	print("Query failed!")
	pass

# For all found objects
for waters in result.elements():
	# Add water poligon to datastring
	datastring = waters.geometry()
	try:
		# Get base data
		base = pyplot.gca().transData
		# Add water poligon to map
		datastring = waters.geometry()
		x = [xx[0] for xx in datastring.coordinates[0]]
		y = [xx[1] for xx in datastring.coordinates[0]]

		# Random for displacing obects from centar -- may not work
		#rndNear = random.randint(1,1000)
		#print("Near: ", rndNear)
		# Add displacement
		#xc = sum(x)/len(x)+random.random()/rndNear
		#yc = sum(y)/len(y)+random.random()/rndNear
		# Get values back to X and Y
		#x = [xx-xc for xx in x]
		#y = [yy-yc for yy in y]

		# Generate random for line width
		random_line_width = random.randint(5,15)
		print("Line width: ", random_line_width)
		# Generate random for rotation
		random_rotation = random.randint(0,360)
		print("Rotation: ", random_rotation)
		
		rotation = transforms.Affine2D().rotate_deg(random_rotation)
		# Add geometry to graph with random line width and random rotation
		plt.plot(x, y,linewidth=random_line_width, transform = rotation + base)
		# Add geometry without rotation
		#plt.plot(x, y,linewidth=random_line_width)
		# Interactive on -- needs to be on if we want pause and close to work
		plt.ion()
		# Hide Axis
		plt.axis('off')
		# Show graph
		plt.show()
		# Pause to check picture
		print("Pausing 0.2 sec...")
		plt.pause(0.2)
		# Close current graph
		plt.close('all')
	except:
		print("Water adding failed!")
		pass