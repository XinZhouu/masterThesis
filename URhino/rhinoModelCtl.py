import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
from rhinoCtl import rhCTL
from UTool.dataCtl import strUtil
#############################################################
class rhModel:
    
    @staticmethod
    def extractRhinoModelsFromLayers(rhinoLayer):
        # get objects in each layer that is on
        rhCTL.objByLayers(rhinoLayer)
        objDic = rhCTL.dic

        # parsing objDic
        newObjDic = dict()
        for key in objDic:
            layerName = strUtil.extractTargetStrLayer(key, ':', 2, 'right')
            if layerName not in newObjDic:
                newObjDic[layerName] = objDic[key]
                
        return newObjDic