import os
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from matplotlib.colors import LogNorm
from pylab import *
import wcsaxes
from datetime import datetime
startloc = os.path.abspath('.')
check_log = os.listdir('.')
logname = 'PNGMake.log'
if logname not in check_log:
    logfile = open(logname, 'w')
    logfile.write('RUN AT ' + str(datetime.now()) + '\n')
    logfile.close()
else:
    logfile = open(logname, 'a')
    logfile.write('RUN AT ' + str(datetime.now()) + '\n')
    logfile.close()
os.chdir('Targets/ARCHIVE/')
search_dir = os.path.abspath('.')
SUBARCHIVES = os.listdir('.')
failid = 0
for ARCHIVE in SUBARCHIVES:
    os.chdir(search_dir)
    if os.path.isdir(ARCHIVE):
        os.chdir(ARCHIVE)
        working_dir = os.path.abspath('.')
    else:
        continue
    dirs = os.listdir('.')
    xloc = 0
    for x in dirs:
        if x[0] == '.':
            dirs.pop(xloc)
        else:
            pass
        xloc += 1
    c1 = '#66ff66'
    c2 = '#ff0000'
    # if you want to start at a spesific target
    #~ start_loc = dirs.index('feige_110')
    #~ dirs = dirs[start_loc-1:]
    for dex, i in enumerate(dirs):
        find = False
        print 'target: ', i, '(number', dex+1, 'out of', len(dirs), ')in archive', ARCHIVE
        #~ print 'progress: ', dex+start_loc, ' out of ', len(dirs) + start_loc 
        os.chdir(i)
        files = os.listdir('.')
        if i + 'Count.png' in files:
            os.chdir('..')
            continue
        for z in files:
            if '_count_coadd.fits' in z:
                image_file = z
                find = True
                break
            else:
                pass
        if find is False:
            os.chdir('..')
            continue
        hdu_list = fits.open(image_file)
        hdu = fits.open(image_file)[0]
        wcs = WCS(hdu.header)
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection = wcs)
        try:
            try:
                regionfile = open('region_' + i.lower() + '.reg', 'rb')
            except IOError:
                regionfile = open('region_' + i.upper() + '.reg', 'rb')
        except IOError as e:
            print 'NON FATAL ERROR, HARD FAILURE FOR TARGET', i
            print 'RECOVERING AND MOVING TO NEXT TARGET'
            tempdir = os.path.abspath('.')
            os.chdir(startloc)
            logfile = open(logname, 'a')
            logfile.write('################\n')
            logfile.write('\tHARD FAIL FOR TARGET' + str(i) + '\n')
            logfile.write('\tSUBARCHIVE' + ARCHIVE + '\n')
            logfile.write('\tFailID = ' + str(failid) + '\n')
            logfile.write('\tReturned Error:' + str(e) + '\n')
            logfile.write('################\n')
            logfile.close()
            failid += 1
            os.chdir(tempdir)
            os.chdir('..')
            continue
        regionread = regionfile.readlines()
        regionread = [x.rstrip() for x in regionread]
        size_info = regionread[4:7]
        size_info = [x.replace('circle(', '') for x in size_info]
        size_info = [x.replace(') # width=2', '') for x in size_info]
        size_info = [x.replace(') # color=red width=2', '') for x in size_info]
        size_info = [x.split(',') for x in size_info]
        inc = 0
        region_file = [0]*len(size_info)
        for uvb in size_info:
            region_file[inc] = float(uvb[-1][0:-1])
            inc += 1
        loc_info = [float(size_info[0][0]), float(size_info[0][1])]
        opts = dict(fc='none', ec=c1, lw=2)
        opts2 = dict(fc='none', ec=c2, lw=2)
        opts3 = dict(fc='none', ec=c2, lw=4)
        image_data=hdu_list[0].data
        center_y = image_data.shape[0] / 2.0
        center_x = image_data.shape[1] / 2.0
        tmp = ax.imshow(image_data, cmap='gray', norm=LogNorm())
        ax.set_title('gMap Image of ' + i)
        Aperture = Circle((center_x, center_y), region_file[0], **opts)
        ax.add_patch(Aperture)
        InnerAn = Circle((center_x, center_y), region_file[1], **opts2)
        ax.add_patch(InnerAn)
        OuterAn = Circle((center_x, center_y), region_file[2], **opts3)
        ax.add_patch(OuterAn)
        fig.colorbar(tmp)
        plt.savefig(i + 'Count.png', dpi=250)
        plt.close()
        os.chdir('..')
