######################################################
# this script needs to connect to Rhino
######################################################
import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
import scriptcontext as sc


from UTool.dirLocation import DirUsr
from UTool.dataIO import pyDataIO

from URhino.rhinoModelCtl import rhModel
from URhino.rhinoData import rhTransData
from URhino.rhinoVis import rhCanvas, rhVis
from URhino.rhinoCurve import rhCurve
from URhino.rhinoLayerCtl import rhLayer
from URhino.rhinoSrf import rhSrfPrimitive
from URhino.rhinoTransform import rhTrans
from URhino.rhinoMesh import rhMeshEdit

from USimEngine.UHoneybee.hbView import *
from USimEngine.UHoneybee.hbAssign import *
from USimEngine.UHoneybee.hbSky import *
from USimEngine.UHoneybee.hbGrid import hbGrid
from USimEngine.UHoneybee.transGeo import HBGeo
from USimEngine.UHoneybee.hbAssign import hbAssign
from USimEngine.UHoneybee.hbEpw import epw
from USimEngine.UHoneybee.hbRecipe import battery
from USimEngine.UHoneybee.hbSDA import sDA
from USimEngine.UHoneybee.hbVis import hbVis

import ladybug_geometry.geometry3d.pointvector

class rhinoOutput:
    
    @staticmethod
    def rhinoModelPrep():
        #######################################################
        # parameters
        #######################################################
        '''
        general parameters
        '''
        daylightParentLayer = "Daylight Model"
        north = 0 # positive Y axis

        addGridPointLayer = "GRIDPTS"
        addGridSquareLayer = "GRIDMAP"
        sDAHeatmap = "sDAHeatmap"
        DAHeatmap = "DAHeatmap"
        cDAHeatmap = "cDAHeatmap"
        UDILowHeatmap = "UDILHeatmap"
        UDIMiddleHeatmap = "UDIMHeatmap"
        UDIHighHeatmap = "UDIHHeatmap"
        '''
        parameters for sDA
        '''
        gridSize = 0.5
        offsetDistance = 1.2
        targetTime = 50
        #######################################################
        # MODEL PREPARATION
        #######################################################
        '''
        1.get rhino models from layers
        '''
        objsDic = rhModel.extractRhinoModelsFromLayers(daylightParentLayer)
        #print(objsDic)

        '''
        2.transfer rhino model to honeybee model
        '''
        walModLst = HBGeo.HBSurface(objsDic, '', None, None, 'PARTITION')
        flrModLst = HBGeo.HBSurface(objsDic, '', None, None, 'FLOOR')
        ceilModLst = HBGeo.HBSurface(objsDic, '', None, None, 'CEILING')
        colModLst = HBGeo.HBSurface(objsDic, '', None, None, 'COLUMN')
        mulModLst = HBGeo.HBSurface(objsDic, '', None, None, 'MULLION')
        shadeModLst = HBGeo.HBSurface(objsDic, '', None, None, 'SHADE')
        winModLst = HBGeo.HBWindow(objsDic, '', True)

        allObjLst = walModLst + flrModLst + ceilModLst + colModLst + mulModLst + shadeModLst
        HBModel = HBGeo.modelForSim(allObjLst, winModLst, '')
        #print(HBModel)
        ################################################################################
        # DA MODEL PREP
        ################################################################################
        '''
        3. sampling data for matrix based simulation
        '''
        samplingArea = objsDic['GRIDS'][0]# this is a GUID object
        samplingObj = rhTransData.GUIDToBrep(samplingArea)# transfer GUID to Brep object
        sampleData = hbGrid.generateSensorGrid(samplingObj, gridSize, offsetDistance, ladybugMesh = True)

        'extract sampling data'
        samplePts = sampleData[0] # list
        sampleDirections = sampleData[1]
        sampleMeshes = sampleData[3] # class mesh object in a list
        sampleMesh = sampleMeshes[0]
        print('sampleMesh', sampleMesh)

        'adding layers'
        rhLayer.addLayer(addGridPointLayer, daylightParentLayer)
        rhLayer.addLayer(addGridSquareLayer, daylightParentLayer)
        rhLayer.addLayer(sDAHeatmap, daylightParentLayer)
        rhLayer.addLayer(DAHeatmap, daylightParentLayer)
        rhLayer.addLayer(cDAHeatmap, daylightParentLayer)
        rhLayer.addLayer(UDILowHeatmap, daylightParentLayer)
        rhLayer.addLayer(UDIMiddleHeatmap, daylightParentLayer)
        rhLayer.addLayer(UDIHighHeatmap, daylightParentLayer)

        # 'visualize sensor points'
        rhCanvas.enableRedraw()
        GUID_SamplePoints = rhVis.points(samplePts) # add to display
        rhLayer.addObjToLayer(GUID_SamplePoints, addGridPointLayer) # add them to the layer

        # 'visualize heatmaps'
        # for pt in samplePts:
        #     samplePolyline = rhCurve.squareFromCenter(pt, gridSize)
        #     GUID_samplePolyline = rhVis.polyline(samplePolyline)
        #     GUID_sampleSrf = rhVis.planarSrf(GUID_samplePolyline)
        #     rhLayer.addObjToLayer(GUID_sampleSrf, addGridSquareLayer)
        #     rhVis.deleteObjects(GUID_samplePolyline) # delete lines

        'visualize sample heatmaps'
        GUID_sampleMesh = sc.doc.ActiveDoc.Objects.Add(sampleMesh)
        rhTrans.moveObj(GUID_sampleMesh, [0,0,-1])
        RG_sampleMesh = rhTransData.GUIDToMesh_RG(GUID_sampleMesh)
        GUID_subdivedSampleMesh = rhMeshEdit.explodeOpenMesh(RG_sampleMesh)
        rhLayer.addObjToLayer(GUID_subdivedSampleMesh, addGridSquareLayer)
        rhVis.deleteObjects(GUID_sampleMesh) # delete lines

        '''
        4. sampling area from rhino to honeybee object
        '''
        # hbGrid is a class object
        ClassOBJ_hbGrid = hbGrid.HBSensorGrid(None, samplePts, sampleDirections, sampleMesh, samplingObj)
        # # get point tuple (location + direction)
        # hbGrid = hbGrid.sensors
        # # transfer tuple to list
        # hbGrid = list(ClassOBJ_hbGrid)
        hbModelWithGrid = hbAssign.viewOrGridToModel(HBModel, None, ClassOBJ_hbGrid)

        '''
        5. sampling area from rhino to honeybee object
        '''
        wea = epw.epwToWea(DirUsr.epwPath, None, '')

        '''
        6. simulation initial run for DA, cDA, UDI
        '''
        result = battery.annualDaylight(hbModelWithGrid, wea, north, '', None, '', '', True)

        resultPath = result[0]
        rawDataPathLst = result[1] # ['ill, sunhour.txt]
        DAMetric = result[2][0]
        cDAMetric = result[3][0]
        UDIMMetric = result[4][0]
        UDILMetric = result[5][0]
        UDIUMetric = result[6][0]

        ghLst = result[7] # [ghResults, ghDA, ghCDA, ghUDI, ghUDILOW, ghUDIUP]
        ghDA = ghLst[1] # this is a tree: tree {440}


        '''
        7. simulation initial run for sDA
        '''
        passTree, passLst, sDAVal = sDA.simulateSDA(ghDA, targetTime, sampleMeshes)
        sDAValue = sDAVal[0]
        SDAMetric = passLst[0]

        '''
        8.initial heatmaps for DA, cDA, UDI, sDA
        '''
        metricsCollectionDic = {sDAHeatmap: SDAMetric, 
                                DAHeatmap: DAMetric, 
                                cDAHeatmap: cDAMetric,
                                UDILowHeatmap: UDILMetric,
                                UDIMiddleHeatmap: UDIMMetric,
                                UDIHighHeatmap: UDIUMetric
                                }

        sampleAreaPtLst = []
        for metric in metricsCollectionDic:
            RG_Mesh, legend, colors, legendPara, colorLst, samplePtMin, samplePtMax = hbVis.spatialHeatMap(metricsCollectionDic[metric], sampleMesh, [0, 0], None, '%', None)
            GUID_Mesh = sc.doc.ActiveDoc.Objects.Add(RG_Mesh)
            rhTrans.moveObj(GUID_Mesh, [0,0,-1])
            rhLayer.addObjToLayer(GUID_Mesh, metric)
            
            sampleAreaPtLst[:] = [] # empty the list
            sampleAreaPtLst.append(samplePtMin)
            sampleAreaPtLst.append(samplePtMax)
        
        #output sample area min and max points to the file
        sampleArealadybugToVectorLst = []
        for point in sampleAreaPtLst:
            str_vector = point.ToString()
            sampleArealadybugToVectorLst.append(str_vector)
        
        sampleAreaPtLstFileName = DirUsr.modelWithGridDir + '\\gridMinMax.txt'
        sampleAreaPtString = ' '.join(sampleArealadybugToVectorLst)
        pyDataIO.writeToNewFile(sampleAreaPtString, sampleAreaPtLstFileName)
        
        #change the result folder to the target folder
        pyDataIO.changeAllInDirToAnother(resultPath, DirUsr.modelWithGridDir)
        ################################################################################
        # radiance renderer prep
        ################################################################################
        # '''
        # 5.export honeybee model
        # '''
        # # export the honeybee model
        # HBGeo.GeoRhinoToRad(HBModel, DirUsr.modelWithGridDir)
        
        
        
########################################################
rhinoOutput.rhinoModelPrep()

