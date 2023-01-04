import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')

from UTool.dirLocation import DirUsr

#####################################################
class UEIO:
    
    @staticmethod
    def getViewPositionFromUE(filePath):
        with open(filePath) as f:
            lines = f.read()
            lines = lines.split(" ")
            
            positionVector = []
            
            for line in lines:
                index = line.find("=")
                valueStr = line[index+1:]
                value = float(valueStr)
                positionVector.append(value)
                

            #change from cm to m
            #change -y to +y
            xAxis = positionVector[0] / 100
            yAxis = abs(positionVector[1]) / 100
            zAxisSit = 1.2
            zAxisStand = 1.5
            
            finalPositionVectorSit = [xAxis, yAxis, zAxisSit]
            finalPositionVectorStand = [xAxis, yAxis, zAxisStand]
            
            f.close()
            
            return finalPositionVectorSit, finalPositionVectorStand
    

    

    