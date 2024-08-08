# -*- coding: utf-8 -*-
from pycwr.io import read_auto
import matplotlib.pyplot as plt
#from pycwr.draw.RadarPlot import Graph
from pycwr.draw.RadarPlot import GraphMap
import cartopy.crs as ccrs
import numpy as np

filename =  r'/mnt/f/Doksuri/data/RADAR_S/20230728/Z9595/Z_RADR_I_Z9595_20230728111139_O_DOR_SAD_CAP_FMT.bin.bz2'
PRD = read_auto(filename)
Stime=np.datetime_as_string(PRD.scan_info.start_time.values,unit='m',timezone='UTC')

fig, ax = plt.subplots()
#graph = Graph(PRD)
#graph.plot_vcs(ax, (80.4,115.3), (27.1,2.0), "dBZ", cmap="pyart_NWSRef") #起点，终点 （units: km）


graph = GraphMap(PRD,ccrs.PlateCarree())
start_lonlat=(118.62,24.66)
end_lonlat=(118.89,25.45)
graph.plot_vcs_map(ax, start_lonlat, end_lonlat, "dBZ", cmap="pyart_NWSRef")
        
ax.set_ylim([0, 10])
ax.set_xlim([0, 80])
ax.set_ylabel("Height (km)", fontsize=14)
ax.set_xlabel("Distance From Section Start (Uints:km)", fontsize=14)
ax.set_title("VCS Plot", fontsize=16)
ax.set_title("%s VCS Plot CRef \n%s"%(PRD.sitename,Stime), fontsize=16)

plt.tight_layout()
#plt.show()
plt.savefig("/mnt/e/Doksuri/fig/Radar_CREF_onestation/%s_CRef_%s.png"%(PRD.sitename,Stime))