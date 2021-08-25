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

# Selecting few cities we want to get data from
city = "Berlin" # Zagreb has 146 water objects - on error select smaller City
# Use area of the city
areaUsed = Nominatim().query(city)
# Check more natural: https://wiki.openstreetmap.org/wiki/Key:natural
# Create Query openstreetmap for all water surfaces in given area
#query = overpassQueryBuilder(area=areaUsed.areaId(), elementType=['way', 'relation'], selector='"natural"="scrub"', includeGeometry=True)
try:
	query = overpassQueryBuilder(area=areaUsed.areaId(), elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
except:
	print("Query builder failed!")
# Get results
try:
	result = Overpass().query(query)
except:
	print("Query failed!")
	pass
# Create object counter
objectCounter = 0
# For all found objects
for waters in result.elements():
	# Add water poligon to datastring
	datastring = waters.geometry()
	objectCounter+=1
print("Found " + str(objectCounter) + " objects")