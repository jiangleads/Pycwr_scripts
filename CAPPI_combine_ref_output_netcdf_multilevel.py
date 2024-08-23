# -*- coding: utf-8 -*-
#conda create --name cwr python=3.10.14 numpy=1.26.4 matplotlib=3.6.3 cartopy=0.23.0 pyqt=5.15.9 -c conda-forge
#python3 /mnt/e/Doksuri/scripts/Radar/pycwr/CAPPI_overlay_terrain_combine.py /mnt/f/Doksuri/data/RADAR_S 20230728120000 /mnt/e/Doksuri/fig/Radar_CAPPI_combine dBZ 1500

from pycwr.io import read_auto
import matplotlib.pyplot as plt
from pycwr.draw.RadarPlot import plot_lonlat_map
import cartopy.crs as ccrs
import numpy as np
import argparse
from fnmatch import fnmatch
import os
from datetime import datetime, timedelta
import xarray as xr

ap = argparse.ArgumentParser()
ap.add_argument('input_radar_path', help='path and name of input radar_file path')
ap.add_argument('input_time', help='time to draw radar: YYYYMMDDHHMMSS')
ap.add_argument('save_path', help='path of output file')
ap.add_argument('variable', help='variable name')
# ap.add_argument('height', help='interp_height')
args = ap.parse_args()

fPath = args.input_radar_path
fTime= args.input_time
outPath = args.save_path
Vname = args.variable #"dBZ"
# height = int(args.height) #"dBZ"

# fPath = "/mnt/f/Doksuri/data/RADAR_S/20230728/Z9592/"
# fName = "Z_RADR_I_Z9592_20230728123734_O_DOR_SAD_CAP_FMT.bin.bz2"
# outPath = "/mnt/e/Doksuri/fig/Radar_CREF_onestation/CAPPI/"
# Vname = "dBZ"
# height = 1000

if fPath[-1] != '/':
    fPath += '/'
if outPath[-1] != '/':
    outPath += '/'



#find the nearest time range
dt = datetime(year=int(fTime[0:4]),month=int(fTime[4:6]),day=int(fTime[6:8]),hour=int(fTime[8:10]),minute=int(fTime[10:12]),second=int(fTime[12:14]))
timestamp0 = int(dt.timestamp())

# 30min 前
deltat= timedelta(minutes=30)
Timematch1=((dt-deltat).strftime("%Y%m%d%H"))+"????"
# print(Timematch1)

# 10分钟内
Timematch2=fTime[0:11]+"???"
# print(Timematch2)

# 7分钟窗口
Timedelta=7*60


# get the nearest files on the radarset
# pattern = "Z_RADR_I_Z????_??????????????_*_*_*_*.bin.bz2"
pattern0 = "Z_RADR_I_Z????_"+Timematch1+"_*_*_*_*.bin.bz2"
pattern1 = "Z_RADR_I_Z????_"+Timematch2+"_*_*_*_*.bin.bz2"
selected_files = {}
selected_files_time = {}
for root, dirs, files in os.walk(fPath, topdown=False):    
   for name in files:
       if fnmatch(name, pattern0) or fnmatch(name, pattern1):
           staid=name[9:14]           

           #    calculate the difference time offset
           indexoffset=int(15)
        #    print(name[int(4+indexoffset):int(6+indexoffset)])
           dt1 = datetime(year=int(name[int(0+indexoffset):int(4+indexoffset)]), \
                         month=int(name[int(4+indexoffset):int(6+indexoffset)]), \
                         day=int(name[int(6+indexoffset):int(8+indexoffset)]), \
                         hour=int(name[int(8+indexoffset):int(10+indexoffset)]), \
                         minute=int(name[int(10+indexoffset):int(12+indexoffset)]), \
                         second=int(name[int(12+indexoffset):int(14+indexoffset)]) )
           timestamp1 = int(dt1.timestamp())
           stampdelta = abs(timestamp1-timestamp0)
           if stampdelta <=  Timedelta:
               # with in time windows
               if staid in selected_files:
                   # has already existed before
                   if stampdelta <= selected_files_time[staid]:
                       # find the the closet time
                       selected_files[staid]=os.path.join(root, name)
                       selected_files_time[staid] = stampdelta
               else:
                   selected_files[staid]=os.path.join(root, name)
                   selected_files_time[staid] = stampdelta

