import clr
clr.AddReferenceByName("Grasshopper")

from ladybug.wea import Wea
from ladybug.datacollection import HourlyContinuousCollection
from ladybug.header import Header
from ladybug.datatype.illuminance import Illuminance

from ladybug_geometry.geometry2d.pointvector import Vector2D, Point2D
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.plane import Plane

from ladybug.sunpath import Sunpath
from ladybug.compass import Compass
from ladybug.graphic import GraphicContainer
from ladybug.datacollection import HourlyContinuousCollection
from ladybug.dt import Date

from ladybug_rhino.config import conversion_to_meters
from ladybug_rhino.color import color_to_color
from ladybug_rhino.colorize import ColoredPoint
from ladybug_rhino.fromgeometry import from_polyline3d, from_polyline2d, \
    from_arc3d, from_vector3d, from_point3d, from_point2d
from ladybug_rhino.fromobjects import legend_objects, compass_objects
from ladybug_rhino.togeometry import to_vector2d, to_point2d, to_point3d
from ladybug_rhino.text import text_objects
from ladybug_rhino.grasshopper import list_to_data_tree, \
    hide_output, show_output, schedule_solution

import math

class solar:
    
    @staticmethod
    def irradToillum(data):
        """Change the data type of an input collection from irradiane to illuminance."""
        head = data.header
        new_header = Header(Illuminance(), 'lux', head.analysis_period, head.metadata)
        return HourlyContinuousCollection(new_header, data.values) if \
            isinstance(data, HourlyContinuousCollection) else \
            data.__class__(new_header, data.values, data.datetimes)
            
    @staticmethod      
    def directIllumInHorizPlane(loc, dirNormal, diffhorz, srfAzimuth, sefAltit, gdRef, anisotropic):
        # set default values
        az = srfAzimuth if srfAzimuth is not None else 180
        alt = sefAltit if sefAltit is not None else 0
        gref = gdRef if gdRef is not None else 0.2
        isot = not anisotropic

        # create the Wea and output irradaince
        wea = Wea(loc, dirNormal, diffhorz)
        total, direct, diff, reflect = \
            wea.directional_irradiance(alt, az, gref, isot)
        for dat in (total, direct, diff, reflect):
            dat.header.metadata['altitude'] = alt
            dat.header.metadata['azimuth'] = az

        # convert to illuminace if input data was illuiminance
        if isinstance(dirNormal.header.data_type, Illuminance):
            total = solar.irradToillum(total)
            direct = solar.irradToillum(direct)
            diff = solar.irradToillum(diff)
            reflect = solar.irradToillum(reflect)
            
        return direct
        
        
class hbSun:

    @staticmethod
    def sunVectorsForHours(north_, _location, hoys_, dl_saving_, solar_time_, _center_pt_,
                _scale_, projection_, data_, statement_):
        
        # process all of the global inputs for the sunpath
        if north_ is not None:  # process the north_
            try:
                north_ = math.degrees(
                    to_vector2d(north_).angle_clockwise(Vector2D(0, 1)))
            except AttributeError:  # north angle instead of vector
                north_ = float(north_)
        else:
            north_ = 0
            
        if _center_pt_ is not None:  # process the center point into a Point2D
            center_pt, center_pt3d = to_point2d(_center_pt_), to_point3d(_center_pt_)
            z = center_pt3d.z
        else:
            center_pt, center_pt3d = Point2D(), Point3D()
            z = 0
            
        _scale_ = 1 if _scale_ is None else _scale_ # process the scale into a radius
        radius = (100 * _scale_) / conversion_to_meters()
        solar_time_ = False if solar_time_ is None else solar_time_  # process solar time
        projection_ = projection_.title() if projection_ is not None else None

        if len(data_) > 0 and len(hoys_) > 0:
            all_aligned = all(data_[0].is_collection_aligned(d) for d in data_[1:])
            assert all_aligned, 'All collections input to data_ must be aligned for ' \
                'each Sunpath.\nGrafting the data_ and suplying multiple grafted ' \
                '_center_pt_ can be used to view each data on its own path.'
            if statement_ is not None:
                data_ = HourlyContinuousCollection.filter_collections_by_statement(
                    data_, statement_)
            data_hoys = set(dt.hoy for dt in data_[0].datetimes)
            hoys_ = list(data_hoys.intersection(set(hoys_)))

        # initialize sunpath based on location
        sp = Sunpath.from_location(_location, north_, dl_saving_)

        # process all of the input hoys into altitudes, azimuths and vectors
        altitudes, azimuths, datetimes, moys, hoys, vectors, suns = [], [], [], [], [], [], []
        for hoy in hoys_:
            sun = sp.calculate_sun_from_hoy(hoy, solar_time_)
            if sun.is_during_day:
                altitudes.append(sun.altitude)
                azimuths.append(sun.azimuth)
                datetimes.append(sun.datetime)
                moys.append(sun.datetime.moy)
                hoys.append(sun.datetime.hoy)
                vectors.append(from_vector3d(sun.sun_vector))
                suns.append(sun)

        return vectors

        