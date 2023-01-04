import clr
clr.AddReferenceByName("Grasshopper")
import Grasshopper

from ladybug.graphic import GraphicContainer
from ladybug_rhino.togeometry import to_mesh3d
from ladybug_rhino.fromgeometry import from_mesh3d
from ladybug_rhino.fromobjects import legend_objects
from ladybug_rhino.text import text_objects
from ladybug_rhino.color import color_to_color


class hbVis:
    
    @staticmethod
    def spatialHeatMap(metricValues, mesh, offsetDomain, legendPara, legendTitle, globalTitle):
        # generate Ladybug objects
        lb_mesh = to_mesh3d(mesh)
        if offsetDomain:
            lb_mesh = lb_mesh.height_field_mesh(metricValues, offsetDomain)
        graphic = GraphicContainer(metricValues, lb_mesh.min, lb_mesh.max, legendPara)

        # generate titles
        if legendTitle is not None:
            graphic.legend_parameters.title = legendTitle
        if globalTitle is not None:
            title = text_objects(globalTitle, graphic.lower_title_location,
                                graphic.legend_parameters.text_height * 1.5,
                                graphic.legend_parameters.font)

        # draw rhino objects
        lb_mesh.colors = graphic.value_colors
        mesh = from_mesh3d(lb_mesh)
        legend = legend_objects(graphic.legend)
        colors = [color_to_color(col) for col in lb_mesh.colors]
        legend_par = graphic.legend_parameters
        
        return mesh, legend, colors, legend_par, lb_mesh.colors, lb_mesh.min, lb_mesh.max
        