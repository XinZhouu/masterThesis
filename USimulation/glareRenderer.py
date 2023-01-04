import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
sys.path.append('C:\\Users\\zxin1\\anaconda3\\Lib\\site-packages')

from DataParse.UEData import UEIO
from DataParse.RadData import combRad
from DataParse.evalglare import evalglareParse

from UTool.dataIO import pyDataIO, sysDataIO
from UTool.dirLocation import DirUsr
from UTool.dataCtl import strUtil

from USimEngine.UHoneybee.hbView import viewHB
from USimEngine.UHoneybee.hbSky import sky
from USimEngine.URadiance.Radiance import transRad
from USimEngine.UAcceleRad.AcceleRad import fastRender
from USimEngine.URadiance.Radiance import radGlare, postprocess
#############################################
epwFile = DirUsr.epwPath
radPara = '-aa 0.25 -ab 4 -ad 512 -ar 16 -as 128'
#############################################
'''
-1. clear files in hdrFolder
'''
sysDataIO.delFilesInFolder(DirUsr.hdrDir)
'''
0. get time from Unreal Engine
'''
month, day, hour = pyDataIO.readDayFile(DirUsr.inputDataDir + '\\day.txt')

'''
1. get viewposition from Unreal Engine
'''
positionSit, positionStand = UEIO.getViewPositionFromUE(DirUsr.inputDataDir +'\\position.txt')
#debug
header = ['x', 'y', 'z']
data = [positionSit]
filePath = DirUsr.outputDataDir + '\\correctPosition.csv'
pyDataIO.saveToCSV(header, data, filePath)

'''
2. set up view file (.VF)
'''
view1 = viewHB.customizedView('', positionSit, (1,0,0), (0,0,1), 'h', 180, 180)
view2 = viewHB.customizedView('', positionSit, (-1,0,0), (0,0,1), 'h', 180, 180)
viewFileName1 = strUtil.viewCreation('vectorX')
viewFileName2 = strUtil.viewCreation('vectorNegX')
viewFilePath1 = viewHB.outputPath(view1, DirUsr.modelForSimDir, viewFileName1, False)
viewFilePath2 = viewHB.outputPath(view2, DirUsr.modelForSimDir, viewFileName2, False)
print(viewFileName1, viewFileName2)

'''
3. set up sky file (.sky)
    para1: CIE Sky Type.

    0 = Sunny with sun.
    1 = Sunny without sun.
    2 = Intermediate with sun. 
    3 = Intermediate without sun. 
    4 = Cloudy sky.
    5 = Uniform cloudy sky. 
'''
skyFileName = strUtil.dateCreation(month, day, hour) + '.sky' 
cieSky = sky.createCIESky(epwFile, month, day, hour, 0) #refer to para1
skyFilePath = sky.outputPath(cieSky, DirUsr.modelForSimDir,skyFileName)
print('sky file path: ', skyFilePath)

# FOR DEBUGGING
# skyString = sky.outputString(cieSky)
# print('gensky: ', skyString)


'''
4. create octree files
'''
winMatDir = DirUsr.windowMatDir
winRadDir = DirUsr.windowRadDir
sceneMatDir = DirUsr.sceneMatDir
sceneRadDir = DirUsr.sceneRadDir

radFilePath = winMatDir + " " + sceneMatDir + " " + winRadDir + " " + sceneRadDir
octFileName = 'scene.oct'
transRad.radToOctree(radFilePath, DirUsr.modelForSimDir, octFileName)

'''
5. add sky data to octree file
'''
octFilePath = DirUsr.modelForSimDir + '\\' + octFileName
newOctFileName, newOctFilePath = transRad.addOctreeInstance(octFilePath, skyFilePath, skyFileName, DirUsr.modelForSimDir, DirUsr.modelForSimDir)

