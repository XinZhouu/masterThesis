import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
from UTool.UMath import mathUsr
import subprocess
import os

class strUtil:
    
    @staticmethod
    def batchFromStrToFloat(lst):
        newLst = []
        for string in lst:
            num = float(string)
            num = mathUsr.roundHalfUp(num)
            newLst.append(num)
        return newLst
            
    
    @staticmethod
    # general
    # source code:
    # https://stackoverflow.com/questions/21199943/index-of-second-repeated-character-in-a-string
    def getIndex(str, targetStr, iteration):
        current = -1
        for i in range(iteration):
            current = str.index(targetStr, current + 1)
        else:
            ValueError("ordinal {} - is invalid".format(iteration))
        return current
    
    # specific to the rhino layer
    @staticmethod
    def extractTargetStrLayer(str, targetStr, iteration, direction):
        i = strUtil.getIndex(str, targetStr, iteration)
        if direction == 'left':
            layerName = str[:i]
        else:
            layerName = str[i+1:]
        return layerName
    
    # specific to the format of date construction Month/Day/Time
    @staticmethod
    def dateCreation(month, day, time):
        updatedStr = str(month) + '_' + str(day) + '_' + str(time)
        return updatedStr
    
    @staticmethod
    def viewCreation(viewDirStr):
        updatedStr = 'view' + '_' + viewDirStr
        return updatedStr
    
        
    
    
#     # Brute Force method
#     @staticmethod
#     def organizeObjFolder(objFolder):
#         path1 = 'C:\\Users\\zxin1\\Desktop\\research\\HB\\file\\objData\\model\\aperture'
#         material1 = path1 +'\\aperture.mad'
#         obj1 = path1 + '\\aperture.rad'
#         path2 = 'C:\\Users\\zxin1\\Desktop\\research\\HB\\file\\objData\\model\\scene'
#         material2 = path2 +'\\envelope.mad'
#         obj2 = path2 + '\\envelope.rad'
#         print(path1,material1, obj1, path2, material2, obj2)
#         for item in [material1, obj1]:
#             cmd = (
#                     'move' +
#                     ' ' + item +
#                     ' ' + objFolder
#                     )
            
#             subprocess.call(cmd,
#                             shell = True,
#                             executable = dir.CMD,
#                             cwd = path1)
            
#         for item in [material2, obj2]:
#             cmd = (
#                     'move' +
#                     ' ' + item +
#                     ' ' + objFolder
#                     )
            
#             subprocess.call(cmd,
#                             shell = True,
#                             executable = dir.CMD,
#                             cwd = path2)
        
    
    # # specific to solve objFolder issues
    # @staticmethod
    # def navigateDir(rtDir):
    #     lst = []
    #     sysDir.navigateDirHelper(rtDir, lst)
        
    # def navigateDirHelper(rtDir, lst):
    #     for dir in rtDir:
    #         if os.path.isfile(dir):
    #             if 'envelope.mat' or 'envelope.rad' or 'aperture.mat' or \
    #             'aperture.rad' in dir:           
    #                 lst.append(dir)
    #         else:
    #             newPath = os.path.join(rtDir, dir)
    #             sysDir.navigateDir(newPath, lst)    
            