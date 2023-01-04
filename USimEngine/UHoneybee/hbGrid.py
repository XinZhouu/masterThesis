from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.mesh import Mesh3D
from ladybug_rhino.togeometry import to_gridded_mesh3d, to_mesh3d, to_face3d, to_vector3d
from ladybug_rhino.fromgeometry import from_mesh3d, from_point3d, from_vector3d
from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D
from ladybug_rhino.config import conversion_to_meters

from honeybee.typing import clean_and_id_rad_string, clean_rad_string
from honeybee_radiance.sensorgrid import SensorGrid

################################################################################
# CODE SOURCE: 
'''
The following codes are MODIFIED from
orginial official codes in LADYBUG TOOLS: https://github.com/ladybug-tools

The official link above has several respositories, which have open SDKS:
https://discourse.ladybug.tools/pub/ladybug-tools-core-sdk-documentation

Modifications:
1, The script simplifies some of the steps to tailor to the project.
2, The script shortens some of the input parameters.
3, The script paraphrases some of the python syntax to make it more 
   clear and understandable to myself.
4, The script attempts to use CLASS to better control and classify each function.
'''
################################################################################


class hbGrid:
    
    @staticmethod
    def generateSensorGrid(samplingArea, gridSize, offsetDistance, ladybugMesh):
        # check the input and generate the mesh.
        offsetDistance = offsetDistance or 0
        if ladybugMesh:  # use Ladybug's built-in meshing methods
            lbFaces = to_face3d(samplingArea)
            try:
                xAxis = to_vector3d(ladybugMesh)
                lbFaces = [Face3D(f.boundary, Plane(f.normal, f[0], xAxis), f.holes)
                            for f in lbFaces]
            except AttributeError:
                pass  # no plane connected; juse use default orientation
            lbMeshes = []
            for geo in lbFaces:
                try:
                    lbMeshes.append(geo.mesh_grid(gridSize, offset=offsetDistance))
                except AssertionError:  # tiny geometry not compatible with quad faces
                    continue
            if len(lbMeshes) == 0:
                lbMesh = None
            elif len(lbMeshes) == 1:
                lbMesh = lbMeshes[0]
            elif len(lbMeshes) > 1:
                lbMesh = Mesh3D.join_meshes(lbMeshes)
        
        # generate the test points, vectors, and areas.
        if lbMesh is not None:
            points = [from_point3d(pt) for pt in lbMesh.face_centroids]
            vectors = [from_vector3d(vec) for vec in lbMesh.face_normals]
            faceAreas = lbMesh.face_areas
            mesh = [from_mesh3d(lbMesh)]
        else:
            mesh = []    
        
        return points, vectors, faceAreas, mesh  
    
    @staticmethod
    def HBSensorGrid(gridName, samplePoints, pointDirections, meshes, baseArea):
        # set the default name and process the points to tuples
        name = clean_and_id_rad_string('SensorGrid') if gridName is None else gridName
        pts = [(pt.X, pt.Y, pt.Z) for pt in samplePoints]

        # create the sensor grid object
        id  = clean_rad_string(name) if '/' not in name else clean_rad_string(name.split('/')[0])
        if len(pointDirections) == 0:
            grid = SensorGrid.from_planar_positions(id, pts, (0, 0, 1))
        else:
            vecs = [(vec.X, vec.Y, vec.Z) for vec in pointDirections]
            # get all the grids with points and directions
            grid = SensorGrid.from_position_and_direction(id, pts, vecs)

        #set the display name
        if gridName is not None:
            grid.display_name = gridName
        if '/' in name:
            grid.group_identifier = \
                '/'.join(clean_rad_string(key) for key in name.split('/')[1:])
        if meshes is not None:
            grid.mesh = to_mesh3d(meshes)
            
        if baseArea is not None:
            grid.base_geometry = to_face3d(baseArea)
            
        return grid
    
    # this function is for annual glare simulation
    @staticmethod
    def HBRadialGrid(gridName, samplePts, viewDirectionsCounts, viewStartVector, meshRadius):
        # set the default name and process the points to tuples
        name = clean_and_id_rad_string('SensorGrid') if gridName is None else gridName
        pts = [(pt.X, pt.Y, pt.Z) for pt in samplePts]
        dir_count = 8 if viewDirectionsCounts is None else viewDirectionsCounts
        mesh_radius = 0.2 / conversion_to_meters() if meshRadius is None else meshRadius
        try:
            st_vec = to_vector3d(viewStartVector)
        except AttributeError:
            st_vec = Vector3D(0, -1, 0)

        # create the sensor grid object
        id  = clean_rad_string(name) if '/' not in name else clean_rad_string(name.split('/')[0])
        grid = SensorGrid.from_positions_radial(
            id, pts, dir_count, start_vector=st_vec, mesh_radius=mesh_radius)

        # set the display name and get outputs
        if gridName is not None:
            grid.display_name = gridName
        if '/' in name:
            grid.group_identifier = \
                '/'.join(clean_rad_string(key) for key in name.split('/')[1:])
        sensors = grid.sensors
        points = [from_point3d(Point3D(*sen.pos)) for sen in sensors]
        vecs = [from_vector3d(Vector3D(*sen.dir)) for sen in sensors]
        lb_mesh = grid.mesh
        if lb_mesh is not None:
            mesh = from_mesh3d(lb_mesh)
            
        return grid, sensors, points, vecs, mesh