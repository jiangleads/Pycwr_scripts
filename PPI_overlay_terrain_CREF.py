# -*- coding: utf-8 -*-
#from pycwr.io import read_auto
#import matplotlib.pyplot as plt
#from pycwr.draw.RadarPlot import Graph
#
#filename = r"./data/Z_RADR_I_Z9898_20190828181529_O_DOR_SAD_CAP_FMT.bin.bz2"
#PRD = read_auto(filename)
#fig, ax = plt.subplots()
#graph = Graph(PRD)
#graph.plot_ppi(ax, 0, "dBZ", cmap="CN_ref") ## 0代表第一层, dBZ代表反射率产品
#graph.add_rings(ax, [0, 50, 100, 150, 200, 250, 300])
#ax.set_title("PPI Plot", fontsize=16)
#ax.set_xlabel("Distance From Radar In East (km)", fontsize=14)
#ax.set_ylabel("Distance From Radar In North (km)", fontsize=14)
#plt.show()
#
#
#conda create --name cwr python=3.10.14 numpy=1.26.4 matplotlib=3.6.3 cartopy=0.23.0 pyqt=5.15.9 -c conda-forge



from pycwr.io import read_auto
import matplotlib.pyplot as plt
from pycwr.draw.RadarPlot import GraphMap
import cartopy.crs as ccrs
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('input_path', help='path and name of input file path')
ap.add_argument('input_file', help='path and name of input file name')
ap.add_argument('save_path', help='path of output file')
ap.add_argument('variable', help='variable name')
args = ap.parse_args()

fPath = args.input_path
fName = args.input_file
outPath = args.save_path
Vname = args.variable #"dBZ"

dataTime=fName.split('_')[4]



if fPath[-1] != '/':
    fPath += '/'
if outPath[-1] != '/':
    outPath += '/'


#filename="/mnt/f/Doksuri/data/RADAR_S/20230728/Z9595/Z_RADR_I_Z9595_20230728160205_O_DOR_SAD_CAP_FMT.bin.bz2"
#E:\Doksuri\fig\Radar_CREF_onestation
filename = fPath+fName
PRD = read_auto(filename)
staname=PRD.sitename


ax = plt.axes(projection=ccrs.PlateCarree())

graph = GraphMap(PRD, ccrs.PlateCarree())

iangle = 0
fangle = PRD.scan_info.fixed_angle.loc[iangle].item()
Stime=np.datetime_as_string(PRD.scan_info.start_time.values,unit='m',timezone='UTC')


outName="%s_%s_%s_%.2f.png"%(staname,dataTime,Vname,fangle)
print(outName)

graph.plot_ppi_map(ax, iangle, Vname, cmap="CN_ref") ## 0代表第一层, dBZ代表反射率产品，cmap
#graph.plot_ppi_map(ax, iangle, "V", cmap="CN_ref") ## 0代表第一层, dBZ代表反射率产品，cmap

# https://pycwr.readthedocs.io/en/latest/select_data.html
# dBT total_power
# dBZ reflectivity
# V velocity
# W spectrum_width
# SQI normalized_coherent_power
# CPA clutter_phase_alignment
# ZDR differential_reflectivity
# LDR linear_depolarization_ratio
# CC cross_correlation_ratio
# PhiDP differential_phase
# KDP specific_differential_phase
# CP clutter_probability
# Flag flag_of_rpv_data
# HCL hydro_class
# CF clutter_flag
# Zc corrected_reflectivity
# Vc corrected_velocity
# Wc spectrum_width_corrected
# SNRH horizontal_signal_noise_ratio
# SNRV vertical_signal_noise_ratio

selectedLonMin = 116 #7
selectedLonMax = 122 #.5
selectedLatMin = 21
selectedLatMax = 27

resxy=2
selectedLonMin =  float(PRD.scan_info.longitude) - resxy
selectedLonMax =  float(PRD.scan_info.longitude) + resxy
selectedLatMin =  float(PRD.scan_info.latitude)  - resxy
selectedLatMax =  float(PRD.scan_info.latitude)  + resxy



extent = [ selectedLonMin, selectedLonMax, selectedLatMin, selectedLatMax, ]

# visualization
proj = ccrs.PlateCarree()

ax.set_extent(extent, crs=proj)
ax.set_title("%s CRef %3.1f\N{DEGREE SIGN}\n%s"%(PRD.sitename,fangle,Stime), fontsize=12)



plt.tight_layout()
#plt.show()
plt.savefig(outPath+outName)
