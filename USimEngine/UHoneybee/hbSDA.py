from ladybug_rhino.togeometry import to_mesh3d
from ladybug_rhino.grasshopper import list_to_data_tree, data_tree_to_list

class sDA:
    
    @staticmethod
    def simulateSDA(DATree, targetTime, meshObj):
        # process the input values into a rokable format
        da_mtx = [item[-1] for item in data_tree_to_list(DATree)]
        targetTime = 50 if targetTime is None else targetTime
        lb_meshes = [to_mesh3d(mesh) for mesh in meshObj]

        # determine whether each point passes or fails
        pass_fail = [[int(val > targetTime) for val in grid] for grid in da_mtx]

        # compute spatial daylight autonomy from the pass/fail results
        if len(lb_meshes) == 0:  # all sensors represent the same area
            sDA = [sum(pf_list) / len(pf_list) for pf_list in pass_fail]
        else:  # weight the sensors based on the area of mesh faces
            sDA = []
            for i, mesh in enumerate(lb_meshes):
                m_area = mesh.area
                weights = [fa / m_area for fa in mesh.face_areas]
                sDA.append(sum(v * w for v, w in zip(pass_fail[i], weights)))

        passTree = list_to_data_tree(pass_fail)  # convert matrix to data tree
        return passTree, pass_fail, sDA