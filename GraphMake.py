# Program to generate graphs based on data outputed from gAperture
import math
import os
from gPhoton.gAperture import gaperture as gAperture
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord
from gPhoton.gphoton_utils import read_lc
from datetime import datetime
import plotly.plotly as py
import plotly.tools as tls
from plotly import tools
import numpy as np
from scipy.signal import lombscargle
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

starttime = datetime.now()
#py.sign_in('tboudreaux', 'Nhv#r&HBlVlb6K9UR#0ihHxX0OK7!2')
### FLAGS ###
ONE = 'Hotspot'
TWO = 'Mask Edge'
FOUR = 'Exptime'
EIGHT = 'Respose'
SIXTEEN = 'Nonlinearity'
THIRTYTWO = 'Detector Edge'
SIXTYFOUR = 'bg Hotspot'
ONETWENTYEIGHT = 'bg Mask'

FLAGARRAY = [ONE, TWO, FOUR, EIGHT, SIXTEEN, THIRTYTWO, SIXTYFOUR, ONETWENTYEIGHT, 'NO FLAGS']
NUMERICFLAGARRAY = [0, 1, 2, 3, 4, 5, 6, 7, 8]

marker_style = dict(color='green', linestyle=':', marker='o',
                            markersize=5, markerfacecoloralt='gray')

NyFeq = 1
def LCFormat(TARGETNAME):
    return ['sdB_' + str(TARGETNAME) + '_lc.csv', 'GENLC_' + str(TARGETNAME) + '.csv']
start = os.path.abspath('.')

#filename = 'ST.csv'
topdir = 'Targets/ARCHIVE'
os.chdir(topdir)
search_dir = os.path.abspath('.')
#readfile = [x.rsplit() for x in open(filename, 'rb').readlines()]
#readfile.pop(0)
urlout = []
urlfile = open('plotlyurlsPulse.csv', 'w')
checkdit = os.listdir('.')
if 'tempurl.csv' in checkdit:
    pass
else:
    tempfile = open('tempurl.csv', 'w')
    tempfile.write('')
    tempfile.close()
