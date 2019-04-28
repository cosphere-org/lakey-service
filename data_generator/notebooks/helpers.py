import pandas as pd
import dask.dataframe as dd


# interval - int in seconds
def getTimestampList(month, day, interval):
    number_of_events = int(24 * 3600 / interval)
    def calc(x):
        hour = int(x / (number_of_events / 24))
        minute = int((x - (3600 / interval) * hour) * 60 * (interval / 3600))
        second = int((x - ((3600 / interval) * hour + (60 / interval) * minute)) * 60 * (interval / 60))
        return (
            '2018-{m:02d}-{d:02d}T{h:02d}:{mm:02d}:{s:02d}Z'
            .format(
                m=month, 
                d=day, 
                h=hour,
                mm=minute,
                s=second))
    
    return [calc(x) for x in range(number_of_events)]


# temps - pandas dataframe[hour, mean, std] with 24 elements - hour, mean temperature during the hour, stddev
# factor - float <-1, 1>
# interval - int in seconds
def getTemperatureList(temps, factor, interval):
    temp_list = []
    day_std = []
    day_temp = []
    for r in temps.iterrows():
        day_std.append(r[1]['std'])
        day_temp.append(r[1]['mean'])
        
    number_of_events = int(24 * 3600 / interval)
    for x in range(number_of_events):
        hour = int(x / (number_of_events / 24))
        pointer_in_hour = int(x % (number_of_events / 24))    
        if not pointer_in_hour:
            temp = round(day_temp[hour] + day_std[hour] * factor, 1)

        else:
            next_factor = pointer_in_hour / int(3600 / interval)
            current_factor = 1 - next_factor
            next_hour = hour + 1
            if (next_hour == 24):
                next_hour = 23

            temp = round(
                ((day_temp[hour] + day_std[hour] * factor) * current_factor +
                (day_temp[next_hour] + day_std[next_hour] * factor) * next_factor), 
                1)

        temp_list.append(temp)
        
    return temp_list


def transformComplexDF(df, col_immutable_names, col_values_name, col_timestamp_name):    
    first = col_values_name
    second = col_timestamp_name
    data2 = (
        df[first].apply(pd.Series)
            .merge(df, right_index = True, left_index = True)
            .drop([first], axis = 1)
            .melt(id_vars = col_immutable_names + [second], value_name = first)
            .drop("variable", axis = 1)
            .dropna()
            .reset_index(drop=True))[col_immutable_names + [first]]
    
    data3 = (
        df[second].apply(pd.Series)
            .merge(df, right_index = True, left_index = True)
            .drop([second], axis = 1)
            .melt(id_vars = col_immutable_names + [first], value_name = second)
            .drop("variable", axis = 1)
            .dropna()
            .reset_index(drop=True))[[second]]
  
    return data2.join(data3)

##########################################################################################################################

feature_columns = ['gateway_uuid', 'timestamp', 'property', 'value', 'month', 'day']
day_room_temps = pd.DataFrame({
    'hour': range(24),
    'mean': [20, 20.5, 20, 19.5, 19, 19.7, 20.2, 21, 22, 23, 24, 25, 25, 20, 21, 22, 23, 24, 24, 23, 23, 22, 22, 21],
    'std': 2.0
})


def prepareOutsideTemperatureEvents(day_events, day_temps, month, day, interval, number_of_cores):
    feature_name = 'device.temperature.outside/value'
    
    events = day_events
    ddata = dd.from_pandas(events, npartitions=number_of_cores)
    timestamps = getTimestampList(month, day, interval)
    
    events['value'] = ddata.apply(
        lambda x: getTemperatureList(
            day_temps[(day_temps.zip_code_prefix == x.zip_code_prefix)].reset_index(drop=True),
            x.factor,
            interval
        ), 
        meta=('x', object), 
        axis=1).compute()
    
    events['timestamp'] = ddata.apply(lambda x: timestamps, meta=('x', object), axis=1).compute()
    
    events['property'] = feature_name
    
    return transformComplexDF(events[feature_columns], ['gateway_uuid', 'month', 'day', 'property'], 'value', 'timestamp')[feature_columns]


def prepareRoomTemperatureEvents(day_events, month, day, interval, number_of_cores):
    feature_name = 'device.temperature.room/value'
    
    events = day_events
    ddata = dd.from_pandas(events, npartitions=number_of_cores)
    timestamps = getTimestampList(month, day, interval)
    
    events['value'] = ddata.apply(
        lambda x: getTemperatureList(
            day_room_temps,
            x.factor,
            interval
        ), 
        meta=('x', object), 
        axis=1).compute()
    
    events['timestamp'] = ddata.apply(lambda x: timestamps, meta=('x', object), axis=1).compute()
    
    events['property'] = feature_name
    
    return transformComplexDF(events[feature_columns], ['gateway_uuid', 'month', 'day', 'property'], 'value', 'timestamp')[feature_columns]