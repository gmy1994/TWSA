# Calculate the simulated monthly TWS variations (2004-2010) by Noah-MP-PHS
# TWS = soil water + snow water equivalent + plant water + canopy water (interception) + water in aquifer
import os
import os.path
import subprocess
import numpy as np
import netCDF4 as nc

TEMPLATE    =  './SIM_TWSA_TEM.cdl'
INDIR       =  '/scratch/06956/mguo/NoahMP_PHS/CN/output/process/monthly/'
OUTDIR      =  '/scratch/06956/mguo/NoahMP_PHS/CN/experiment/TWS/TWSV/'

MASKFILE = '/work2/06956/mguo/script/mask/MASK_FOREST.nc'
mask = nc.Dataset(MASKFILE).variables['MASK_FOREST'][:]

# phsnm = ["Noah","CLM","SiB", "map","oak","plot"]
phsnm = ["map","oak","plot"]
soilm = [2, 10]

month = ['01','02','03','04','05','06','07','08','09','10','11','12']
soil_layers = [[0.1, 0.3, 0.6, 1.0], [0.1, 0.3, 0.6, 9.0]]

for var in phsnm:
    for sm in range(0,len(soilm)):

        OUTPUT_CASE_DIR = OUTDIR + var + '_' + str(soilm[sm]) + 'm'
        if os.path.exists(OUTPUT_CASE_DIR) == False:
            os.system("mkdir " + OUTPUT_CASE_DIR)
        else:
            os.system("rm " + OUTPUT_CASE_DIR + "/*")

        INPUT_CASE_DIR = INDIR + var + '_' + str(soilm[sm]) + 'm'

        for year in range(2004,2011):
            for m in range(0,len(month)):
                print("******* " +  var + "_" + str(soilm[sm]) + "m:" + " Start Computing TWS for  " + str(year) + month[m] + " *******")
                SW = np.ma.zeros([4,400,700])
                SWE = np.ma.zeros([400,700])
                CW = np.ma.zeros([400,700])
                PW = np.ma.zeros([400,700])
                AW = np.ma.zeros([400,700])
                TWS_SIM = np.ma.zeros([400,700])

                file_name = 'mon-' + str(year) + month[m] + '.nc'
                input_file = os.path.join(INPUT_CASE_DIR, file_name)
                dataset = nc.Dataset(input_file)
                SOIL_M = dataset.variables['SOIL_M'][0]
                SNEQV  = dataset.variables['SNEQV'][0]
                VWSS  = dataset.variables['VWSS'][0]
                VWSL  = dataset.variables['VWSL'][0]
                CANLIQ  = dataset.variables['CANLIQ'][0]
                CANICE  = dataset.variables['CANICE'][0]
                WA  = dataset.variables['WA'][0]
                ZWT = dataset.variables['ZWT'][0]

                # soil water storage (m to cm)
                for z in range(4):
                    VALUE = SOIL_M[:, z, :] * soil_layers[sm][z] * 100
                    VALUE.mask = mask
                    SW[z,:,:] = VALUE
                
                # snow water equivalent (kg/m2 to cm)
                SWE = SNEQV * 0.1
                SWE.mask = mask

                # plant water storage (kg/m2 to cm), the variations, not absolute value
                PW = (VWSS + VWSL) * 0.1
                PW.mask = mask

                # canopy water content (mm to cm)
                CW = (CANICE + CANLIQ) * 0.1
                CW.mask = mask

                # water in aquifer (kg/m2 to cm)
                AW = WA * 0.1
                AW.mask = mask

                TWS_SIM = SW[0,:] + SW[1,:] + SW[2,:] + SW[3,:] + SWE + PW + CW + AW

                file_name = 'SIM-TWSV-' + str(year) + month[m] + '.nc'
                outputfile = os.path.join(OUTPUT_CASE_DIR, file_name)
                if os.path.exists(outputfile) == False:
                    subprocess.run(['ncgen', '-3', '-o', outputfile, TEMPLATE])
                with nc.Dataset(outputfile, 'a') as ncf:
                    ncf.variables['SW'][:] = SW[:]
                    ncf.variables['SWE'][:] = SWE[:]
                    ncf.variables['PW'][:] = PW[:]
                    ncf.variables['CW'][:] = CW[:]
                    ncf.variables['AW'][:] = AW[:]
                    ncf.variables['TWS_SIM'][:] = TWS_SIM[:]                