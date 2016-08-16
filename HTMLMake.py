#!/home/tboudreaux/anaconda/bin/python
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
print 'START'
scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('../SummerSTScI-ca588a8e388a.json', scope)

gc = gspread.authorize(credentials)
checkstar = 'sdssj_141812.51-024426.9'
start = os.path.abspath('.')
urls_raw = [x.rsplit()[1] for x in open('tempurl.csv', 'rb').readlines()]
indexes_raw = [x.rsplit()[0] for x in open('tempurl.csv', 'rb').readlines()]
indexes = []
all_index = []
ulrs = []
ulrstmp = []
all_url = []
all_urltmp = []
power_url = []
power_urltmp = []
power_index = []
go = 0
for Uitem, Iitem in zip(urls_raw, indexes_raw):
    if go < 1000:
        #print Uitem, Iitem
        go += 1
    if '_all' in Iitem:
        all_index.append(Iitem[:-9])
        all_urltmp.append(Uitem)
    elif '_POWERSPEC' in Iitem:
        power_urltmp.append(Uitem)
        power_index.append(Iitem)
    else:
        indexes.append(Iitem)
        ulrstmp.append(Uitem)
for check in ulrstmp:
    if 'file:///Pool/' in check:
        ulrs.append(check[48:])
    else:
        ulrs.append(check + '.embed')
for check in power_urltmp:
    if 'file:///Pool/' in check:
        power_url.append(check[48:])
    else:
        power_url.append(check + '.embed')
for check in all_urltmp:
    if 'file:///Pool/' in check:
        all_url.append(check[48:])
    else:
        all_url.append(check + '.embed')
justchanged = True
targetzone_ind = []
targetzone_use = []
prevzonenum = 0
prev_targ = indexes[0].split('_')[0] + '_' + indexes[0].split('_')[1]
for index, target in enumerate(indexes):
    #print 'number ', index, 'of ', len(indexes)
    #print target
    if checkstar in target:
        print 'trace a'
    target_check = target.split('_')

    # The general flipper, figures out how many zones a target has more or less
    if prev_targ == target_check[0] + '_' + target_check[1]:
        if checkstar in target:
            print 'trace b'
        justchanged = False
        prev_targ = target_check[0] + '_' + target_check[1]
        zonenum = target_check[-1]
        if int(zonenum) > int(prevzonenum):
            prevzonenum = int(zonenum)

        # The deals with the final target
        if index == len(indexes) - 1:
            targetzone_ind.append(prev_targ)
            targetzone_use.append(prevzonenum) 

    #This deals with the first zone of a new target
    elif prev_targ != target_check[0] + '_' + target_check[1] and justchanged is False:
        if checkstar in target:
            print 'trace c'
        juctchanged = True
        targetzone_ind.append(prev_targ)
        targetzone_use.append(prevzonenum)
        zonenum = 0
        prevzonenum = 0
        prev_targ = target_check[0] + '_' + target_check[1]
        zonenum = target_check[-1]
        if int(zonenum) > int(prevzonenum):
            prevzonenum = int(zonenum)

    # this is incase a target only had one zone in it
    elif prev_targ != target_check[0] + '_' + target_check[1] and justchanged is True:
        if checkstar in target:
            print 'trace d'
        juctchanged = True
        targetzone_ind.append(prev_targ)
        targetzone_use.append(prevzonenum)
        zonenum = 0
        prevzonenum = 0
        prev_targ = target_check[0] + '_' + target_check[1]
        zonenum = target_check[-1]
        if zonenum > prevzonenum:
            prevzonenum = zonenum
        targetzone_ind.append(target_check[0] + '_' + target_check[1])
        targetzone_use.append(zonenum)
