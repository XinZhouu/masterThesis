import rhinoscriptsyntax as rs
import Rhino

#########################################################

# this class use rhinocommon to control rhino
class rhCTL:
    
    # initiate an empty dic
    dic = dict()
    
    @staticmethod
    def objByLayers(layerName):

        names = rs.LayerNames()
        # find the parent layer
        if layerName in names:
            # set this layer to be the current layer
            rs.CurrentLayer(layerName)
            
            # check if this layer is the parent layer
            parent = rs.ParentLayer(layerName)
            if parent == None: # meaning there is no parent
        
                # loop through sublayers
                childLst = rs.LayerChildren(layerName)
                #print('child layer list: ', childLst)
                
                rhCTL.findObjects(childLst)
    
    @staticmethod
    # do this iteratively
    def findObjects(lst): 
          
        for layer in lst:
            # filter the layers that are not on
            if rs.IsLayerOn(layer):
                
                # check if every sublayer has children
                childSubLst = rs.LayerChildren(layer)
                
                if len(childSubLst) == 0: # no children
                    
                    # find objs included in this layer
                    objList = rs.ObjectsByLayer(layer)
                    
                    # write it into the dic
                    if layer not in rhCTL.dic:
                        rhCTL.dic[layer] = objList
                    
                    
    @staticmethod
    def getViewPosition():
        viewPoint = rs.GetPoint('view point')
        return viewPoint

class rhAnys():
    
    @staticmethod
    def reconstructViewPoint(unit, vector3D):
        if unit == 'Meters':
            z = 1.2192
        elif unit == 'Millimeters':
            z = 1219.2
        elif unit == 'Feet':
            z = 4
        newPt = rs.CreatePoint(vector3D[0], vector3D[1], z)
        return newPt

# rhino visualization: show results to the active rhino window
#class rhVis():
           

class rhUtil():
    
    # check current unit system on canvas
    @staticmethod
    def identifyModelUnit():
        unit = Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem.ToString()
        return unit

    
