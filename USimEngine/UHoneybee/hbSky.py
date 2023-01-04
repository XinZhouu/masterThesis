import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
# modules for CIE sky
from USimEngine.UHoneybee.hbEpw import epw
from honeybee_radiance.lightsource.sky.cie import CIE
from UTool.dataCtl import *

# # modules for view.vf
# from honeybee_radiance.view import View
# from ladybug_rhino.togeometry import to_point3d, to_vector3d
# # modules for view based simulation
# from honeybee.model import Model
# from lbt_recipes.recipe import Recipe


#def getEPWFile():
class sky:
    @staticmethod
    def createCIESky(epwFile, month, day, hour, skyTypeNum):
        loc = epw.extractData(epwFile)
        # create CIE sky  
        # return a class instance
        cieSky = CIE.from_location(loc, 
                                    month, day, hour, 
                                    sky_type = skyTypeNum, 
                                    north_angle = 0, 
                                    ground_reflectance = 0.2)
        # debug
        print('honeybee - cieSky: ', cieSky)
        return cieSky
    
    # create a file containing sky info
    @staticmethod
    def outputPath(skyInstance, folder, fileName):
        path = skyInstance.to_file(folder, fileName, False)
        return path
    
    @staticmethod
    def outputString(skyInstance):
        skyString = skyInstance.to_radiance()
        return skyString
        
#######################################################################
# TESTING
####################################################################### 
# epwFile = '.\\file\\weather\\USA_MA_Boston-Logan.Intl.AP.725090_TMY3.epw'
# targetFolder = '.\\file\\weather'
# fileName = ''
# month = 12
# day = 21
# hour = 16
# cieSky = sky.createCIESky(epwFile, month, day, hour)
# skyFilePath = sky.output(cieSky, targetFolder,fileName)

