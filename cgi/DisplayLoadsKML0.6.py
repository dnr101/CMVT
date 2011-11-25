#!/usr/bin/python
#Filename: DisplayLoads0.1.py

import sys
import os
import cgi
import cgitb
#from MapPlacemark import MapPlacemark
#cgitb.enable()
os.environ['HOME'] = '/var/www/html/Thesis/cgi/figs'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import numpy as np
import urllib
from scipy import stats

form = cgi.FieldStorage()
pol = form.getvalue('basin', 'JA')
#nutrient = form.getvalue('nutrient', 'N')
scenario = form.getvalue('scenario', '1')
scenario = int(scenario)

if pol == 'EL':
    selBasin = 'Lower Eastern Shore'
elif pol == 'EM':
    selBasin = 'Middle Eastern Shore'
elif pol == 'EU':
    selBasin = 'Upper Eastern Shore'
elif pol == 'JA':
    selBasin = 'Appomatox'
elif pol == 'JL':
    selBasin = 'Lower James'
elif pol == 'JU':
    selBasin = 'Upper James'
elif pol == 'PL':
    selBasin = 'Lower Potomac'
elif pol == 'RU':
    selBasin = 'Upper Rappahannock'
elif pol == 'RL':
    selBasin = 'Lower Rappahannock'
elif pol == 'WL':
    selBasin = 'Lower Western Shore'
elif pol == 'WM':
    selBasin = 'Middle Western Shore'
elif pol == 'WU':
    selBasin = 'Upper Western Shore'
elif pol == 'XL':
    selBasin = 'Lower Patuxent'
elif pol == 'XU':
    selBasin = 'Upper Patuxent'
elif pol == 'YL':
    selBasin = 'Lower York'
elif pol == 'YM':
    selBasin = 'Mattaponi'
elif pol == 'YP':
    selBasin = 'Pamunkey'
elif pol == 'JB':
    selBasin = 'James Below Richmond'
elif pol == 'PM':
    selBasin = 'Middle Potomac'
elif pol == 'PU':
    selBasin = 'Upper Potomac'
elif pol == 'PS':
    selBasin = 'Shenandoah'
elif pol == 'SL':
    selBasin = 'Lower Susquehanna'
elif pol == 'SU':
    selBasin = 'Upper Susquehanna'
elif pol == 'SJ':
    selBasin = 'Juniata'
elif pol == 'SW':
    selBasin = 'Susquehanna, West Branch'
else:
    selBasin = 'Basin Missing'

goodBasins = ['EL', 'EM', 'EU', 'JA', 'JL', 'JU', 'PL', 'RL', 'RU', 'WL', 'WM', 'WU', 'XL', 'XU', 'YL', 'YM', 'YP']

def updateFusionTable():
   pass

def drawFigure(load, land, fg, loadStr, landStr):
    fitM, fitB = pylab.polyfit(land, load, 1)
#    r = np.corrcoef(land, load)[0, 1]
#    r2 = r**2
    r, p = stats.pearsonr(land, load)
    r2 = r**2
    fitX = [min(land), max(land)]
    fitY = [((min(land)*fitM)+fitB), ((max(land)*fitM)+fitB)]
    fitLine = matplotlib.lines.Line2D(fitX, fitY)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(land, load)
#    ax.add_line(fitLine)
    landLabel = 'Percent %s' %landStr
    loadLabel = '%s Load (kg/yr/acre)' %loadStr
    titleStr = '%s vs. Percent %s Land Use' %(loadStr, landStr)
    slopeLable = 'Pearson correlation coefficient: %2.5f\
            \nCoefficient of determination: %2.5f\
            \nTwo tailed p-value: %2.5f' %(r, r2, p)
    plt.xlabel(landLabel)
    plt.ylabel(loadLabel)
    plt.title(titleStr)
    plt.text(0.1, 0.75, slopeLable, transform = ax.transAxes)
    fig.savefig(fg)


def getLoadData(basin, scen):
    scenOffset = 4
    pOffset = 13
    sedOffset = 26
    acreOffset = 39
    n_elt = scen + scenOffset
    p_elt = scen + scenOffset + pOffset
    sed_elt = scen + scenOffset + sedOffset
    acre_elt = scen + scenOffset + acreOffset
    dataFile = open('files/P5.3_Loads-Acres_del.csv', 'r')
    dataList = []
    for dataLine in dataFile:
        if dataLine[:6] == 'labels' or dataLine[:5] == 'River':
            continue
        elif dataLine[:2] == basin:
            dataLine = dataLine.strip().split(',')
            #acres = float(dataLine[acre_elt])
            dataList.append([dataLine[0], int(dataLine[n_elt]), int(dataLine[p_elt]), \
                    int(dataLine[sed_elt]), float(dataLine[acre_elt])])
    dataDict = {}
    for d in dataList:
        dataDict[d[0]] = [0, 0, 0, 0]
    for d in dataList:
        l = dataDict[d[0]]
        l[0] += d[1]
        l[1] += d[2]
        l[2] += d[3]
        l[3] += d[4]
        dataDict[d[0]] = l
    dataFile.close()
    return dataDict