# for key,value in selected_files.items():
#     print(key,value)
# for key,value in selected_files_time.items():
#     print(key,value)




selectedLonMin_large =  116
selectedLonMax_large =  121
selectedLatMin_large =  22
selectedLatMax_large =  27

resolutionxy = 0.01
#height=500

extent_large = [ selectedLonMin_large, selectedLonMax_large, selectedLatMin_large, selectedLatMax_large, ]
lon1d_large = np.arange(selectedLonMin_large, selectedLonMax_large+resolutionxy, resolutionxy) ##lon方向0.01等间距，117-120范围
lat1d_large = np.arange(selectedLatMin_large, selectedLatMax_large+resolutionxy, resolutionxy) ##lat方向0.01等间距， 31-34度范围
grid_lon_large, grid_lat_large = np.meshgrid(lon1d_large, lat1d_large, indexing="ij")




lev=[1700,2000,2500,3000,3500,4000,4500,5000]



merged = np.empty((1,len(lev),grid_lon_large.shape[1],grid_lon_large.shape[0]))
merged[:]=np.NaN
# print("valid value merged",np.count_nonzero(~np.isnan(merged)))

for iheight,height in enumerate(lev):
    for stationid,filename in selected_files.items():    
        PRD = read_auto(filename)
        staname=PRD.sitename
    
        '''# resxy = 0.75    
        # # 小数点后1位，精度对齐
        # selectedLonMin =  round(float(PRD.scan_info.longitude),2) - resxy
        # selectedLonMax =  round(float(PRD.scan_info.longitude),2) + resxy
        # selectedLatMin =  round(float(PRD.scan_info.latitude) ,2) - resxy
        # selectedLatMax =  round(float(PRD.scan_info.latitude) ,2) + resxy
        # lon1d = np.arange(selectedLonMin, selectedLonMax+resolutionxy, resolutionxy) ##lon方向0.01等间距，117-120范围
        # lat1d = np.arange(selectedLatMin, selectedLatMax+resolutionxy, resolutionxy) ##lat方向0.01等间距， 31-34度范围    
        # PRD.add_product_CAPPI_lonlat(XLon=lon1d, YLat=lat1d, level_height=height) ##插值1500m高度的
        '''
    
        PRD.add_product_CAPPI_lonlat(XLon=lon1d_large, YLat=lat1d_large, level_height=height) ##插值1500m高度的
        
        # Stime=np.datetime_as_string(PRD.scan_info.start_time.values,unit='m',timezone='UTC')
        
     
       
        functionname="CAPPI_geo_"+str(height)
        func_tmp=getattr(PRD.product,functionname)
        
        # print(merged[0,iheight,:,:].shape)
        # print((func_tmp.values).shape)
        # print(np.swapaxes(func_tmp.values,0,1).shape)
        

        #merged[:,:,iheight]= np.ma.where(np.isnan(merged[:,:,iheight]) , func_tmp.values, merged[:,:,iheight])
        
        merged[0,iheight,:,:]= np.ma.where(np.isnan(merged[0,iheight,:,:]) , np.swapaxes(func_tmp.values,0,1), merged[0,iheight,:,:])
        
        # print("after merged, number of valid values:", np.count_nonzero(~np.isnan(merged)),)    
        
#print(merged)#
varattrs={'long_name': 'quantitative_precipitation_estimation', 'short_name':Vname ,"time":fTime}


encoding = {'lat': {'zlib': False, '_FillValue': False},
            'lon': {'zlib': False, '_FillValue': False},
            'height': {'zlib': False, '_FillValue': False},
            Vname: {'_FillValue': -9.99e8,
                  'complevel': 1,
                  'chunksizes':(1,1,grid_lon_large.shape[1],grid_lon_large.shape[0]),
                  'complevel': 1,
                  'zlib': True}
            }

timestamp=[timestamp0]
df = xr.DataArray(merged,coords=[('time',timestamp),('height',lev),('lat',lat1d_large),('lon',lon1d_large)],attrs=varattrs,name=Vname)
df.time.attrs['units']="seconds since 1970-01-01T00:00:00Z"
df.height.attrs['units']="m"
df.lat.attrs['units']="degrees_north"
df.lon.attrs['units']="degrees_east"

outName="CAPPI_combine_addline_%s_%s.nc"%(fTime,Vname)
df.to_netcdf(outName, encoding=encoding)
#plt.savefig(outPath+outName)