import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('SummerSTScI-ca588a8e388a.json', scope)

gc = gspread.authorize(credentials)
checkstar = 'sdssj9-10_212232.68+000426.6'
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
        print Uitem, Iitem
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
#    print 'number ', index, 'of ', len(indexes)
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
ARCHIVES = ['KNOWN', 'SOAR', 'NORTHERN', 'SOUTHERN']
for subdir in ARCHIVES:
    print 'CURRENT DIRECTORY IS: ', os.path.abspath('.')
    os.chdir(start)
    os.chdir('Targets/ARCHIVE/' + subdir)
    working_dir = os.path.abspath('.')
    dir = os.listdir('.')
    if subdir == 'KNOWN':
        KNOWNDIR = dir
    elif subdir == 'SOAR':
        SOARDIR = dir
    elif subdir == 'NORTH':
        NORTHDIR = dir
    elif subdir == 'SOUTH':
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
        for x in checkzones:
            if '.png' in x and 'ZONE' in x and not '._' in x:
                zonefind = x.find('ZONE')
                try:
                    checknum = int(x[zonefind + 5:zonefind + 7])
                    pathtox[checknum - 1] = x
                except ValueError:
                    checknum = int(x[zonefind + 5])
                    pathtox[checknum -1] = x
                if checknum > int(numzones):
                    numzones = checknum
                else:
                    pass
            elif '.png' in x and 'Count' in x and '._' not in x[0:3]:
                imageforpage = x
        if firstlinkrec is False:
            firstlink = addon + '/' + dir[i] + '/' + dir[i] + 'ViewPage.html'
            firstlinkrec = True
        else:
            pass
        if alright is False:
            htmlout = open(dir[i] + 'ViewPage.html', 'w')
        try:
            zoneindex = targetzone_ind.index(dir[i])
        except ValueError:
            os.chdir(working_dir)
            continue
        numzones = targetzone_use[zoneindex]
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
        allplot = all_url[all_index.index(dir[i])]
        if dir[i] == 'sdssj9-10_212232.68+000426.6':
            print htmlgo, alright
        if htmlgo is True and alright is False:
            #print 'writing out file for', dir[i]
            htmlout.write('<!DOCTYPE html>\n'
                          '<html>\n'
                          '<head>\n'
                          '<title>Summer STScI gPhoton HTML pipleline</title>\n'
                          '</head>\n'
                          '<body>\n'
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
                          '<body onload="hide">\n'
                          '<table style = "width:75%">\n'
                          '\t<tr>\n'
                          '\t\t<td><img src="' + imageforpage + '" alt="star", style="width:500px;height500px;"></td>\n'
                          '\t\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + allplot + '"></iframe></td>\n'
                          '\t</tr>\n'
                          )
            if numzones > 1:
                for p in xrange(0, numzones, 2):
                    UI1 = indexes.index(dir[i] + '_ZONE_' + str(p+1))
                    if numzones % 2 == 0 or p+1 != numzones:
                        UI2 = indexes.index(dir[i] + '_ZONE_' + str(p+2))
                    htmlout.write('<tr>\n')
                    htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + ulrs[UI1] + '"></iframe></td>\n')
                    if numzones % 2 == 0 or p+1 != numzones:
                        htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + ulrs[UI2] + '"></iframe></td>\n')
                    htmlout.write('</tr>\n')
            elif numzones == 1:
                UI1 = indexes.index(dir[i] + '_ZONE_1')
                htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + ulrs[UI1] + '"></iframe></td>\n')
            htmlout.write('</table>\n'
                          '<power>\n'
                          '<h2> POWER SPECTRUM </h2>\n'
                          '<table style = "width:75%">\n'
                          )
            if numzones > 1:
                for p in xrange(0, numzones, 2):
                    UI1 = power_index.index(dir[i] + '_ZONE_' + str(p+1) + '_POWERSPEC')
                    if numzones % 2 == 0 or p+1 != numzones:
                        UI2 = power_index.index(dir[i] + '_ZONE_' + str(p+2) + '_POWERSPEC')
                    htmlout.write('<tr>\n')
                    htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + power_url[UI1] + '"></iframe></td>\n')
                    if numzones % 2 == 0 or p+1 != numzones:
                        htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + power_url[UI2] + '"></iframe></td>\n')
                    htmlout.write('</tr>\n')
            elif numzones == 1:
                UI1 = power_index.index(dir[i] + '_ZONE_1' + '_POWERSPEC')
                htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + power_url[UI1] + '"></iframe></td>\n')
            htmlout.write('</table>\n'
                          '</power>\n'
                          '<h2>Flag Lookup Table</h2>'
                          '<table>\n'
                              '<tr><td>1 - (0 power scale) - Hotspot</td></tr>\n'
                              '<tr><td>2 - (1 power scale) - Mask Edge</td></tr>\n'
                              '<tr><td>4 - (3 power scale) - exptime</td></tr>\n'
                              '<tr><td>8 - (4 power scale) - respose</td></tr>\n'
                              '<tr><td>16 - (5 power scale) - nonlinearity</td></tr>\n'
                              '<tr><td>32 - (6 power scale) - detector edge</td></tr>\n'
                              '<tr><td>64 - (7 power scale) - Backgrond hotspot</td></tr>\n'
                              '<tr><td>128 - (8 power scale) - Backgound mask</td></tr>\n'
                          '</table>\n'
                          '<form action="' + nextlink + '">\n'
                          '\t<input type="submit" value="Go To Next Target">\n'
                          '</form>\n'
                          '<form action="' + prevlink + '">\n'
                          '\t<input type="submit" value="Go To Previous Target">\n'
                          '</form>'
                          '<form action = "../../../../../index.html">\n'
                          '\t<input type="submit" value="go to index">\n'
                          '</form>\n'
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
                          '<h1>STScI Summer internship pipeline FINAL TARGET | Target' + dir[i] + '</h1>\n'
                          '<form action="' + prevlink + '">\n'
                          '\t<input type="submit" value="Go To Previous Target">\n'
                          '</form>\n'
                          '<form action = "../../../../index.html">\n'
                          '\t<input type="submit" value="go to index">\n'
                          '</form>\n'
                          '<table style = "width:75%">\n'
                          '\t<tr>\n'
                          '\t\t<td><img src="' + imageforpage + '" alt="star", style="width:500px;height:500px;"></td>\n'
                          '\t\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + allplot + '.embed"></iframe></td>\n'
                          '\t</tr>\n'
                          )
            if numzones > 1:
                for p in xrange(0, numzones, 2):
                    UI1 = indexes.index(dir[i] + '_ZONE_' + str(p+1))
                    if numzones % 2 == 0 or p+1 != numzones:
                        UI2 = indexes.index(dir[i] + '_ZONE_' + str(p+2))
                    htmlout.write('<tr>\n')
                    htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + ulrs[UI1] + '.embed"></iframe></td>\n')
                    if numzones % 2 == 0 or p+1 != numzones:
                        htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + ulrs[UI2] + '.embed"></iframe></td>\n')
                    htmlout.write('</tr>\n')
            elif numzones == 1:
                UI1 = indexes.index(dir[i] + '_ZONE_1')
                htmlout.write('\t<td><iframe width="650" height="650" frameborder="0" scrolling="no" src="' + ulrs[UI1] + '.embed"></iframe></td>\n')
            htmlout.write('<form action="' + prevlink + '">\n'
                          '\t<input type="submit" value="Go To Previous Target">\n'
                          '</form>\n'
                          '<form action = "../../../../index.html">\n'
                          '\t<input type="submit" value="go to index">\n'
                          '</form>\n'
                          '</table>\n'
                          '</body>\n'
                          '</html>')
        
        htmlout.close()
        if pagenum > 0:
            prevlink = '../../../../' + addon + '/' + dir[i] + '/' + dir[i] + 'ViewPage.html'
        os.chdir('..')
        print 'HERE'
    os.chdir(working_dir)
