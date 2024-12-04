import pandas as pd
from helpers.dataPreprocessing import quantize_time


input_path = 'Data/Raw Data/'
output_path = 'Data/Cleaned Data/'


def main():
    preprocess_track_geom_data()
    preprocess_track_weath_data()
    preprocess_race_telemetry()
    preprocess_driver_metrics()


def preprocess_track_geom_data(file_name="Track Geometry.xlsx"):
    track_info = pd.read_excel(input_path + file_name)
    track_info = track_info.drop('MaxElevation', axis=1)
    track_info = track_info.drop('location', axis=1)
    
    track_info.to_excel(
            output_path + file_name,
            index=False
        )

    return track_info


def preprocess_track_weath_data(file_name="Track Weather.xlsx"):
    weather_info = pd.read_excel(input_path + file_name)
    weather_info = quantize_time(weather_info, time_col='Time')
    weather_info = weather_info.drop('location', axis=1)
    weather_info = weather_info.drop('Time', axis=1)
    
    weather_info.to_excel(
            output_path + file_name,
            index=False
        )

    return weather_info


def preprocess_race_telemetry(file_name="Race Telemetry.xlsx"):
    lap_info = pd.read_excel(input_path + file_name)
    lap_info = lap_info[lap_info['TrackStatus'] == 1]
    lap_info = lap_info[lap_info['Deleted'] == False]
    lap_info = lap_info.drop(['TrackStatus', 'Deleted'], axis=1)
    lap_info = quantize_time(lap_info, time_col='LapStartTime')
    lap_info = lap_info.drop('location', axis=1)
    lap_info = lap_info.drop('LapStartTime', axis=1)

    lap_info = lap_info.drop(['Sector1Time', 'Sector2Time', 'Sector3Time'], axis=1)
    lap_info = lap_info.drop('IsPersonalBest', axis=1)
    
    lap_info.to_excel(
            output_path + file_name,
            index=False
        )

    return lap_info


def preprocess_driver_metrics(file_name="Driver Metrics.xlsx"):
    lap_info = pd.read_excel(input_path + file_name)
    lap_info = lap_info.drop('location', axis=1)

    lap_info = lap_info.drop(['BestLapTime', 'QualifyingPosition'], axis=1)
    lap_info = lap_info.drop(['QualiSector1Time', 'QualiSector2Time', 'QualiSector3Time'], axis=1)
    
    
    lap_info.to_excel(
            output_path + file_name,
            index=False
        )

    return lap_info


if __name__ == "__main__":
    main()