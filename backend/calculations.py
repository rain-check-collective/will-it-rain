import pandas as pd

# Calculate average precipitation for date
def calc_precip_average(df_precip):
    observed_precip = len(df_precip[df_precip['p01i'] > 0])
    all_precip = len(df_precip)

    if all_precip > 0:
        return (round((observed_precip / all_precip) * 100, 1))
    else:
        return 0
    
# Calculate average high temperature for date
def calc_high_temp_average(df_temp, threshold=85):
    observed_high_temp = len(df_temp[df_temp['tmpf'] > threshold])
    all_temp = len(df_temp)

    if all_temp > 0:
        return (round((observed_high_temp / all_temp) * 100, 1))
    else:
        return 0

# Calculate average low temperature for date
def calc_low_temp_average(df_temp, threshold=32):
    observed_low_temp = len(df_temp[df_temp['tmpf'] < threshold])
    all_temp = len(df_temp)

    if all_temp > 0:
        return (round((observed_low_temp / all_temp) * 100, 1))
    else:
        return 0

# Calculate average windspeed for date
def calc_wind_average(df_wind, threshold=20):
    observed_wind = len(df_wind[df_wind['sknt'] < threshold])
    all_wind = len(df_wind)

    if all_wind > 0:
        return (round((observed_wind / all_wind) * 100, 1))
    else:
        return 0

# Calculate average humidity for date
def calc_humidity_average(df_relh, threshold=20):
    observed_relh = len(df_relh[df_relh['relh'] < threshold])
    all_relh = len(df_relh)

    if all_relh > 0:
        return (round((observed_relh / all_relh) * 100, 1))
    else:
        return 0