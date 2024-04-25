# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:42:13 2024

@author: Sinurat
"""

from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt

def algoTVAP(dataB07, dataB13, dataB15, thres):
	res = np.zeros((len(dataB07), len(dataB07[0])), dtype=np.int)
	print (len(dataB07))
	print (len(dataB07[0]))
	for i in range(len(dataB07)):
		for j in range(len(dataB07[0])):
			tes = 60 + (150 * (dataB15[i,j] - dataB13[i,j]) + (4.5 * (dataB07[i,j] - dataB13[i,j])))
			if (tes > thres):
				res[i,j] = 1
	return res

def split1(dataB13, dataB15):
	res = np.zeros((len(dataB13), len(dataB13[0])), dtype=np.int)
	for i in range(len(dataB13)):
		for j in range(len(dataB13[0])):
			if (dataB13[i,j] < 233):
				if (dataB13[i,j] - dataB15[i,j] < -2):
					res[i,j] = 1
				else:
					res[i,j] = 0
			else:
				if (dataB13[i,j] - dataB15[i,j] < 0):
					res[i,j] = 1
				else:
					res[i,j] = 0
	return res

def split2(dataB07, dataB13):
	res = np.zeros((len(dataB13), len(dataB13[0])), dtype=np.int)
	for i in range(len(dataB07)):
		for j in range(len(dataB07[0])):
			if (dataB07[i,j] - dataB13[i,j] > 0):
				res[i,j] = 1
			else:
				res[i,j] = 0
	return res
thresTVAP = 100

rawB07 = 'eH08_B07_Indonesia_201805110300.nc'
rawB13 = 'eH08_B13_Indonesia_201805110300.nc'
rawB15 = 'eH08_B15_Indonesia_201805110300.nc'
dsetB07 = Dataset(rawB07, mode = 'r')
dsetB13 = Dataset(rawB13, mode = 'r')
dsetB15 = Dataset(rawB15, mode = 'r')

lat = dsetB07.variables['latitude']	#grid 0,0 is bottom left and max,max is upper right
lon = dsetB07.variables['longitude']
plotvarB07 = dsetB07.variables['I4'][0]
plotvarB13 = dsetB13.variables['IR'][0]
plotvarB15 = dsetB15.variables['I2'][0]
plt.title('Volcanic Ash ALL')
print (np.shape(plotvarB07))

################
tvapres = algoTVAP(plotvarB07, plotvarB13, plotvarB15, thresTVAP)
split1res = split1(plotvarB13, plotvarB15)
split2res = split2(plotvarB07, plotvarB13)

finres = tvapres + split1res + split2res
plotfinres = np.zeros((len(plotvarB07), len(plotvarB07[0])), dtype=np.int)
for i in range (len(plotvarB07)):
	for j in range(len(plotvarB07[0])):
		if (finres[i,j] == 3):
			plotfinres[i,j] = 1
lev = [.99,2]
colva = ['red']
m = Basemap(resolution='i',llcrnrlon=lon[0], llcrnrlat=lat[0], urcrnrlon=lon[-1],urcrnrlat=lat[-1])
x,y = np.meshgrid(np.linspace(lon[0],lon[-1],len(plotvarB07[0,:])), np.linspace(lat[0],lat[-1],len(plotvarB07)))
pltva = m.contourf(x,y,plotfinres,levels=lev,colors=colva,labels='Volcanic Ash')
m.drawcoastlines(linewidth=0.75, color = 'blue')
m.drawcountries(linewidth=0.75, color = 'blue')
plt.show()