os.chdir(start)

gc = gspread.authorize(credentials)
SHEET = gc.open("SDB_TARGET_NOTES")
SOARSHEET = SHEET.worksheet("SOAR")
KNOWNSHEET = SHEET.worksheet("KNOWN")
NORTHSHEET = SHEET.worksheet("NORTH")
SOUTHSHEET = SHEET.worksheet("SOUTH")
SOAR_list = SOARSHEET.range('E2:E288')
KNOWN_list = KNOWNSHEET.range('E2:E8')
NORTH_list = NORTHSHEET.range('E2:E10')
SOUTH_list = SOUTHSHEET.range('E2:E10')
SOAR_list_name = SOARSHEET.range('A2:A288')
KNOWN_list_name = KNOWNSHEET.range('A2:A8')
NORTH_list_name = NORTHSHEET.range('A2:A10')
SOUTH_list_name = SOUTHSHEET.range('A2:A10')
rankings = []
rankins_names = []
LIST_list = [SOAR_list, KNOWN_list, NORTH_list, SOUTH_list]
LIST_list_name = [SOAR_list_name, KNOWN_list_name, SOUTH_list_name]
LIST_list = sorted(LIST_list)
LIST_list_name = sorted(LIST_list_name)
for index, (i, j) in enumerate(zip(LIST_list, LIST_list_name)):
    LIST_list[index] = [x for (y, x) in sorted(zip(j, i))]
