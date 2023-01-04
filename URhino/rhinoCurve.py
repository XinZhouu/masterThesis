import rhinoscriptsyntax as rs
import Rhino

from rhinoData import pt

class rhCurve:
    
    @staticmethod
    def squareFromCenter(point, size):
        halfSize = size/2
        x, y, z = pt.deconstructPt(point)
        p0 = pt.constructPt((x - halfSize, y + halfSize, z))
        p1 = pt.constructPt((x - halfSize, y - halfSize, z))
        p2 = pt.constructPt((x + halfSize, y - halfSize, z))
        p3 = pt.constructPt((x + halfSize, y + halfSize, z))
        
        polyline = Rhino.Geometry.Polyline([p0, p1, p2, p3, p0])
        return polyline