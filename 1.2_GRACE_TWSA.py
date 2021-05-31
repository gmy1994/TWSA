# Calculate the GRACE TWSA over the period of 2004-2010 (consecutive years without missing monthly data) 
import os
import os.path
import subprocess
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

INDIR       = '/scratch/06956/mguo/GRACE/GRACE_MONTH/'
OUTDIR      = '/scratch/06956/mguo/GRACE/GRACE_TWSA/'
TEMPLATE    =  './GRACE_TWSA_TEM.cdl'
COORDS_FILE = '/work/06956/mguo/lonestar/PHS_CN/run_set/1.0_spin_up/0.2_hrldas_setup_file_PHS_CN.nc'

XLONG = nc.Dataset(COORDS_FILE).variables['XLONG'][:]
XLAT = nc.Dataset(COORDS_FILE).variables['XLAT'][:]

month = ['01','02','03','04','05','06','07','08','09','10','11','12']

TWS_AVG = np.ma.zeros([400,700])
for year in range(2004,2011):
    for m in range(0,len(month)):
        infile_name = 'grd-' + str(year) + month[m] + '.nc'
        inputfile = os.path.join(INDIR, infile_name)
        TWS = nc.Dataset(inputfile).variables['lwe_thickness'][0]

        TWS_AVG += TWS
TWS_AVG = TWS_AVG/((2010-2004+1) * 12)

for year in range(2004,2011):
    for m in range(0,len(month)):
        infile_name = 'grd-' + str(year) + month[m] + '.nc'
        inputfile = os.path.join(INDIR, infile_name)
        TWS = nc.Dataset(inputfile).variables['lwe_thickness'][0]
        
        TWSA = TWS - TWS_AVG

        outfile_name = 'GRACE-TWSA-' + str(year) + month[m] + '.nc'
        outputfile = os.path.join(OUTDIR, outfile_name)
        if os.path.exists(outputfile) == False:
            subprocess.run(['ncgen', '-3', '-o', outputfile, TEMPLATE])
        with nc.Dataset(outputfile, 'a') as ncf:
                ncf.variables['TWSA'][:] = TWSA[:]
                ncf.variables['XLONG'][:] = XLONG[:]
                ncf.variables['XLAT'][:] = XLAT[:]