SOARDIR = []
NORTHDIR = []
KNOWNDIR = []
SOUTHDIR = []
os.chdir('Targets/ARCHIVE')
ARCHIVES = ['SOAR', 'KNOWN', 'NORTHERN', 'SOUTHERN']
for subdir in ARCHIVES:
    #print 'CURRENT DIRECTORY IS: ', os.path.abspath('.')
    os.chdir(start)
    os.chdir('Targets/ARCHIVE/' + subdir)
    working_dir = os.path.abspath('.')
    dir = os.listdir('.')
    if subdir == 'KNOWN':
        KNOWNDIR = dir
    elif subdir == 'SOAR':
        SOARDIR = dir
    elif subdir == 'NORTHERN':
        NORTHDIR = dir
    elif subdir == 'SOUTHERN':
        SOUTHDIR = dir
    xloc = 0
    addon = 'Targets/ARCHIVE/' + subdir
    # removes hidden files
    for x in dir:
        if x[0] == '.':
            dir.pop(xloc)
        else:
            xloc += 1
    xloc = 0
    numtarg = len(dir)
    firstlinkrec = False
    firstlink = 'http://www.google.com'
    nextlink = 'http://www.google.com'
    count = 1
    incriment = 'NAN'
    prevlink = '../../../../index.html'
    imageforpage = 'NOIMAGEFOUND'
    LINKARRAY = []
    for i in range(numtarg):
        htmlgo = False
        alright = False
        onetimefilp = False
        cont = False
        numzones = 0
        pagenum = 0
        pathtox = ['../../../../404.png'] * 1000
        #try:
        os.chdir(dir[i])
        checkzones = os.listdir('.')
        for x in checkzones:
            if x[0] == '.':
                checkzones.pop(xloc)
            else:
                xloc += 1
        xloc = 0
        raw_graphs = []
        graph_init_order = []
        power_graphs = []
        power_graph_init_order = [] 
        for x in checkzones:
            if '.html' in x and 'ZONE' in x and not '._' in x and not 'POWERSPEC' in x and not 'all' in x and not '60s' in x and not '10s' in x:
                try:
                    graph_init_order.append(int(x.split('_')[3].strip('.html')))
                except ValueError as e:
                    print 'NON FATAL ERROR, ATTEMPTING RECOVERY:', e
                    tempx = x.split('_')
                    tempindex = tempx.index('ZONE')
                    graph_init_order.append(int(tempx[tempindex+1].strip('.html')))
                    print 'ERROR RECOVERY SUCSSESSFUL, CONTINUING AS NORMAL'
                raw_graphs.append(x)
            elif '.html' in x and 'ZONE' in x and not '._' in x and 'POWERSPEC' in x and not 'all' in x and not '60s' in x and not '10s' in x:
                try:
                    power_graph_init_order.append(int(x.split('_')[3].strip('.html')))
                except ValueError as e:
                    print 'NON FATAL ERROR, ATTEMPTING RECOVERY: ', e
                    tempx = x.split('_')
                    tempindex = tempx.index('ZONE')
                    power_graph_init_order.append(int(tempx[tempindex+1].strip('.html')))
                    print 'ERROR RECOVERY SUCSSESFUL, CONTINUING AS NORMAL'
                power_graphs.append(x)
            elif '.html' in x and 'ZONE' in x and not '._' in x and not 'POWERSPEC' in x and 'all' in x:
                allplot = x
            elif '.png' in x and 'Count' in x and '._' not in x[0:3]:
                imageforpage = x
        if firstlinkrec is False:
            firstlink = addon + '/' + dir[i] + '/' + dir[i] + 'ViewPage.html'
            firstlinkrec = True
        else:
            pass
        if alright is False:
            htmlout = open(dir[i] + 'ViewPage.html', 'w')
        together = zip(graph_init_order, raw_graphs)
        sorted_together = sorted(together)
        graphs = [x[1] for x in sorted_together]
        try: 
            numzones = max(graph_init_order)
        except ValueError as e:
            print 'NON FATAL ERROR: ', e
            print 'Moving to next target with hard failure on target:', dir[i]
            os.chdir(working_dir)
            continue
        for k in range((len(dir) - i) - 1):
            precheckhtml = os.listdir(os.path.abspath('..') + '/' + dir[i + k + 1])
            for x in precheckhtml:
                if '.png' in x or 'ZONE' in x and not '._' in x:
                    htmlgo = True
                    incriment = k + 1
                    cont = True
                    break
                else:
                    pass
            if cont is True:
                break
            else:
                pass
        if htmlgo is True:
            nextlink = '../../../../' + addon + '/' + dir[i+incriment] + '/' + dir[i+incriment] + 'ViewPage.html'
        else:
            nextlink = '../../../../' + addon + '/' + dir[i] + '/' + dir[i] + 'ViewPage.html'
        pagenum += 1
        URLINDEX = 0
        #~ allplot = all_url[all_index.index(dir[i])]
        if dir[i] == checkstar:
            print htmlgo, alright
        if htmlgo is True and alright is False:
            # print 'writing out file for', dir[i], ' | target ', i, ' out of', numtarg
            htmlout.write('<!DOCTYPE html>\n'
                          '<html>\n'
                          '<head>\n'
                          '<title>Summer STScI gPhoton HTML pipleline</title>\n'
                          '</head>\n'
                          '<body>\n'
                          '<div id="header" style="position: fixed; background-color: #ffffff; left:0; right:0; top:0; padding:5px;">\n'
                          '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js">\n'
                          '</script>\n'
                          '<h1>STScI Summer internship pipeline | Target ' + dir[i] + '</h1>\n'
                          '<form action="' + nextlink + '">\n'
                          '\t<input type="submit" value="Go To Next Target">\n'
                          '</form>\n'
                          '<form action="' + prevlink + '">\n'
                          '\t<input type="submit" value="Go To Previous Target">\n'
                          '</form>\n'
                          '<form action = "../../../../../index.html">\n'
                          '\t<input type="submit" value="go to index">\n'
                          '</form>\n'
                          '<script>\n'
                          '$(document).ready(function(){\n'
                          '\t$("#hide").click(function(){\n'
                          '\t\t$("power").hide();\n'
                          '\t});\n'
                          '\t$("#show").click(function(){\n'
                          '\t\t$("power").show();\n'
                          '\t});\n'
                          '});\n'
                          '</script>\n'
                          '<button id="hide">Hide Power Spectrum</button>\n'
                          '<button id="show">Show Power Spectrum</button>\n'
                          '</div>\n'
                          '<div id="content" style="padding-top: 75px;">\n'
                          '<table style = "width:75%">\n'
                          '\t<tr>\n'
                          '\t\t<td><img src="' + imageforpage + '" alt="star", style="width:500px;height500px;"></td>\n'
                          '\t\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + allplot + '"></iframe></td>\n'
                          '\t</tr>\n'
                          )
            if numzones > 1:
                for p in xrange(0, numzones, 2):
                    #~ UI1 = indexes.index(dir[i] + '_ZONE_' + str(p+1))
                    #~ if numzones % 2 == 0 or p+1 != numzones:
                        #~ UI2 = indexes.index(dir[i] + '_ZONE_' + str(p+2))
                    htmlout.write('<tr>\n')
                    htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + graphs[p] + '"></iframe></td>\n')
                    if numzones % 2 == 0 or p+1 != numzones:
                        htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + graphs[p+1] + '"></iframe></td>\n')
                    htmlout.write('</tr>\n')
            elif numzones == 1:
                #~ UI1 = indexes.index(dir[i] + '_ZONE_1')
                htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + graphs[p] + '"></iframe></td>\n')
            htmlout.write('</table>\n'
                          '<power>\n'
                          '<h2> POWER SPECTRUM </h2>\n'
                          '<table style = "width:75%">\n'
                          )
            if numzones > 1:
                for p in xrange(0, numzones, 2):
                    #~ UI1 = power_index.index(dir[i] + '_ZONE_' + str(p+1) + '_POWERSPEC')
                    #~ if numzones % 2 == 0 or p+1 != numzones:
                        #~ UI2 = power_index.index(dir[i] + '_ZONE_' + str(p+2) + '_POWERSPEC')
                    htmlout.write('<tr>\n')
                    htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + power_graphs[p] + '"></iframe></td>\n')
                    if numzones % 2 == 0 or p+1 != numzones:
                        htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + power_graphs[p+1] + '"></iframe></td>\n')
                    htmlout.write('</tr>\n')
            elif numzones == 1:
                #~ UI1 = power_index.index(dir[i] + '_ZONE_1' + '_POWERSPEC')
                htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + power_graphs[p] + '"></iframe></td>\n')
            htmlout.write('</table>\n'
                          '</power>\n'
                          '</div>\n'
                          '</body>\n'
                          '</html>')
            htmlgo = False
            alright = True
        elif htmlgo is False and alright is False:
            alright = True
            htmlout.write('<!DOCTYPE html>\n'
                          '<html>\n'
                          '<head>\n'
                          '<title>Summer STScI gPhoton HTML pipleline</title>\n'
                          '</head>\n'
                          '<body>\n'
                          '<div id="header" style="position: fixed; background-color: #ffffff; left:0; right:0; top:0; padding:5px;">\n'
                          '<h1>STScI Summer internship pipeline FINAL TARGET | Target' + dir[i] + '</h1>\n'
                          '<form action="' + prevlink + '">\n'
                          '\t<input type="submit" value="Go To Previous Target">\n'
                          '</form>\n'
                          '<form action = "../../../../index.html">\n'
                          '\t<input type="submit" value="go to index">\n'
                          '</form>\n'
                          '</div>\n'
                          '<div id="content" style="padding-top: 75px;">\n'
                          '<table style = "width:75%">\n'
                          '\t<tr>\n'
                          '\t\t<td><img src="' + imageforpage + '" alt="star", style="width:500px;height:500px;"></td>\n'
                          '\t\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + allplot + '"></iframe></td>\n'
                          '\t</tr>\n'
                          )
            if numzones > 1:
                for p in xrange(0, numzones, 2):
                    #~ UI1 = indexes.index(dir[i] + '_ZONE_' + str(p+1))
                    #~ if numzones % 2 == 0 or p+1 != numzones:
                        #~ UI2 = indexes.index(dir[i] + '_ZONE_' + str(p+2))
                    htmlout.write('<tr>\n')
                    htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + graphs[p] + '"></iframe></td>\n')
                    if numzones % 2 == 0 or p+1 != numzones:
                        htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + graphs[p+1] + '"></iframe></td>\n')
                    htmlout.write('</tr>\n')
            elif numzones == 1:
                #~ UI1 = indexes.index(dir[i] + '_ZONE_1')
                htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + graphs[p] + '.embed"></iframe></td>\n')
            htmlout.write('<form action="' + prevlink + '">\n'
                          '\t<input type="submit" value="Go To Previous Target">\n'
                          '</form>\n'
                          '<form action = "../../../../index.html">\n'
                          '\t<input type="submit" value="go to index">\n'
                          '</form>\n'
                          '</table>\n'
                          '</div>\n'
                          '</body>\n'
                          '</html>')
        
        htmlout.close()
        if pagenum > 0:
            prevlink = '../../../../' + addon + '/' + dir[i] + '/' + dir[i] + 'ViewPage.html'
        os.chdir('..')
    os.chdir(working_dir)
