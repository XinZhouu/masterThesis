import rhinoscriptsyntax as rs
import scriptcontext
import System


class rhMeshEdit:
    
    @staticmethod
    def explodeOpenMesh(RG_mesh):
        RG_mesh.Unweld(0, True)
        RG_subMeshes = RG_mesh.ExplodeAtUnweldedEdges()

        rc = []
        for submesh in RG_subMeshes:
            id = scriptcontext.doc.Objects.AddMesh(submesh)
            if id!=System.Guid.Empty: rc.append(id)
            
        if rc: scriptcontext.doc.Views.Redraw()
        return rc