# modules for HBWindow()
from honeybee.aperture import Aperture

# modules for HBSurface()
from honeybee.face import Face
from honeybee.facetype import _FaceType
from honeybee.boundarycondition import _BoundaryCondition

# modules for modelForSim()
from honeybee.model import Model
from ladybug_rhino.config import units_system

# modules for GeoRhinoToRad(combinedModel)
import os
import re
from ladybug.futil import write_to_file_by_name, nukedir, preparedir
from honeybee.config import Folders
from honeybee_radiance_folder.folder import ModelFolder



# shared modules
from ladybug_rhino.togeometry import to_face3d
from honeybee.typing import clean_string, clean_and_id_string

import rhinoscriptsyntax as rs

#########################################################
# LOG
'''
1. HBWindow():
    _name is default
    _epCon not imple
    _radMod not imple
    
2. HBSurface():
    without user defined type and boundary
    
1. lacking the implemention of HB shade
'''
#########################################################

class HBGeo():
    '''
    name: string
    operable: bool
    opConstruct:
    radModifier:
    '''
    @staticmethod
    def HBWindow(dic, name, operable):
        # list of apertures that will be returned
        for key in dic:
            if key == 'GLAZING': 
                objList = dic[key]
                
                # loop through the objList
                windows = []
                
                for objGUID in objList:
                    
                    # check name
                    if len(name) == 0:
                        # make a default name
                        displayName = clean_and_id_string('Aperture')

                    # transfer objDUID to real obj
                    obj = rs.coercebrep(objGUID)
                    
                    #lbFacesLst format: [Face3D (4 vertices)]
                    lbFacesLst = to_face3d(obj) # obj should be rhino brep,surface or mesh
                    
                    for lbFace in lbFacesLst:
                        #core
                        hbAp = Aperture(displayName, lbFace, is_operable = operable)
                        windows.append(hbAp)
        return windows      
    
    
    '''
    _Facetype:
    1.AirBoundary
    2.Floor
    3.RoofCeiling
    4.Wall
    '''
    @staticmethod
    def HBSurface(dic, name, type, bc, layerName):
       # list of faces that will be returned

        try:
            objList = dic[layerName]
        except:
            print('Cannot find the values to the key {}.'.format(layerName))
                
        # loop through the objList
        faces = []      
        
        for objGUID in objList:
            # check name
            if len(name) == 0:
                # make a default name
                displayName = clean_and_id_string('Face')
            
            obj = rs.coercebrep(objGUID)
            lbFaces = to_face3d(obj)
            
            for lbFace in lbFaces:
                hbFace = Face(displayName, lbFace, type, bc)
                
                faces.append(hbFace)
                
        return faces
    
    @staticmethod
    # no room method
    def modelForSim(faces, windows, name):
        
        if len(name) == 0:
            displayName = clean_and_id_string('unnamed')
            units = units_system()
            
        model = Model(displayName, 
                      rooms = None,
                      orphaned_faces = faces, 
                      orphaned_shades = None,
                      orphaned_apertures = windows,
                      orphaned_doors = None, 
                      units=units, tolerance= None, angle_tolerance = 1.0)
        return model
    
    @staticmethod
    def GeoRhinoToRad(combModel, objFolder):
        # process the simulation folder name and the directory
        clean_name = re.sub(r'[^.A-Za-z0-9_-]', '_', combModel.display_name)
        print('clean_name: ', clean_name)
        folder = os.path.join(Folders.default_simulation_folder, clean_name, 'radiance') \
            if objFolder is None else objFolder
            
        print('obj folder: ', folder)
            
        if os.path.isdir(folder):
            nukedir(folder, rmdir=True)  # delete the folder if it already exists
        else:
            preparedir(folder)  # create the directory if it's not there

        # write the model folder
        combModel.to.rad_folder(combModel, folder, minimal=False)

        
            
        
        
                    
                    
        
        
        