os.chdir(start)

gc = gspread.authorize(credentials)
SHEET = gc.open("SDB_TARGET_NOTES")
SOARSHEET = SHEET.worksheet("SOAR")
KNOWNSHEET = SHEET.worksheet("KNOWN")
NORTHSHEET = SHEET.worksheet("NORTH")
SOUTHSHEET = SHEET.worksheet("SOUTH")
SOAR_list = SOARSHEET.range('E2:E288')
KNOWN_list = KNOWNSHEET.range('E2:E9')
NORTH_list = NORTHSHEET.range('E2:E1051')
SOUTH_list = SOUTHSHEET.range('E2:E126')
SOAR_notes = SOARSHEET.range('C2:C288')
KNOWN_notes = KNOWNSHEET.range('C2:C9')
NORTH_notes = NORTHSHEET.range('C2:C1051')
SOUTH_notes = SOUTHSHEET.range('C2:C126')
SOAR_list_name = SOARSHEET.range('A2:A288')
KNOWN_list_name = KNOWNSHEET.range('A2:A9')
NORTH_list_name = NORTHSHEET.range('A2:A1051')
SOUTH_list_name = SOUTHSHEET.range('A2:A126')
rankings = []
rankins_names = []
LIST_list = [[x.value for x in SOAR_list], [x.value for x in KNOWN_list], [x.value for x in NORTH_list], [x.value for x in SOUTH_list]]
LIST_list_name = [[x.value for x in SOAR_list_name], [x.value for x in KNOWN_list_name], [x.value for x in NORTH_list_name],[x.value for x in SOUTH_list_name]]
LIST_list_notes = [[x.value for x in SOAR_notes], [x.value for x in KNOWN_notes], [x.value for x in NORTH_notes], [x.value for x in SOUTH_notes]]
for index, (i, j) in enumerate(zip(LIST_list, LIST_list_name)):
    together = zip(j, i)
    sorted_together = sorted(together)
    LIST_list[index] = [x[1] for x in sorted_together]
