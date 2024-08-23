#!/usr/bin/bash

#YMDHM0="20230728120000"
#YMDHM1="20230728143000"
YMDHM0="20230728121500"
YMDHM1="20230729050000"

#startimestamp=`date "+%Y%m%d%H%M%S" -d "${YMDHM:0:8} ${YMDHM:8:2}:${YMDHM:10:2}:${YMDHM:12:2}" `
startimestamp0=`date "+%s" -d "${YMDHM0:0:8} ${YMDHM0:8:2}:${YMDHM0:10:2}:${YMDHM0:12:2}" `
startimestamp1=`date "+%s" -d "${YMDHM1:0:8} ${YMDHM1:8:2}:${YMDHM1:10:2}:${YMDHM1:12:2}" `


echo $startimestamp1 
echo $startimestamp0 

#time1='2023-07-29 05:00:00'
#endsec=`date -d $time0 "+%Y%m%d%H%M%S"`
for((i=$startimestamp0;i<=$startimestamp1;i+=1200))
do
	currenttime=`date -d "@$i" "+%Y%m%d%H%M%S"`
	echo "current time:" $currenttime
    python3 /mnt/e/Doksuri/scripts/Radar/pycwr/auto_combine_ref_output_netcdf_multilevel.py /mnt/f/Doksuri/data/RADAR_S $currenttime /mnt/e/Doksuri/fig/Radar_CAPPI_combine dBZ
done