start_loc = 0
#readfile = readfile[start_loc:]
# Target iterator loop
for index, SUBARCHIVE in enumerate(os.listdir('.')):
    os.chdir(search_dir)
    print 'PATH AT FOR START:', search_dir
    if os.path.isdir(SUBARCHIVE) is True: 
        os.chdir(SUBARCHIVE)
        working_dir = os.path.abspath('.')
    else:
        continue
    targets = os.listdir('.')
    for i, star in enumerate(targets):
        os.chdir(working_dir)
        print '#########################'
        print 'target name', star
        print 'working on target', i+start_loc, 'of', len(targets)
        try:
            numsave = 1
            print '@@@@@@@@@@@@@@@@@@@@'
            print 'ABOUT TO CHANGE INTO STAR'
            print 'PATH IS:', os.path.abspath('.')
            print 'star name is:', star 
            print '@@@@@@@@@@@@@@@@@@@@'
            os.chdir(star)
            print 'SUCSESS CHANGINED INTO STAR'
            dir = os.listdir('.')

            print 'LC LOOK FOR:', LCFormat(star)
            print 'directories', dir
            # Checks for data file
            if set(LCFormat(star)) & set(dir): # Look for the intesection of these two lists
                gAppFile = read_lc(list(set(LCFormat(star)) & set(dir))[0])
                gAppOutput = []
                fluxfile = []
                fluxerr = []
                flags = []
                exptime = []
                detRAD = []
                counts = []
                gapnum = 0
                prevloc = 0
                greatestdiffernce = 0
                AllTrace = go.Scatter(
                        x = gAppFile['t_mean'],
                        y = gAppFile['flux_bgsub'],
                        mode ='markers'
                        )
                afig = go.Figure(data=[AllTrace])
                url = plot(afig, filename = star + '_ZONE_all', auto_open = False)
                urlout.append(star + '_ZONE_all' + '\t' + url + '\n')
                tempfile = open('../../../../tempurl.csv', 'a')
                print 'HERER WE ARE', tempfile
                tempfile.write(star + '_ZONE_all' + '\t' + url + '\n')
                tempfile.close()


                # Greates multiple data sets form single monolithic data set "zoomed" into data so that there is not massive
                #   Time deltas between data making it impossible to read
                for k in range(len(gAppFile['t_mean'])):
                    if k + 1 < len(gAppFile['t_mean']):
                        if gAppFile['t_mean'][k + 1] - gAppFile['t_mean'][k] > 500:
                            differnce = gAppFile['t_mean'][k + 1] - gAppFile['t_mean'][k]
                            if differnce > greatestdiffernce:
                                greatestdiffernce = differnce
                            else:
                                pass
                            gAppOutput.append(gAppFile['t_mean'][prevloc:k + 1])
                            fluxfile.append(gAppFile['flux_bgsub'][prevloc:k + 1])
                            fluxerr.append(gAppFile['flux_err'][prevloc:k + 1])
                            flags.append(gAppFile['flags'][prevloc:k + 1])
                            exptime.append(gAppFile['exptime'][prevloc:k + 1])
                            detRAD.append(gAppFile['detrad'][prevloc:k + 1])
                            counts.append(gAppFile['counts'][prevloc:k + 1])
                            prevloc = k + 1
                            gapnum += 1
                        else:
                            pass
                    else:
                        gAppOutput.append(gAppFile['t_mean'][prevloc:-1])
                        fluxfile.append(gAppFile['flux_bgsub'][prevloc:-1])
                        fluxerr.append(gAppFile['flux_err'][prevloc:-1])
                        flags.append(gAppFile['flags'][prevloc:-1])
                        exptime.append(gAppFile['exptime'][prevloc:-1])
                        detRAD.append(gAppFile['detrad'][prevloc:-1])
                        counts.append(gAppFile['counts'][prevloc:-1])
                        
                gAppOutput = [x.tolist() for x in gAppOutput]
                fluxfile = [x.tolist() for x in fluxfile]
                fluxerr = [x.tolist() for x in fluxerr]
                flags = [x.tolist() for x in flags]
                exptime = [x.tolist() for x in exptime]
                detRAD = [x.tolist() for x in detRAD]
                counts = [x.tolist() for x in counts]
                if gapnum > 0:
                    for k in range(len(gAppOutput)):
                        if star + '_ZONE_' + str(k+1) + '.html' in dir:
                            print 'Not generating zone', k, 'plot for', star
                            continue
                        goodflux = []
                        goodtime = []
                        gooderr = []
                        badflux = []
                        badtime = []
                        baderr = []
                        dataflags = []

                        # flag checks
                        for p in range(len(fluxerr[k])):
                            flag_pos = []
                            if flags[k][p] != 0.0:
                                print 'bad flag for target ' + star + ' | f: ' + str(flags[k][p])
                                flag = int(flags[k][p])
                                flag = bin(flag)[2:]
                                for numeral in range(len(flag)):
                                    if flag[numeral] == '1':
                                        flag_pos.append(len(flag)-numeral)
                                badflux.append(fluxfile[k][p])
                                badtime.append(gAppOutput[k][p])
                                baderr.append(fluxerr[k][p])
                                dataflags.append(flag_pos)
                            else:
                                print 'Good flag for target ' + star + ' | f: ' + str(flags[k][p])
                                goodflux.append(fluxfile[k][p])
                                goodtime.append(gAppOutput[k][p])
                                gooderr.append(fluxerr[k][p])
                                #dataflags.append([0])
                        print 'Begining plot creation for target ' + star + ' ZONE ' + str(k) + ' out of ' + str(len(gAppOutput))
                        useflags = [str(x) for x in dataflags]
                        writeflags = []
                        for q in dataflags:
                            tempflags = []
                            for p in q:
                                tempflags.append(FLAGARRAY[NUMERICFLAGARRAY.index(p) - 1])
                            writeflags.append(', '.join(tempflags))
                        # ALL PLOT
                        
                        # Power Spectrum
                        f = np.linspace(0.001, NyFeq, 10000)
                        xuse = np.asarray(gAppOutput[k])
                        yuse = np.asarray(fluxfile[k])
                        try:
                            pgram = lombscargle(xuse, yuse, f)
                        except ZeroDivisionError:
                            pgram = np.linspace(0, 1, 10000)
                        normval = xuse.shape[0]

                        PowerSpectrum = go.Scatter(
                                x = f, 
                                y = np.sqrt(4*(pgram/normval))
                                )

                        LCTraceGeneralBad = go.Scatter(
                                x = badtime,
                                y = badflux,
                                mode = 'markers',
                                text = writeflags,
                                marker = dict(
                                        color='rgba(255, 182, 193, 0.9)',
                                    )
                                )
                        LCTraceGeneralAll = go.Scatter(
                                x = gAppOutput[k],
                                y = fluxfile[k],
                                mode = 'lines+markers',
                                marker = dict(
                                        color = 'rgba(1, 182, 193, 0.9)',
                                    )
                                )
                        LCTraceBad = go.Scatter(
                                x = badtime,
                                y = badflux,
                                mode = 'markers',
                                text = writeflags,
                                #error_y=dict(
                                #        type='data',
                                #        array=fluxerr[k],
                                #        visible=True,
                                #    ),
                                marker = dict(
                                    color = 'rgba(255, 182, 193, .9)',
                                    ),
                                yaxis = 'y2'
                                )
                        LCTraceAll = go.Scatter(
                                x = gAppOutput[k],
                                y = fluxfile[k],
                                mode = 'lines+markers',
                                error_y=dict(
                                        type='data',
                                        array=fluxerr[k],
                                        visible=True,
                                    ),
                                marker = dict(
                                    color = 'rgba(1, 182, 193, .9)',
                                    ),
                                yaxis = 'y2'
                                )
                        DetRadTrace = go.Scatter(
                                x = gAppOutput[k],
                                y = detRAD[k],
                                mode = 'lines+markers',
                                yaxis = 'y3'
                                )
                        ExpTrace = go.Scatter(
                                x = gAppOutput[k],
                                y = exptime[k],
                                mode = 'lines+markers',
                                yaxis = 'y4'
                                )
                        CountTrace = go.Scatter(
                                x = gAppOutput[k],
                                y = counts[k],
                                mode = 'lines+markers',
                                yaxis = 'y5'
                                )
                        data = [LCTraceAll, LCTraceGeneralAll, LCTraceGeneralBad, LCTraceBad, ExpTrace, DetRadTrace, CountTrace]
                        layout = go.Layout(
                                yaxis=dict(
                                    domain=[0.80, 1],
                                    title='Flux NE'
                                    ),
                                yaxis2=dict(
                                    domain=[0.60, 0.80],
                                    title='Flux'
                                    ),
                                yaxis3=dict(
                                    domain=[0.40, 0.60],
                                    title='Det Rad'
                                    ),
                                yaxis4 = dict(
                                    domain=[0.20, 0.40],
                                    title='EXP Time'
                                    ),
                                yaxis5 = dict(
                                    domain=[0, 0.20],
                                    title = 'Counts'
                                    ),
                                title = 'Zone: ' + str(k+1) + ' total exposure time: ' + str(len(gAppOutput[k])* 30) + ' 30s',
                                showlegend=False
                                )
                        pslayout = go.Layout(
                                title = 'Zone: ' + str(k+1) + '_POWERSPEC' + 'total exposure time: ' + str(len(gAppOutput[k])*30) + ' 30s',
                                showlegend=False
                                )
                        pfig = go.Figure(data=data, layout=layout)
                        ffig = go.Figure(data=[PowerSpectrum], layout=pslayout)
                        maxx = int(math.ceil(max(gAppOutput[k])))
                        minx = int(math.floor(min(gAppOutput[k])))
                        tiemdelta = maxx - minx
                        slicewidth = int(math.ceil(tiemdelta/len(gAppOutput[k])))
                        prev_datapoint = 'N/A'
                        inc = 0
                        inc_width = 0
                        recording = False
                        numsave += 1
                        #url = py.plot(pfig, filename = star + '_ZONE_' + str(k+1), auto_open = False)
                        url = plot(pfig, filename = star + '_ZONE_' + str(k+1) + '.html', auto_open = False)
                        tempfile = open('../../../../tempurl.csv', 'a')
                        tempfile.write(star + '_ZONE_' + str(k+1) + '\t' + url + '\n')
                        tempfile.close()
                        urlout.append(star + '_ZONE_' + str(k+1) + '\t' + url + '\n')
                        #url = py.plot(ffig, filename = star + '_ZONE_' + str(k+1) + '_POWERSPEC', auto_open = False)
                        url = plot(ffig, filename = star + '_ZONE_' + str(k+1) + '_POWERSPEC.html', auto_open = False)
                        urlout.append(star + '_ZONE_' + str(k+1) + '_POWERSPEC' + '\t' + url + '\n')
                        currentdir = os.path.abspath('.')
                        print start
                        os.chdir(start)
                        tempfile = open('tempurl.csv', 'a')
                        tempfile.write(star + '_ZONE_' + str(k+1) + '_POWERSPEC' + '\t' + url + '\n')
                        tempfile.close()
                        try:
                            logfile = open('HTMLOUT.log', 'a')
                        except IOError:
                            logfile = open('HTMLOUT.log', 'w')
                        logfile.write(star + '\t' + str(k+1) + '\n')
                        logfile.close()
                        os.chdir(currentdir)
                        plt.plot(gAppFile['t_mean'], gAppFile['flux_bgsub'])
                        plt.errorbar(gAppFile['t_mean'], gAppFile['flux_bgsub'], yerr=gAppFile['flux_err'])
                        plt.title(star + 'all')
                        plt.savefig(star + '_all.pdf', dpi=250)
                        plt.close()
                else:

                    print 'Outputing single zone plot for target ', star
                    plt.figure(1)
                    fig, axt = plt.subplots() 
                    ax1 = plt.subplot(311)
                    plt.title('Zone # 1 Estimated integration time: ' + str(len(fluxfile)*10) + '(s)')
                    #plt.errorbar(gAppFile['t_mean'], gAppFile['flux_bgsub'], yerr=gAppFile['flux_err'], fmt='o')
                    plt.plot(gAppFile['t_mean'], gAppFile['flux_bgsub'], 'ko-')
                    plt.xlabel('Time(s)')
                    plt.ylabel('bgflux')
                    ax2 = plt.subplot(312, sharex = ax1)
                    plt.plot(gAppFile['t_mean'], gAppFile['exptime'], 'o-')
                    plt.xlabel('Time(s)')
                    plt.ylabel('EXP (s)')
                    ax3 = plt.subplot(313, sharex = ax1)
                    plt.plot(gAppFile['t_mean'], gAppFile['detrad'], 'o-')
                    plt.xlabel('Time(s)')
                    plt.ylabel('RAD (units)')
                    plt.savefig(star + 'ZONE_1.png', dpi=250)
                    plt.close()
                    print 'plot creation complete'
                    #axt.errorbar(gAppFile['t_mean'], gAppFile['flux_bgsub'], yerr=gAppFile['flux_err'], fmt='o')
                    axt.plot(gAppFile['t_mean'], gAppFile['flux_bgsub'], 'ko-')
                    axt.set_xlabel('Time(s)')
                    axt.set_ylabel('bgflux')
                    url = py.plot_mpl(fig, filename = star + '_ZONE_1', auto_open=False)
                    urlout.append(star + '_ZONE_1' + '\t' + url + '\n')
            else:
                print 'SKIPPING NO CSV DATA FILE FOR TAGRET ' + star
            print 'Moving to next target'
            os.chdir('../../../..')
        except OSError:
            print 'NO FILE LOCATED'
    os.chdir(search_dir)
for i in urlout:
    urlfile.write(i)
urlfile.close()
