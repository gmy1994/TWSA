# Calculate the simulated monthly TWSA over 2004-2010 by Noah-MP-PHS
# TWSA = soil water anomaly + snow water equivalent anomaly + plant water anomaly + canopy water (interception) anomaly + water in aquifer anomaly
import os
import os.path
import subprocess
import numpy as np
import netCDF4 as nc

TEMPLATE    =  './SIM_TWSA_TEM.cdl'
INDIR       =   '/scratch/06956/mguo/NoahMP_PHS/CN/experiment/TWS/TWSV/'
OUTDIR      =   '/scratch/06956/mguo/NoahMP_PHS/CN/experiment/TWS/TWSA/'

MASKFILE = '/work2/06956/mguo/script/mask/MASK_FOREST.nc'
mask = nc.Dataset(MASKFILE).variables['MASK_FOREST'][:]

XLONG = nc.Dataset('/work/06956/mguo/lonestar/PHS_CN/run_set/1.0_spin_up/0.2_hrldas_setup_file_PHS_CN.nc').variables['XLONG'][:]
XLAT = nc.Dataset('/work/06956/mguo/lonestar/PHS_CN/run_set/1.0_spin_up/0.2_hrldas_setup_file_PHS_CN.nc').variables['XLAT'][:]

# phsnm =["Noah","CLM","SiB", "map","oak","plot"]
phsnm =["map","oak","plot"]
soilm = [2, 10]
month = ['01','02','03','04','05','06','07','08','09','10','11','12']

for var in phsnm:
    for sm in range(0,len(soilm)):

        OUTPUT_CASE_DIR = OUTDIR + var + '_' + str(soilm[sm]) + 'm'
        if os.path.exists(OUTPUT_CASE_DIR) == False:
            os.system("mkdir " + OUTPUT_CASE_DIR)
        else:
            os.system("rm " + OUTPUT_CASE_DIR + "/*")

        INPUT_CASE_DIR = INDIR + var + '_' + str(soilm[sm]) + 'm'

        filelist = os.listdir(INPUT_CASE_DIR)
        timespan = len(filelist)
        print(timespan)

        SW_MEAN = np.ma.zeros([4,400,700])
        SWE_MEAN = np.ma.zeros([400,700])
        PW_MEAN = np.ma.zeros([400,700])
        CW_MEAN = np.ma.zeros([400,700])
        AW_MEAN = np.ma.zeros([400,700])
        TWS_MEAN = np.ma.zeros([400,700])
        
        for year in range(2004,2011):
            for m in range(0,len(month)):

                file_name = 'SIM-TWSV-' + str(year) + month[m] + '.nc'
                input_file = os.path.join(INPUT_CASE_DIR, file_name)
                dataset = nc.Dataset(input_file)
                SW = dataset.variables['SW'][:]
                SWE = dataset.variables['SWE'][:]
                PW  = dataset.variables['PW'][:]
                CW  = dataset.variables['CW'][:]
                AW  = dataset.variables['AW'][:]
                TWS  = dataset.variables['TWS_SIM'][:]
                SW_MEAN += SW
                SWE_MEAN += SWE
                PW_MEAN += PW
                CW_MEAN += CW
                AW_MEAN += AW
                TWS_MEAN += TWS
        
        SW_MEAN = SW_MEAN / timespan
        SWE_MEAN = SWE_MEAN / timespan
        PW_MEAN = PW_MEAN / timespan
        CW_MEAN = CW_MEAN / timespan
        AW_MEAN = AW_MEAN / timespan
        TWS_MEAN = TWS_MEAN / timespan

        SW_MEAN.mask = mask
        SWE_MEAN.mask = mask
        PW_MEAN.mask = mask
        CW_MEAN.mask = mask
        AW_MEAN.mask  = mask
        TWS_MEAN.mask = mask


        for year in range(2004, 2011):
            for m in range(0,len(month)):
                    
                file_name = 'SIM-TWSV-' + str(year) + month[m] + '.nc'
                input_file = os.path.join(INPUT_CASE_DIR, file_name)
                dataset = nc.Dataset(input_file)
                SW = dataset.variables['SW'][:]
                SWE = dataset.variables['SWE'][:]
                PW  = dataset.variables['PW'][:]
                CW = dataset.variables['CW'][:]
                AW  = dataset.variables['AW'][:]
                TWS  = dataset.variables['TWS_SIM'][:]

                SWA = SW - SW_MEAN
                SWEA = SWE - SWE_MEAN
                PWA = PW - PW_MEAN
                CWA = CW - CW_MEAN
                AWA = AW - AW_MEAN
                TWSA = TWS - TWS_MEAN
    
                outfile_name = 'SIM-TWSA-' + str(year) + month[m] + '.nc'
                outputfile = os.path.join(OUTPUT_CASE_DIR, outfile_name)
                subprocess.run(['ncgen', '-3', '-o', outputfile, TEMPLATE])
                with nc.Dataset(outputfile, 'a') as ncf:
                    ncf.variables['PWA'][:] = PWA[:]
                    ncf.variables['CWA'][:] = CWA[:]
                    ncf.variables['AWA'][:] = AWA[:]
                    ncf.variables['SWA'][:] = SWA[:]
                    ncf.variables['SWEA'][:] = SWEA[:]
                    ncf.variables['TWSA_SIM'][:] = TWSA[:]
                    ncf.variables['XLONG'][:] = XLONG[:]
                    ncf.variables['XLAT'][:] = XLAT[:]

        
        