def getLU(basin, scen):
    scen = int(scen)
    LU = 4
    scenOffset = 4
    acreOffset = 39
    acre_elt = scen + scenOffset + acreOffset

    dataFile = open('files/P5.3_Loads-Acres_del.csv', 'r')
    dataList = []
    #25 lu's waste, septic and atmos depo are sources, not lu's
    #16 agg lu's
    aggLU = ['hwm', 'nhi', 'hom', 'nho', 'lwm', 'nlo',\
              'hyw', 'nhy', 'alf', 'nal', 'hyo', 'pas',\
              'npa', 'trp', 'afo', 'urs']
    #7 urb lu's
    urbLU = ['puh', 'pul', 'imh', 'iml', 'bar', 'ext', 'css']
    wasteLU = ['ps']
    septLU = ['septic']
    #2 for lu's
    forLU = ['for', 'hvf']
    atdepLU = ['atdep']
    totAgg = 0
    totUrb = 0
    totWaste = 0
    totSept = 0
    totFor = 0
    totAt = 0
    totalAcres = 0

    for dataLine in dataFile:
        if dataLine[:2] == basin:
            dataLine = dataLine.strip().split(',')
            if dataLine[LU] in aggLU:
                totAgg += int(dataLine[acre_elt])
            if dataLine[LU] in urbLU:
                totUrb += int(dataLine[acre_elt])
            if dataLine[LU] in wasteLU:
                totWaste += int(dataLine[acre_elt])
            if dataLine[LU] in septLU:
                totSept +=int(dataLine[acre_elt])
            if dataLine[LU] in forLU:
                totFor += int(dataLine[acre_elt])
            if dataLine[LU] in atdepLU:
                totAt += int(dataLine[acre_elt])
            totalAcres += int(dataLine[acre_elt])
    dataFile.close()
    return (totAgg, totUrb, totFor, float(totalAcres))

def getDELLoads(rDataDict):
    rivCen = open('files/riverCentroids.csv', 'r')
    rivNames = open('files/rivernames.csv', 'r')
    names = []
    points = []
    fin = []
    for n in rivNames:
        n = n.strip().split(',')
        if n[0] == 'river':
            continue
        names.append(n)
    for cen in rivCen:
        cen = cen.strip().split(',')
        points.append(cen)
    for p in points:
        data = rDataDict.get(p[2])
        if data != None:
            p.append(float(data[0])/float(data[3]))
            p.append(float(data[1])/float(data[3]))
            p.append(float(data[2])/float(data[3]))
            p.append(float(data[3]))
            fin.append(p)
    for f in fin:
        for nm in names:
            if f[2] == nm[0]:
                f.append(nm[1])

    rivNames.close()
    rivCen.close()
    return tuple(fin)


def getSum(rDataDict):
    summary = [0, 0, 0, 0]
    for elt in rDataDict.itervalues():
        for i in range(len(summary)):
            summary[i] += elt[i]

    return tuple(summary)

myLoadDict = getLoadData(pol, scenario)
myLoads = getDELLoads(myLoadDict)
#print "*******************",myLoads[1],"******************"
points = []
messages = []
for p in myLoads:
    points.append([p[0], p[1]])
    messages.append(('%s<br/>Tot N: %.3f kg/yr/acre<br/>Tot P: %.3f kg/yr/acre<br/>Sus Solids: %.3f kg/yr/acre') %(p[7], p[3], p[4], p[5]))
totals = getSum(myLoadDict)
landUse = getLU(pol, scenario)
dev = []
und = []
agg = []
n = []
p = []
s = []

for b in goodBasins:
    lu = getLU(b, scenario)
    nu = getSum(getLoadData(b, scenario))
    agg.append(lu[0]/lu[3])
    dev.append(lu[1]/lu[3])
    und.append(lu[2]/lu[3])
    n.append(nu[0]/nu[3])
    p.append(nu[1]/nu[3])
    s.append(nu[2]/nu[3])

