import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
from UTool.dirLocation import DirUsr
##############################################################
class combRad:
    
    @staticmethod
    def combineAllRadFiles():
        winMatDir = DirUsr.windowMatDir
        winRadDir = DirUsr.windowRadDir
        sceneMatDir = DirUsr.sceneMatDir
        sceneRadDir = DirUsr.sceneRadDir
        radFileName = "scene.rad"
        combRadDir = DirUsr.modelForSimDir + '\\' + radFileName
        
        file1 = open(winMatDir, "r")
        content1 = file1.read()
        file1.close()

        newFile = open(combRadDir, "w")
        newFile.write(content1 + "\n" + "\n")
        newFile.close()
        
        file2 = open(sceneMatDir, "r")
        content2 = file2.read()
        file2.close()
        
        newFile = open(combRadDir, "a")
        newFile.write(content2 + "\n" + "\n") 
        newFile.close()   
        
        file3 = open(winRadDir, "r")
        content3 = file3.read()
        file3.close() 
        
        newFile = open(combRadDir, "a")
        newFile.write(content3 + "\n" + "\n") 
        newFile.close()  

        file4 = open(sceneRadDir, "r")
        content4 = file4.read()
        file4.close() 
        
        newFile = open(combRadDir, "a")
        newFile.write(content4) 
        newFile.close()  
        
        return combRadDir      
                   
