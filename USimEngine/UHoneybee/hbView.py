from honeybee.typing import clean_and_id_rad_string, clean_rad_string
from honeybee_radiance.view import View



class viewHB:
    
    # standard view operation
    @staticmethod
    def customizedView(name, position, direction, upVector, viewType, hAngle, vAngle):
        
        viewTypePool = ('v', 'h', 'l', 'c', 'a', 's')
        
        if len(name) == 0:
            name = clean_and_id_rad_string('View')
            
        if viewType is None:
            _type = 'v'
        else:
            if viewType in viewTypePool:
                _type = viewType
            else:
                print('viewType not found')
            
        _hAngle = 60 if hAngle is None else hAngle
        _vAngle = 60 if vAngle is None else vAngle
        
        # view = View(clean_rad_string(name), _pos, _dir, _upVector, _type,
        #         _hAngle, _vAngle)
        hbView = View(clean_rad_string(name), position, direction, upVector, _type,
                _hAngle, _vAngle)
        # automatically set view to size to 180 degrees if the view type is a fisheye
        hbView.standardize_fisheye()
        
        return hbView
    
    @staticmethod
    def outputPath(viewClass, folder, fileName, mkdir):
        path = viewClass.to_file(folder, fileName, mkdir)
        return path
        
        
                

            
        
        
        