nutrs = {'Nitrogen':n, 'Phosphorous':p, 'Suspended Sediment':s}
uses = {'Urban Runoff':dev, 'Forest':und, 'Agricultural':agg}
f = 1
for nu in nutrs.iterkeys():
    for us in uses.iterkeys():
        figName = 'figs/figure%d.png' %f
        drawFigure(nutrs[nu], uses[us], figName, nu, us)
        f += 1

print 'Content-Type: text/html'
print
print '''\
        <!DOCTYPE html public "-//W3C//DTD HTML 4.01 //EN">
        <html>
        <head>
        <title>Chesapeake Bay CMVT</title>
        <link rel="stylesheet" type="text/css" href="../css/phase5.css" />
        <link rel="icon" type="image/png" href="../images/cmvt_favicon.png" />
        <script src="../scripts/jquery-1.6.2.js"></script>
        <script src="http://maps.google.com/maps/api/js?sensor=false"></script>
        <script src="../scripts/galleria/galleria-1.2.5.js"></script>
        <script src="../scripts/showBayMapMarkersKML-2.js"></script>
        '''

print '''\
        </head>
        <body  onload="initialize(%s, %s, %s, \'%s\')">
        <div id="controls">
        <a href="../ChesBayCMVT.1.5.html">Return to selection page</a>
        <h1>Average Annual Nutrient Loads on the %s Basin</h1><hr/>
        <center><h3>Nutrient Flags</h3>
        <input type="button" value="Toggle\nN or P" onClick="changeAll();">
        <input type="button" value="Toggle\nOn-Off" onClick="togAll();"></center><hr/>
        <h3>Key:</h3>
        <ul>Red flag: Total Measured Nutrien in kg/year/acre is 10 percent above the Total Measurable Daily Load Allocation</ul>
        <ul>Yellow flag: Total Measured Nutrient in kg/year/acre is within percent of the Total Measurable Daily Load Allocation</ul>
        <ul>Green flag: Total Measured Nutrient in kg/year/acre is percent below the Total Measurable Daily Load Allocation</ul><hr/>

''' % (points, messages, list(myLoads), pol, selBasin)

#for mark in allMarks.itervalues():
#    print mark.getPlacemark()
i = 0
for load in myLoads:
    print '''<p>Segment: %s \
            <input type="button" value="Marker\nOn Off" onClick="togMark(%d);">
            <br />Total Nitrogen: %2.2f kg/yr/acre
            <br />Total Phosphorus: %2.2f kg/yr/acre
            <br />Total Sus Sediment: %2.2f kg/yr/acre</p><hr />''' % (load[7], i, load[3], load[4], load[5])
    i += 1

print '''\
        </div>
        <div id="map_canvas">
        <h3>Map of Nutrient and Sediment Loading on the %s Basin of the Chesapeake Bay Watershed</h3>
        </div>
        <div id="summary">
        <div id="totals">
        <h3>Basin Summary:</h3>
        <ul>Total Nitrogen: %4.4f kg/year/acre</ul>
        <ul>Total Phosphorus: %4.4f kg/year/acre</ul>
        <ul>Total Suspended Sediment: %4.4f kg/year/acre</ul>
        </div>
        <div id="land_use">
        <h3>Land Use for the %s Basin:</h3>
        <ul>Total Area: %5.2d acres</ul>
        <ul>Agricultural Land Use: %2.2f%%</ul>
        <ul>Urban Land Use: %2.2f%%</ul>
        <ul>Undeveloped Forest Land Use: %2.2f%%</ul>
        </div>
        <div id="graphs">
        <h3>Scatter Plots of Nutrient Loading vs. Land Use Category for the entire Chesapeake Bay Watershed:</h3>
        <div id="gallery">
        '''%(selBasin, totals[0]/totals[3], totals[1]/totals[3], totals[2]/totals[3], selBasin,\
             landUse[3], landUse[0]/landUse[3]*100, landUse[1]/landUse[3]*100, landUse[2]/landUse[3]*100)

#figures = os.listdir('figs/')
for i in range(1, 10):
    if i == 0:
        figure = 'figure%d.png'% i
        print '<img src="figs/%s" alt="" class="active"/>'% figure
    else:
        figure = 'figure%d.png'% i
        print '<img src="figs/%s" alt="" />' % figure
print '''\
        </div>
        </div>
        </div>
        <script type="text/javascript">
            Galleria.loadTheme('../scripts/galleria/themes/classic/galleria.classic.js');
            $("#gallery").galleria({
                width: 800,
                height: 600,
                carousel: false,
                preload: 'all',
                debug: false,
                transition: 'fadeslide'
            });
        </script>
        </body>
        </html>
     '''
