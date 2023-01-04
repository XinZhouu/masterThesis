import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
import os
import subprocess

from UTool.dataCtl import strUtil
from UTool.dirLocation import DirUsr
###########################################################
class transRad:
    
    @staticmethod
    def radToOctree(radFilePath, currentDir, fileName):       
        cmd = 'oconv ' + radFilePath + ' > ' + fileName
        print('rad -> .oct: ', cmd)
        subprocess.call(cmd,
                        shell = True,
                        executable = DirUsr.CMD,
                        cwd = currentDir)
        
    @staticmethod
    def addOctreeInstance(octFile, skyFile, skyName, currentDir, octFolder):
        name = strUtil.extractTargetStrLayer(skyName, '.', 1, 'left')
        newOctFileName = name + '.oct'
        newOctFilePath = octFolder + '\\' + newOctFileName
        cmd = (
                'oconv -i' +
                ' ' + octFile +
                ' ' + skyFile +
                ' > ' + newOctFilePath
        )
        
        print('.oct + sky -> .oct: ', cmd)
        subprocess.call(cmd,
                        shell = True,
                        executable = DirUsr.CMD,
                        cwd = currentDir)
        
        return newOctFileName, newOctFilePath

class radGlare:
    @staticmethod
    def runEvalGlare(filePath, outPath, radianceAppFolder):
        cmd = ('evalglare -d ' + filePath + ' > ' + outPath)
        subprocess.call(cmd,
                        shell = True,
                        executable = DirUsr.CMD,
                        cwd = radianceAppFolder)

class postprocess:
    @staticmethod
    def createBarCommand(maxScale, interval):
        maxScaleVal = ' -s ' + str(maxScale)
        numInterval = ' -n ' + str(interval)
        bar = maxScaleVal + numInterval
        return bar
    
    @staticmethod
    def createFalseColorImg(hdrFileName, hdrFilePath, hdrFileDir, exeFilePath, maxScale, interval):
        newImgName = 'fc_' + hdrFileName
        newImgPath = hdrFileDir + '\\' + newImgName
        bar = postprocess.createBarCommand(maxScale, interval)

        cmd = 'falsecolor -ip ' + hdrFilePath + bar + ' > ' + newImgPath + '.hdr'
        print('falColr command: ', cmd)

        subprocess.call(cmd,
                        shell = True,
                        executable = DirUsr.CMD,
                        cwd = exeFilePath)	
        return newImgName, newImgPath

    @staticmethod
    def createContourLineImg(hdrFileName, hdrFilePath, hdrFileDir, maxScale, interval):
        # access variables in createFalsecolorImg()
        newImgName = 'fcContour_' + hdrFileName
        newImgPath = hdrFileDir + '\\' + newImgName
        bar = postprocess.createBarCommand(maxScale, interval)
        
        # illuminance map
        cmd = ('falsecolor -i ' + hdrFilePath + 
               ' -p ' + hdrFilePath + 
               ' -cl ' + bar + ' > ' + newImgPath + '.hdr')
                
        print('falColrContour_command: ', cmd)           

        subprocess.call(cmd,
                        shell = True,
                        executable = DirUsr.CMD,
                        cwd = hdrFileDir)
        
        
    # @staticmethod
    # def convertHDRToOtherFormat(hdrFilePath, targetFormat, gammaVal, resizeX, resizeY):
        
    #     cmd = ('magick mogrify' +
    #             ' -format ' + targetFormat +
    #             ' -gamma ' + str(gammaVal) +
    #             ' -resize ' + str(resizeX) + 'x' + str(resizeY) +
    #             ' ' + hdrFilePath
    #             )
        
    #     print('convert image:', cmd)
        
    #     subprocess.call(cmd,
    #                     shell = True,
    #                     executable = DirUsr.CMD)     
    
    @staticmethod
    def convertHDRToOtherFormat(hdrFilePath, targetFormat, gammaVal):
        
        cmd = ('magick mogrify' +
                ' -format ' + targetFormat +
                ' -gamma ' + str(gammaVal) +
                ' ' + hdrFilePath
                )
        
        print('convert image:', cmd)
        
        subprocess.call(cmd,
                        shell = True,
                        executable = DirUsr.CMD)    
        