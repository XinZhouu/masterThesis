import clr
clr.AddReferenceByName("Grasshopper")

import ladybug.analysisperiod as ap
from ladybug_rhino.grasshopper import wrap_output

class LBTime:
    
    @staticmethod
    def analysisPeriod(startMonth, startDay, startHour, endMonth, endDay, endHour, timeStep):
        anp = ap.AnalysisPeriod(
            startMonth, startDay, startHour, endMonth, endDay, endHour, timeStep)

        if anp:
            period = anp
            dates = wrap_output(anp.datetimes)
            hoys = anp.hoys
            
        return period, hoys, dates