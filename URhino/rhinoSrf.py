import clr
clr.AddReferenceByName("RhinoCommon")

import Rhino.Geometry as rg
import rhinoscriptsyntax as rs


class rhSrfPrimitive:
    
    @staticmethod
    def getBoundingBox(arrayStrObject):
        bBox = arrayStrObject.GetBoundingBox(True)
        return bBox
    
    @staticmethod
    def explodeMesh(GUI_obj):
        meshes = rs.ExplodeMeshes(GUI_obj)
        return meshes
    
    