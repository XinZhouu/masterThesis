from honeybee.model import Model
from honeybee_radiance.properties.model import ModelRadianceProperties

class hbAssign:
    
    @staticmethod
    def viewOrGridToModel(model, view, hbGrid):
        assert isinstance(model, Model), \
            'Expected Honeybee Model. Got {}.'.format(type(model))
        hbModel = model.duplicate()  # duplicate to avoid editing the input
        if hbGrid != None:
            hbModel.properties.radiance.add_sensor_grid(hbGrid)            
        if view != None:  
            hbModel.properties.radiance.add_view(view)
        return hbModel  