import rhinoscriptsyntax as rs
import Rhino

class rhLayer:
    
    @staticmethod
    def addLayer(layerName, parentLayerName):
        rs.AddLayer(layerName, parent = parentLayerName)
        
    @staticmethod
    def addObjToLayer(obj, layerName):
        rs.ObjectLayer(obj, layerName)