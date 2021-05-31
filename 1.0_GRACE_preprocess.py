# Make the original GRACE TWS (liquid water equivalent thickness):
# from 1*1 degree to 0.1*0.1 degree (consistent with the spatial resolution of Noah-MP-PHS modeling)
# from the unit m to cm
# with China's forestland mask
import os
import os.path
import math
import time
import subprocess
import numpy as np
import netCDF4 as nc

INDIR       = '/scratch/06956/mguo/GRACE/GRACE_JPL'
OUTDIR		= '/scratch/06956/mguo/GRACE/GRACE_CN'
TEMPLATE    = './GRACE_CN_TEM.cdl'
MASKFILE    = '/work2/06956/mguo/script/mask/MASK_FOREST.nc'
COORDS_FILE = '/work/06956/mguo/lonestar/PHS_CN/run_set/1.0_spin_up/0.2_hrldas_setup_file_PHS_CN.nc'

VARS 		= ['lon', 'lat', 'time', 'lwe_thickness', 'time_bounds']
filelist = os.listdir(INDIR)

mask = nc.Dataset(MASKFILE).variables['MASK_FOREST'][:]
XLONG = nc.Dataset(COORDS_FILE).variables['XLONG'][:]
XLAT = nc.Dataset(COORDS_FILE).variables['XLAT'][:]

for i in range(0, len(filelist)):
    FILE_NAME = os.path.join(INDIR, filelist[i])
    if os.path.isfile(FILE_NAME):
        outputfile = os.path.join(OUTDIR, filelist[i])
        if os.path.exists(outputfile) == False:
            subprocess.run(['ncgen', '-3', '-o', outputfile, TEMPLATE])
            dataset = nc.Dataset(FILE_NAME)
            time = dataset.variables['time'][:]
            time_bounds = dataset.variables['time_bounds'][:]
            lwe = dataset.variables['lwe_thickness'][0, :] * 100 # m to cm
            lwe_thickness = np.ma.zeros([400, 700])
            for i in range(0, 400):
                for j in range(0, 700):
                    lat = int(XLAT[i, j]) + 0.5
                    lon = int(XLONG[i, j]) + 0.5
                    lwe_thickness[i,j] = lwe[int(lat + 89.5), int(lon - 0.5)]
            lwe_thickness.mask = mask
            with nc.Dataset(outputfile, 'a') as ncf:
                ncf.variables['time'][:] = time
                ncf.variables['time_bounds'][:] = time_bounds
                ncf.variables['lon'][:] = XLONG
                ncf.variables['lat'][:] = XLAT
                ncf.variables['lwe_thickness'][0, :] = lwe_thickness
                
		
			



			



	




			



			



	



