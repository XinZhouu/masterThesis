import rhinoscriptsyntax as rs

class plane:
    
    # attributes
    planeXY = rs.WorldXYPlane()

class pt(plane):
    
    @staticmethod
    def deconstructPt(pt):
        return (pt.X, pt.Y, pt.Z)
    
    @staticmethod
    def constructPt(tuple):
        pt = rs.CreatePoint(tuple[0], tuple[1], tuple[2])
        return pt
    
class rhTransData:
    
    @staticmethod
    def GUIDToBrep(GUID):
        object = rs.coercebrep(GUID)
        return object
    
    @staticmethod
    def GUIDToMesh_RG(GUID_mesh):
        RG_mesh = rs.coercemesh(GUID_mesh)
        return RG_mesh