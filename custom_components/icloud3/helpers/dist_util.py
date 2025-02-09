

from   homeassistant.util.location import distance

from ..global_variables import GlobalVariables as Gb
from .common            import (round_to_zero, )
from .messaging         import (_trace, _traceha, )


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#   Distance calculation and conversion functions
#
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def calc_distance_km(from_gps, to_gps):

    dist_m = calc_distance_m(from_gps, to_gps)
    return round_to_zero(dist_m/1000)

#--------------------------------------------------------------------
def calc_distance_m(from_gps, to_gps):
    from_lat, from_long = from_gps
    to_lat, to_long     = to_gps

    if (from_lat is None or from_long is None or to_lat is None or to_long is None
            or from_lat == 0  or from_long == 0 or to_lat == 0 or to_long == 0):
        return 0

    dist_m = distance(from_lat, from_long, to_lat, to_long)
    dist_m = round_to_zero(dist_m)
    dist_m = 0 if dist_m < .002 else dist_m
    return dist_m

#--------------------------------------------------------------------
def km_to_mi(dist_km):
    return float(dist_km) * Gb.um_km_mi_factor

#--------------------------------------
def mi_to_km(dist_mi):
    return round(float(dist_mi) / Gb.um_km_mi_factor, 2)

#--------------------------------------
def m_to_ft(dist_m):
   return float(dist_m) * Gb.um_m_ft_factor

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#   Distance string formatting functions
#
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>-
def m_to_um_ft(dist_m, as_integer=False):

    if Gb.um_KM:
        if round_to_zero(dist_m) == 0: return "0m"
        if as_integer: return f"{int(dist_m)}m"
        return f"{dist_m:.1f}m"

    dist_ft = m_to_ft(dist_m)
    if round_to_zero(dist_ft) == 0: return "0ft"
    if as_integer: return f"{int(dist_ft)}ft"
    return f"{dist_ft:.1f}ft"

#--------------------------------------------------------------------
def m_to_um(dist_m):
    return km_to_um(dist_m / 1000)

def km_to_um(dist_km):
    if Gb.um_KM:
        return format_dist_km(dist_km)

    dist_mi = dist_km * Gb.um_km_mi_factor
    return format_dist_mi(dist_mi)

#--------------------------------------
def format_dist_m(dist_m):

    dist_km = dist_m / 1000
    return format_dist_km(dist_km)

#--------------------------------------
def format_dist_km(dist_km):

    if dist_km >= 100: return f"{dist_km:.0f}km"
    if dist_km >= 10:  return f"{dist_km:.1f}km"
    if dist_km >= 1:   return f"{dist_km:.2f}km"
    if round_to_zero(dist_km) == 0: return f"0km"
    return f"{dist_km*1000:.1f}m"

#--------------------------------------------------------------------
def format_dist_mi(dist_mi):

    if dist_mi >= 100:     return f"{dist_mi:.0f}mi"
    if dist_mi >= 10:      return f"{dist_mi:.1f}mi"
    if dist_mi >= 1:       return f"{dist_mi:.1f}mi"
    if dist_mi >= .0947:   return f"{dist_mi:.2f}mi"
    if round_to_zero(dist_mi) == 0: return f"0mi"

    dist_ft = dist_mi * 5280
    if dist_ft > 1:        return f"{int(dist_ft)}ft"
    return f"{dist_ft:.2f}ft"
