import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
sys.path.append('C:\\Users\\zxin1\\anaconda3\\Lib\\site-packages')
import os
import timeit

import subprocess
from UTool.dirLocation import DirUsr
from UTool.dataIO import pyDataIO
from UTool.dataCtl import strUtil

from USimEngine.URuntime.USDARuntime import runtimeSim

from DataParse.heatmap import heatmapParse

from ladybug.graphic import GraphicContainer
from ladybug_geometry.geometry3d.pointvector import Point3D

##################################################
worker = 6
##################################################
'1. change initial run file name'
os.chdir(DirUsr.modelWithGridDir)
os.rename("annual_daylight", "initial")
# DACustomRunFileName = 'test'

# '2. rerun the DA simulation from python'

# cmd = ('queenbee local run ' + 
#        DirUsr.DASimEngine +
#        ' -i ' + DirUsr.DAConfigFile +
#        ' -w ' + str(worker) +
#        ' -n ' +  DACustomRunFileName +
#        ' ' + DirUsr.modelWithGridDir
#        )

# # cmd = ('pollination dsl run annual-daylight' + 
# #        ' -i ' + 'C:\\Users\\zxin1\\simulation\\unnamed_2e7a048d\\annual_daylight_inputs.json' +
# #        ' -w ' + str(worker) +
# #        ' -n ' +  DACustomRunFileName
# #        )

cmd = ('lbt-recipes run' +
       ' -p ' + DirUsr.modelWithGridDir + 
       ' -w ' + str(worker) +
       ' annual-daylight ' +
       DirUsr.DAConfigFile
        )

# print(cmd)

start = timeit.default_timer()
subprocess.call(cmd,
                shell = True,
                executable = DirUsr.CMD)
stop = timeit.default_timer()
time = start - stop #54s


metricPathDA = "E:\\CMU\\thesis\\1127\\scriptsEnv\\RModel\\modelGrid\\annual_daylight\\metrics\\da\\SensorGrid_58a53f51.da"
metricPathCDA = "E:\\CMU\\thesis\\1127\\scriptsEnv\\RModel\\modelGrid\\annual_daylight\\metrics\\cda\\SensorGrid_58a53f51.cda"
metricPathUDI = "E:\\CMU\\thesis\\1127\\scriptsEnv\\RModel\\modelGrid\\annual_daylight\\metrics\\udi\\SensorGrid_58a53f51.udi"
metricPathUDIL = "E:\\CMU\\thesis\\1127\\scriptsEnv\\RModel\\modelGrid\\annual_daylight\\metrics\\udi_lower\\SensorGrid_58a53f51.udi"
metricPathUDIU = "E:\\CMU\\thesis\\1127\\scriptsEnv\\RModel\\modelGrid\\annual_daylight\\metrics\\udi_upper\\SensorGrid_58a53f51.udi"

pMin = [-19.42, 0.50, 1.20]
pMax = [-0.50, 9.57, 1.20]
LB_pt3DMin = Point3D.from_array(pMin)
LB_pt3DMax = Point3D.from_array(pMax)

metricPathsDic = {metricPathDA: 'DA', 
                  metricPathCDA: 'CDA', 
                  metricPathUDI: 'UDIM',
                  metricPathUDIL: 'UDIL',
                  metricPathUDIU: 'UDIU'
                  }

'create color matrix for DA, cDA, UDI'
for metricPath in metricPathsDic:
    rawData = pyDataIO.readSimpleFile(metricPath)
    updatedData = strUtil.batchFromStrToFloat(rawData)
    graphic = GraphicContainer(updatedData, LB_pt3DMin, LB_pt3DMax, None)
    colorsLst = graphic.value_colors

    simplifiedColorLst = []
    for color in colorsLst:
        RVal = str(format(color[0]/255, '.2f')) 
        GVal = str(format(color[1]/255, '.2f'))
        BVal = str(format(color[2]/255, '.2f'))
        AVal = str(format(color[3]/255, '.2f'))
        
        strColorLst = [RVal, GVal, BVal, AVal]
        simplifiedColorLst.append(strColorLst)

    colorCSVPath = DirUsr.modelWithGridDir + '\\colorMatrix' + metricPathsDic[metricPath] + '.csv'
    heatmapParse.colorsToCSV(simplifiedColorLst, colorCSVPath)
    
'create color matrix for sDA'
sDALst, sDA = runtimeSim.simulateSDARuntime(metricPathDA, 50)
SDAGraphic = GraphicContainer(sDALst, LB_pt3DMin, LB_pt3DMax, None)
SDAColorsLst = SDAGraphic.value_colors

simplifiedColorLstSDA = []
for color in SDAColorsLst:
    RVal = str(format(color[0]/255, '.2f')) 
    GVal = str(format(color[1]/255, '.2f'))
    BVal = str(format(color[2]/255, '.2f'))
    AVal = str(format(color[3]/255, '.2f'))
    
    strColorLst = [RVal, GVal, BVal, AVal]
    simplifiedColorLstSDA.append(strColorLst)

colorCSVPathSDA = DirUsr.modelWithGridDir + '\\colorMatrixSDA.csv'
heatmapParse.colorsToCSV(simplifiedColorLstSDA, colorCSVPathSDA)
pyDataIO.writeToNewFile(sDA, DirUsr.modelWithGridDir + '\\sDAValue.txt')




