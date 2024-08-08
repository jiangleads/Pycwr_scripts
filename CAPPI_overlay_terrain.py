# -*- coding: utf-8 -*-
#conda create --name cwr python=3.10.14 numpy=1.26.4 matplotlib=3.6.3 cartopy=0.23.0 pyqt=5.15.9 -c conda-forge


from pycwr.io import read_auto
import matplotlib.pyplot as plt
from pycwr.draw.RadarPlot import plot_lonlat_map
import cartopy.crs as ccrs
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('input_path', help='path and name of input file path')
ap.add_argument('input_file', help='path and name of input file name')
ap.add_argument('save_path', help='path of output file')
ap.add_argument('variable', help='variable name')
ap.add_argument('height', help='interp_height')
args = ap.parse_args()

fPath = args.input_path
fName = args.input_file
outPath = args.save_path
Vname = args.variable #"dBZ"
height = int(args.height) #"dBZ"

dataTime=fName.split('_')[4]



if fPath[-1] != '/':
    fPath += '/'
if outPath[-1] != '/':
    outPath += '/'


filename = fPath+fName
PRD = read_auto(filename)
staname=PRD.sitename

resxy = 1.0

selectedLonMin =  float(PRD.scan_info.longitude) - resxy
selectedLonMax =  float(PRD.scan_info.longitude) + resxy
selectedLatMin =  float(PRD.scan_info.latitude)  - resxy
selectedLatMax =  float(PRD.scan_info.latitude)  + resxy
resolutionxy = 0.01
#height=500

extent = [ selectedLonMin, selectedLonMax, selectedLatMin, selectedLatMax, ]

# visualization
proj = ccrs.PlateCarree()


lon1d = np.arange(selectedLonMin, selectedLonMax+resolutionxy, resolutionxy) ##lon方向0.01等间距，117-120范围
lat1d = np.arange(selectedLatMin, selectedLatMax+resolutionxy, resolutionxy) ##lat方向0.01等间距， 31-34度范围
PRD.add_product_CAPPI_lonlat(XLon=lon1d, YLat=lat1d, level_height=height) ##插值1500m高度的

Stime=np.datetime_as_string(PRD.scan_info.start_time.values,unit='m',timezone='UTC')

# XLon:np.ndarray, 1d, units:degrees
# YLat:np.ndarray, 1d, units:degrees
# level_height:常量，要计算的高度 units:meters
grid_lon, grid_lat = np.meshgrid(lon1d, lat1d, indexing="ij")

ax = plt.axes(projection=proj)
functionname="CAPPI_geo_"+str(height)
func=getattr(PRD.product,functionname)
print(func)
plot_lonlat_map(ax, grid_lon, grid_lat, func, transform=proj)
ax.set_extent([selectedLonMin, selectedLonMax, selectedLatMin, selectedLatMax], crs =proj) #设置范围
ax.set_title("%s CRef CAPPI altitu %.0f m \n%s"%(PRD.sitename,height,Stime), fontsize=12)

plt.tight_layout()
plt.show()