for j in LIST_list:
    sub_rank = []
    sub_name = []
    for i in j:
        try:
            sub_rank.append(int(i.value))
        except ValueError:
            print 'NON INT VALUE, APPENDING AS STR - CHECK RANK COLUM (E)'
            sub_rank.append(i.value)
    rankings.append(sub_rank)
rankings = [rankings[0], rankings[3], rankings[2], rankings[1]]
indexpage = open('index.html', 'w')
linkagg = []
for ARC in ARCHIVES:
    print ARC
    print 'KNOWNDIR:', KNOWNDIR
    subagg = []
    if ARC == 'SOAR':
        for index, folder in enumerate(SOARDIR):
            link = 'Targets/ARCHIVE/' + ARC + '/' + folder + '/' + folder + 'ViewPage.html'
            subagg.append(link)
    elif ARC == 'KNOWN':
        for index, folder in enumerate(KNOWNDIR):
            print folder
            link = 'Targets/ARCHIVE/' + ARC + '/' + folder + '/' + folder + 'ViewPage.html'
            subagg.append(link)
    elif ARC == 'NORTH':
        for index, folder in enumerate(NORTHDIR):
            link = 'Targets/ARCHIVE/' + ARC + '/' + folder + '/' + folder + 'ViewPage.html'
            subagg.append(link)
    elif ARC == 'SOUTH':
        for index, folder in enumerate(SOUTHDIR):
            link = 'Targets/ARCHIVE/' + ARC + '/' + folder + '/' + folder + 'ViewPage.html'
            subagg.append(link)
    linkagg.append(subagg)
linkagg_sorted = []
print '@@@@@@@@@@@@@@@@@@'
print linkagg
print '@@@@@@@@@@@@@@@@@@'
for i, j in zip(linkagg, rankings):
    print '||||||||||||||||||'
    print 'RANKINGS:', rankings
    print 'i', i
    print 'j', j
    print '||||||||||||||||||'
    linkagg_sorted.append([x for (y, x) in sorted(zip(j, i))])
indexpage.write('<!DOCTYPE html>\n'
                '<html>\n'
                '<head>\n'
                '<title>Summer STScI gPhoton HTML pipleline | EXPERIMENTAL VERSION</title>\n'
                '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>\n'
                '</head>\n'
                '<body>\n'
                '<h1>STScI Summer internship FIRST PAGE | EXPERIMENTAL VERSION</h1>\n'
                '<p>This is currently being created with the prerun script meaning it is in active development, features may not work or may be semi working, thanks for your paitience</p>\n'
                '<p> Currently there is an issue with the flag system so just ignore the colors, also it cause PG_0016+151 to break, the jackalope is the placeholder and there are some issues, hopefully they will be sorted soon, bye now</p>\n'
                '<form action="' + firstlink + '">\n'
                '\t<input type="submit" value="Go To First Target">\n'
                '</form>\n'
                '<h2>TARGET INDEX</h2>\n'
                '<table>\n') 
check_link_size = [len(linkagg_sorted[0]), len(linkagg_sorted[1]), len(linkagg_sorted[2]), len(linkagg_sorted[3])]
max_links = max(check_link_size)
for index, SUBARCHIVE in enumerate(linkagg_sorted):
    if index is 0:
        indexpage.write('\t<tr>\n')
        indexpage.write('\t<td><h3>KNOWN</h3></td>\n')
    elif index is 1:
        indexpage.write('\t<tr>\n')
        indexpage.write('\t<td><h3>SOAR</h3></td>\n')
    elif index is 2:
        indexpage.write('\t<tr>\n')
        indexpage.write('\t<td><h3>NORTHERN</h3></td>\n')
    elif index is 3:
        indexpage.write('\t<tr>\n')
        indexpage.write('\t<td><h3>SOUTHERN</h3></td>\n')
    for linkdata in SUBARCHIVE:
        indexpage.write('\t\t<td>\n'
                        '\t\t\t<form action = "' + linkdata + '">\n'
                        '\t\t\t\t<input type="submit" value="' + linkdata + '">\n'
                        '\t\t\t</form>\n'
                        '\t\t<p> ' + str(index) + ' Notes: TODO<p>\n'
                        '\t\t</td>\n'

                )
        for num_max in range(max_links):
            for empty_cells in range(3-index):
                indexpage.write('\t\t<td> </td>\n')
    indexpage.write('\t</tr>\n')
indexpage.write('</table>\n'
				'<script type="text/javascript">\n'
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
