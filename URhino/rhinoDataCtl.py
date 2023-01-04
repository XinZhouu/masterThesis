import clr
clr.AddReferenceByName("Grasshopper")
# clr.AddReferenceByName("GhPython")
clr.AddReferenceByName("RhinoCommon")
clr.AddReferenceToFileAndPath("C:\\Program Files\\Rhino 7\\Plug-ins\\Grasshopper\\Components\\GhPython.gha")

import rhinoscriptsyntax as rs
import ghpythonlib.components as gh
import Rhino.Geometry as rg



class rhDataCtl:
    
    @staticmethod
    def duplicateDataToList(value, num):
        lst = gh.DuplicateData(value, num, True)
        return lst