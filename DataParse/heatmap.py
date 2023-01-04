import csv

############################################################
class heatmapParse:
    
    @staticmethod
    def colorsToCSV(colorLst, filePath):
        with open(filePath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # write multiple rows
            for color in colorLst:
                writer.writerow(color)
        f.close()