for index, (i, j) in enumerate(zip(LIST_list_notes, LIST_list_name)):
    together = zip(j, i)
    sorted_together = sorted(together)
    LIST_list_notes[index] = [x[1] for x in sorted_together]
    LIST_list_name[index] = [x[0] for x in sorted_together]
for index, j in enumerate(LIST_list):
    sub_rank = []
    for number, i in enumerate(j):
        try:
            sub_rank.append([LIST_list_name[index][number], int(i)])
        except ValueError:
            # print 'NON INT VALUE, APPENDING AS STR - CHECK RANK COLUM (E)'
            sub_rank.append([LIST_list_name[index][number], i])
    rankings.append(sub_rank)
notes = []
for j in LIST_list_notes:
        sub_notes = []
        for i in j:
                sub_notes.append(i)
        notes.append(sub_notes)
indexpage = open('index.html', 'w')
linkagg = []
for ARC in ARCHIVES:
    subagg = []
    if ARC == 'SOAR':
        for index, folder in enumerate(SOARDIR):
            link = 'Targets/ARCHIVE/' + ARC + '/' + folder + '/' + folder + 'ViewPage.html'
            subagg.append(link)
    elif ARC == 'KNOWN':
        for index, folder in enumerate(KNOWNDIR):
            #print folder
            link = 'Targets/ARCHIVE/' + ARC + '/' + folder + '/' + folder + 'ViewPage.html'
            subagg.append(link)
    elif ARC == 'NORTHERN':
        for index, folder in enumerate(NORTHDIR):
            link = 'Targets/ARCHIVE/' + ARC + '/' + folder + '/' + folder + 'ViewPage.html'
            subagg.append(link)
    elif ARC == 'SOUTHERN':
        for index, folder in enumerate(SOUTHDIR):
            link = 'Targets/ARCHIVE/' + ARC + '/' + folder + '/' + folder + 'ViewPage.html'
            subagg.append(link)
    linkagg.append(subagg)
