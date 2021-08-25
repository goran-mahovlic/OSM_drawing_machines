# OpenStreetMap art drawing project
# Project was done at Electric Wonderland camp
# Authors: Goran Mahovlić, Igor Brkić, Ana Horvat, Paula Bučar, Mark Bilandžić, Jurica Zrna, Tomislav Mikić
# How it works?
# Show random water surfaces from random cities (currently from list) on random location of the graf(picture)

# https://matplotlib.org/stable/tutorials/introductory/pyplot.html

import matplotlib.pyplot as plt
from matplotlib import pyplot, transforms

plt.plot([1, 2, 3, 4])

# Get min and max graph
axes = plt.gca()
x_min, x_max = axes.get_xlim()
print("Xmax: ",x_min, x_max)	
y_min, y_max = axes.get_ylim()
print("Ymax: ",y_min, y_max)
# Do not print axis
#plt.axis('off')
# Zoom to graph 
#ZoomX = 1
#ZoomY = 1
# Liit axis to get zoom
#plt.xlim(x_min/ZoomX, x_max/ZoomX)
#plt.xlim(y_min/ZoomY, y_max/ZoomY)
#Enable interactive mode.
#plt.ion()
# Show graph
plt.show()
#plt.close('all')