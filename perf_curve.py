class Fan_Curve:
    """
    A data container class. Contains fan curve coefficients.

    Fan curves are needed for any variable drive fans in air loops.
    See the EnergyPlus object documentation for 
    `Fan:VariableVolume <https://bigladdersoftware.com/epx/docs/9-1/input-output-reference/group-fans.html#fanvariablevolume>`_.

    Notes
    -----
    The fan curve equation used by EnergyPlus is

    .. math:: PLF = C_1 + C_2(FF^1) + C_3(FF^2) + C_4(FF^3)

    giving the fraction of full load power (PLF in W/W units) as a function
    of flow fraction (FF in CFM/CFM units). Flow fraction is the air mass
    flow rate divided by the maximum air mass flow rate.
    """

    fan_curve_coefficients = {
        'Constant Volume': [0, 1, 0, 0],
        '90.1 Appendix G Fan': [0.0013, 0.147, 0.9506, -0.0998],
        'Typical VSD': [0.047182815, 0.130541742, -0.117286942, 0.940313747],
        'VSD with SP Reset': [0.27827882, 0.026583195, -0.0870687, 1.03091975]
    }

class Pump_Curve:
    """
    A data container class. Contains pump curve coefficients.

    Pumps curves are needed for any variable speed pumps in plant and condenser loops.
    See the EnergyPlus object documentation for 
    `Pump:VariableSpeed <https://bigladdersoftware.com/epx/docs/9-1/input-output-reference/group-pumps.html#pumpvariablespeed>`_.

    Notes
    -----
    The pump curve equation used by EnergyPlus is

    .. math:: FractionFullLoadPower = C_1 + C_2(PLR^1) + C_3(PLR^2) + C_4(PLR^3)

    giving the fraction of full load power (W/W units) as a function
    of part load ratio (in GPM/GPM units).
    """
    pump_curve_coefficients = {
        'Variable Speed': [0.084926143, 0.18976705, 0.17646786, 0.54883895]
    }
    