linkagg_sorted = [None] * len(linkagg)
linkagg_tied = [None] * len(linkagg)
notes_sorted = [None] * len(notes)
for index_1, SUBARCHIVE in enumerate(rankings):
    sub_linkagg = []
    for index_2, target in enumerate(SUBARCHIVE):
        try:
            sub_linkagg.append(linkagg[index_1][linkagg[index_1].index('Targets/ARCHIVE/' + ARCHIVES[index_1] + '/' + target[0] + '/' + target[0] + 'ViewPage.html')])
        except ValueError:
            sub_linkagg.append('404.html')
    linkagg_tied[index_1] = sub_linkagg
raw_rank = []
for SUBARCHIVE in rankings:
    sub_raw_rank = []
    for element in SUBARCHIVE:
        sub_raw_rank.append(element[1])
    raw_rank.append(sub_raw_rank)
for index, (i, j, k) in enumerate(zip(linkagg_tied, raw_rank, notes)):
    together = zip(j, i, k)
    sorted_together = sorted(together)
    linkagg_sorted[index] = [x[1] for x in sorted_together]
    linkagg_sorted[index].reverse()
    notes_sorted[index] = [x[2] for x in sorted_together]
    notes_sorted[index].reverse()
indexpage.write('<!DOCTYPE html>\n'
                '<html>\n'
                '<head>\n'
                '<title>Summer STScI gPhoton HTML pipleline | DEPLOYMENT VERSION</title>\n'
                '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>\n'
                '</head>\n'
                '<body>\n'
                '<h1>STScI Summer internship FIRST PAGE | DEPLOYMENT VERSION</h1>\n'
                '<p>This is currently being created with the prerun script meaning it is in active development, features may not work or may be semi working, thanks for your paitience</p>\n'
                '<p> Current Bugs: while moving all graphs to locally hosted plotly graphs there are issues with many not showing up due to me not having fully migrated, this will be fixed soon, '
                'I have to modify the graph make routien to run for multiple subarchives but that will not take all too long to do, so hopefully by the end of friday all targets or at least most '
                'targets should be working. Everything else here is more or less in working order, updates from google sheets work (tho the script has to be re run for them to take effect, once I '
                'get the buttons working fully I am going to make a cron job to run it every couple minutes or so so that it "live" updates) Cool</p>\n'
                '<form action="' + firstlink + '">\n'
                '\t<input type="submit" value="Go To First Target">\n'
                '</form>\n'
                '<h2>TARGET INDEX</h2>\n') 
