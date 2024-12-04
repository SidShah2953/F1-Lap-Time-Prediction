import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer

input_path = "Data/Cleaned Data/"
output_path = "Data/"

def main():
    track_data = pd.read_excel(input_path + 'Track Geometry.xlsx')
    track_data['key'] = track_data['year'] * 1000 \
                            + track_data['round']
    track_data = track_data.set_index('key')

    weather_data = pd.read_excel(input_path + 'Track Weather.xlsx')
    weather_data['key'] = weather_data['year'] * 1000 \
                            + weather_data['round']
    weather_data = weather_data.set_index('key')

    df = weather_data\
            .join(track_data, how='left', rsuffix='_r')\
            .dropna()\
            .reset_index()
    df = df.drop(
                    [
                        col 
                        for col in df.columns 
                        if col[-2:] == '_r'
                    ], 
                    axis=1
                )
    df['key'] = df['key'] * 10000 + df['TimeQuant']
    df = df.set_index('key')

    lap_data = pd.read_excel(input_path + 'Race Telemetry.xlsx')
    lap_data['key'] = lap_data['year'] * 1000 * 10000 \
                        + lap_data['round'] * 10000 \
                        + lap_data['LapStartTimeQuant']
    lap_data = lap_data.set_index('key')

    df = lap_data.join(df, how='left', rsuffix='_r')\
            .dropna()\
            .reset_index()
    df = df.drop(
                    [
                        col 
                        for col in df.columns 
                        if col[-2:] == '_r'
                    ], 
                    axis=1
                )
    df['key'] = df['year'] * 1000 * 1000 \
                    + df['round'] * 1000 \
                    + df['DriverNumber']
    df = df.set_index('key')

    driver_data = pd.read_excel(input_path + 'Driver Metrics.xlsx')
    driver_data['key'] = driver_data['year'] * 1000 * 1000 \
                            + driver_data['round'] * 1000 \
                            + driver_data['DriverNumber']
    driver_data = driver_data.set_index('key')

    df = df.join(driver_data, how='left', rsuffix='_r')\
            .dropna()\
            .reset_index()
    df = df.drop(
                    ['key'] + 
                    [
                        col 
                        for col in df.columns 
                        if col[-2:] == '_r'
                    ], 
                    axis=1
                )

    df['LapsLeft'] = df['TotalLaps'] - df['LapNumber']

    df = df[[
                'year', 'round', 'DriverNumber',
                'LapsLeft', 
                'Compound', 'TyreLife', 
                'AirTemp', 'TrackTemp', 'Rain', 
                'HumidityWindInteraction', 'WindChillFactor', 'SurfaceGripIndex',
                'TrackLength',
                'NumberOfCorners', 'TotalCurvature', 'MaxCurvature', 'CurvatureSD', 
                'MinElevation', 'TotalElevationChange', 'ElevationSD', 
                'PointsAtStart', 'BestLapTimeDelta',
                'LapTime'
            ]]

    categorical_columns = ['Compound']
    preserved_columns = ['year', 'round', 'DriverNumber', 'LapTime']
    numerical_columns = [
        'LapsLeft', 'TyreLife', 'AirTemp', 'TrackTemp', 'Rain', 
        'HumidityWindInteraction', 'WindChillFactor', 'SurfaceGripIndex', 
        'TrackLength', 'NumberOfCorners', 'TotalCurvature', 'MaxCurvature', 
        'CurvatureSD', 'MinElevation', 'TotalElevationChange', 'ElevationSD', 
        'PointsAtStart', 'BestLapTimeDelta'
    ]

    onehot_encoder = OneHotEncoder(handle_unknown='ignore')
    compound_encoded = onehot_encoder.fit_transform(df[categorical_columns]).toarray()

    tyre_life = df['TyreLife'].values.reshape(-1, 1)
    multiplied_features = compound_encoded * tyre_life

    other_features = df[preserved_columns + numerical_columns].values
    X_transformed = np.hstack([multiplied_features, other_features])

    compound_feature_names = onehot_encoder.get_feature_names_out(['Compound'])
    feature_names = list(compound_feature_names) + preserved_columns + numerical_columns

    df = pd.DataFrame(X_transformed, columns=feature_names, index=df.index)
    df = df[[
                'year', 'round', 'DriverNumber',
                'Compound_SOFT', 'Compound_MEDIUM', 'Compound_HARD', 
                'Compound_INTERMEDIATE', 'Compound_WET', 
                'LapsLeft', 
                'AirTemp', 'TrackTemp', 'Rain',
                'HumidityWindInteraction', 'WindChillFactor', 'SurfaceGripIndex',
                'TrackLength', 'NumberOfCorners', 'TotalCurvature', 'MaxCurvature',
                'CurvatureSD', 'MinElevation', 'TotalElevationChange', 'ElevationSD',
                'PointsAtStart', 'BestLapTimeDelta',
                'LapTime',
       ]]
    
    df.to_excel(output_path + "Data.xlsx", index=False)
    
    return df