import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
from UTool.dataIO import pyDataIO
from UTool.dataCtl import strUtil

class runtimeSim:
    
    @staticmethod
    def simulateSDARuntime(DAPath, targetTime):

        rawData = pyDataIO.readSimpleFile(DAPath)
        updatedData = strUtil.batchFromStrToFloat(rawData)

        # determine whether each point passes or fails
        pass_fail = [int(val > targetTime) for val in updatedData]

        # compute spatial daylight autonomy from the pass/fail results
        sDA = format(sum(pass_fail) / len(pass_fail), '.3f')
        # else:  # weight the sensors based on the area of mesh faces
        #     sDA = []
        #     for i, mesh in enumerate(lb_meshes):
        #         m_area = mesh.area
        #         weights = [fa / m_area for fa in mesh.face_areas]
        #         sDA.append(sum(v * w for v, w in zip(pass_fail[i], weights)))
        return pass_fail, sDA