check_link_size = [len(linkagg_sorted[0]), len(linkagg_sorted[1]), len(linkagg_sorted[2]), len(linkagg_sorted[3])]
max_links = max(check_link_size)
max_index = check_link_size.index(max_links)
for index, SUBARCHIVE in enumerate(linkagg_sorted):
    indexpage.write('<table style="border: 1px solid black">\n')
    if index is 0:
        indexpage.write('\t<tr>\n')
        indexpage.write('\t<td> </td>\n')
        indexpage.write('\t<td><h3>SOAR</h3></td>\n')
    elif index is 1:
        indexpage.write('\t<tr>\n')
        indexpage.write('\t<td> </td>\n')
        indexpage.write('\t<td><h3>KNOWN</h3></td>\n')
    elif index is 2:
        indexpage.write('\t<tr>\n')
        indexpage.write('\t<td> </td>\n')
        indexpage.write('\t<td><h3>NORTHERN | NDC</h3></td>\n')
    elif index is 3:
        indexpage.write('\t<tr>\n')
        indexpage.write('\t<td> </td>\n')
        indexpage.write('\t<td><h3>SOUTHERN</h3></td>\n')
    for number, linkdata in enumerate(SUBARCHIVE):
        if linkdata == '404.html' or linkdata.split('/')[4] not in os.listdir(linkdata.split('/')[0] + '/' + linkdata.split('/')[1] + '/' + linkdata.split('/')[2] + '/' + linkdata.split('/')[3]):
            print 'NO TARGET DATA | ', ARCHIVES[index]
            use_link = '404.html'
            use_note = 'Data not in Local archive yet'
        else:
            use_link = linkdata
            use_note = str(notes_sorted[index][number])
        try:
            indexpage.write('\t\t<td>\n'
                    '\t\t\t<form action = "' + use_link + '">\n'
                    '\t\t\t\t<input type="submit" value="' + linkdata.split('/')[3] + '">\n'
                    '\t\t\t</form>\n'
                    '\t\t</td>\n')
        except IndexError:
            indexpage.write('\t\t<td>\n'
                    '\t\t\t<form action = "' + use_link + '">\n'
                    '\t\t\t\t<input type="submit" value="' + linkdata + '">\n'
                    '\t\t\t</form>\n'
                    '\t\t</td>\n')
    indexpage.write('\t</tr>\n\t<tr>\n'
                    '\t\t<td> </td>\n'
                    '\t\t<td><h3>Rank</h3></td>\n')
    run_list = sorted(raw_rank[index])
    for number, rank in enumerate(reversed(run_list)):
        indexpage.write('\t\t<td>' + str(rank) + '</td>\n')
    indexpage.write('\t</tr>\n\t<tr>\n'
                    '\t\t<td> </td>\n'
                    '\t\t<td><h3>Notes</h3></td>\n')
    for number, notes in enumerate(notes_sorted[index]):
        indexpage.write('\t\t<td>' + str(notes) + '</td>\n')
    indexpage.write('\t</tr>\n</table>\n')
indexpage.write('<script type="text/javascript">\n'
                                '//<![CDATA[\n'
                                '$(window).load(function(){\n'
                                '\t$("table").each(function() {\n'
                                '\t\tvar $this = $(this);\n'
                                '\t\tvar newrows = [];\n'
                                '\t\t$this.find("tr").each(function(){\n'
                                '\t\t\tvar i = 0;\n'
                                '\t\t\t$(this).find("td, th").each(function(){\n'
                                '\t\t\t\ti++;\n'
                                '\t\t\t\tif(newrows[i] === undefined) { newrows[i] = $("<tr></tr>"); }\n'
                                '\t\t\t\tif(i == 1)\n'
                                '\t\t\t\t\tnewrows[i].append("<th>" + this.innerHTML  + "</th>");\n'
                                '\t\t\t\telse\n'
                                '\t\t\t\t\tnewrows[i].append("<td>" + this.innerHTML  + "</td>");\n'
                                '\t\t\t});\n'
                                '\t\t});\n'
                                '\t\t$this.find("tr").remove();\n'
                                '\t\t$.each(newrows, function(){\n'
                                '\t\t\t$this.append(this);\n'
                                '\t\t});\n'
                                '\t});\n'
                                '\treturn false;\n'
                                '});//]]>\n'
                                '</script>\n'
                '</body>\n'
                '</html>')
indexpage.close()
