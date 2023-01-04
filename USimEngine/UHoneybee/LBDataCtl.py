from ladybug.datacollection import BaseCollection

from ladybug.datacollection import HourlyContinuousCollection

class lbData:
    
    # this function divides HEADER and VALUES
    @staticmethod
    def deconstructLBData(data):
        assert isinstance(data, BaseCollection), \
            '_data must be a Data Collection. Got {}.'.format(type(data))
        header = data.header
        values = data.values   
        return header     
    
    @staticmethod
    def constructLBData(header, values):
        data = HourlyContinuousCollection(header, values)
        return data