# Reorganize file name of the GRACE TWS in China's forests into a monthly list
import os
import os.path
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

INDIR   = '/scratch/06956/mguo/GRACE/GRACE_CN/'
OUTDIR  = '/scratch/06956/mguo/GRACE/GRACE_MONTH/'

month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

DAYS = [[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
        [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]

# Is leap year?
def LeapYear(year):
	if year % 400 == 0:
		return 1
	elif year % 4 == 0 and year % 100 != 0:
		return 1
	else:
		return 0

def WhichMonth(y, days):
    leap = LeapYear(y)
    count = 0
    for i in range(12):
        count += DAYS[leap][i]
        if count>=days:
            return month[i]

filelist = os.listdir(INDIR)
filelist = sorted(filelist)
for i in range(0, len(filelist)):
    FILE_NAME = os.path.join(INDIR, filelist[i])
    if os.path.isfile(FILE_NAME):
        outputfile = os.path.join(INDIR, filelist[i])
        m = WhichMonth(int(filelist[i][6:10]), int(filelist[i][10:13]))
        print(filelist[i][6:10] + m)
        os.system("cp " + outputfile + " " + OUTDIR + "grd-" + filelist[i][6:10] + m + ".nc")