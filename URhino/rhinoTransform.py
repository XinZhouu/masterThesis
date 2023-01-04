import clr
clr.AddReferenceByName("RhinoCommon")

import Rhino.Geometry as rg
import rhinoscriptsyntax as rs

class rhTrans:
    
    @staticmethod
    def moveObj(GUID_obj, translation):
        rs.MoveObject(GUID_obj, translation)