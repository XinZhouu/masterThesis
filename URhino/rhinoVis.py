import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

class rhCanvas:
    
    @staticmethod
    def enableRedraw():
        'use scriptcontext'
        sc.doc.Views.RedrawEnabled = True
        'use rhinoscriptsyntax'
        # rs.EnableRedraw(True)
        
    @staticmethod
    def disableRedraw():
        'use scriptcontext'
        sc.doc.Views.RedrawEnabled = False      
        
    @staticmethod
    def redraw():
        sc.doc.Views.Redraw()

class rhVis:
    
    @staticmethod
    def points(pointList):
        GUID_pts = rs.AddPoints(pointList)
        rhCanvas.redraw()
        return GUID_pts
        

    @staticmethod
    def polyline(polyline):
        if isinstance(polyline, Rhino.Geometry.Polyline):
            if polyline.IsValid: 
                curve = polyline.ToNurbsCurve()
                GUID_Curves = sc.doc.Objects.AddCurve(curve)
                rhCanvas.redraw()
                return GUID_Curves
            
    @staticmethod
    def planarSrf(curve):
        GUID_srfs = rs.AddPlanarSrf(curve)
        return GUID_srfs
        
    @staticmethod
    def deleteObjects(GUID_objs):
        rs.DeleteObjects(GUID_objs)
        
    @staticmethod
    def deleteObj(GUID_obj):
        rs.DeleteObject(GUID_obj)