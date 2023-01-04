import csv
import os
import shutil

###################################################
class pyDataIO:
    #data is a 2D list
    @staticmethod
    def saveToCSV(header, data, filePath):
        with open(filePath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # write the header
            if header != None:
                writer.writerow(header)

            # write multiple rows
            writer.writerows(data)
            
    @staticmethod
    def writeToNewFile(file, targetFilePath):
        with open(targetFilePath, 'w') as f:
            f.write(file)
            f.close()
            
            
    @staticmethod
    def changeAllInDirToAnother(sourcePath, destinationPath):
        allFiles = os.listdir(sourcePath)
        
        for f in allFiles:
            srcPath = os.path.join(sourcePath, f)
            dstPath = os.path.join(destinationPath, f)
            shutil.move(srcPath, dstPath)
            
            
    @staticmethod
    def readSimpleFile(filePath):
        with open(filePath, 'r') as f:
            lines = f.readlines()
            lines = [line.replace('\n', '') for line in lines]
        return lines   
    
    @staticmethod
    def readDayFile(filePath):
        with open(filePath, 'r') as f:
            line = f.readline()
            dayLst = line.split(',')
            month = int(dayLst[0])
            day = int(dayLst[1])
            hour = int(dayLst[2])
        return month, day, hour
    
    
    
class sysDataIO:
    # check if a folder has files already
    @staticmethod
    def checkFolderHaveFiles(folder):
        if os.listdir(folder) != []:
            print(f'{folder} has existing files')
            return True
    
    @staticmethod
    # delete the files in a folder
    def delFilesInFolder(folder):
        for file in os.scandir(folder):
            os.remove(file.path)
            print(f'already remove all the files in {folder}.')
            
        
        