'''
6. acceleRpict simulation
'''
hdrFileName1 = fastRender.AccRpict(viewFilePath1, viewFileName1, newOctFilePath, newOctFileName, radPara, DirUsr.modelForSimDir, DirUsr.hdrDir)
hdrFileName2 = fastRender.AccRpict(viewFilePath2, viewFileName2, newOctFilePath, newOctFileName, radPara, DirUsr.modelForSimDir, DirUsr.hdrDir)

'''
7. postprocessing
'''
hdrFilePath1 = DirUsr.hdrDir + '\\' + hdrFileName1 + '.hdr'
hdrFilePath2 = DirUsr.hdrDir + '\\' + hdrFileName2 + '.hdr'
fcImgName1, fcImgPath1 = postprocess.createFalseColorImg(hdrFileName1, hdrFilePath1, DirUsr.hdrDir, DirUsr.radianceEngineBinPath, 2000, 10)
fcImgName2, fcImgPath2 = postprocess.createFalseColorImg(hdrFileName2, hdrFilePath2, DirUsr.hdrDir, DirUsr.radianceEngineBinPath, 2000, 10)
'''
8. convert and resize to jpg format
# this command uses ImageMagick
'''
# postprocess.convertHDRToOtherFormat(fcImgPath1 + '.hdr', 'jpg', 2.2, 180, 160)
# postprocess.convertHDRToOtherFormat(fcImgPath2 + '.hdr', 'jpg', 2.2, 180, 160)

postprocess.convertHDRToOtherFormat(fcImgPath1 + '.hdr', 'jpg', 2.2)
postprocess.convertHDRToOtherFormat(fcImgPath2 + '.hdr', 'jpg', 2.2)
pyDataIO.writeToNewFile(fcImgPath1+'.jpg', DirUsr.hdrDir + '\\imageNameX.txt')
pyDataIO.writeToNewFile(fcImgPath2+'.jpg', DirUsr.hdrDir + '\\imageNameNX.txt')

'''
9. use evalglare to find DGP value
'''
glareTextFile1 = DirUsr.hdrDir + '\\glareX.txt'
glareTextFile2 = DirUsr.hdrDir + '\\glareNX.txt'
radGlare.runEvalGlare(hdrFilePath1, glareTextFile1, DirUsr.radianceEngineBinPath)
radGlare.runEvalGlare(hdrFilePath2, glareTextFile2, DirUsr.radianceEngineBinPath)

'''
10. find value from evalglare file
'''
dgpVal1, EvVal1 = evalglareParse.analyseMetricsData(glareTextFile1, ['dgp', 'E_v'])
dgpVal2, EvVal2 = evalglareParse.analyseMetricsData(glareTextFile2, ['dgp', 'E_v'])

dgpFilePath1 = DirUsr.hdrDir + '\\dgpVal1.txt'
EvFilePath1 = DirUsr.hdrDir + '\\evVal1.txt'
dgpFilePath2 = DirUsr.hdrDir + '\\dgpVal2.txt'
EvFilePath2 = DirUsr.hdrDir + '\\evVal2.txt'

pyDataIO.writeToNewFile(str(dgpVal1), dgpFilePath1)
pyDataIO.writeToNewFile(str(EvVal1), EvFilePath1)
pyDataIO.writeToNewFile(str(dgpVal1), dgpFilePath2)
pyDataIO.writeToNewFile(str(EvVal1), EvFilePath2)

dgpPath1 = DirUsr.hdrDir + '\\dgpPath1.txt'
evPath1 = DirUsr.hdrDir + '\\evPath1.txt'
dgpPath2 = DirUsr.hdrDir + '\\dgpPath2.txt'
evPath2 = DirUsr.hdrDir + '\\evPath2.txt'
pyDataIO.writeToNewFile(dgpFilePath1, dgpPath1)
pyDataIO.writeToNewFile(EvFilePath1, evPath1)
pyDataIO.writeToNewFile(dgpFilePath2, dgpPath2)
pyDataIO.writeToNewFile(EvFilePath2, evPath2)



