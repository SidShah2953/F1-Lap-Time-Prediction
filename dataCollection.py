import pandas as pd
from helpers.dataCollection.raceCalendar import RaceCalendar
from helpers.dataCollection.trackGeometry import TrackGeometryAnalyzer
from helpers.dataCollection.trackWeather import TrackWeatherAnalyzer
from helpers.dataCollection.raceTelemetry import RaceTelemetry
from helpers.dataCollection.driverMetrics import DriverMetrics


years = [2023]


def main():
    store_race_calendar()
    store_track_geometry()
    store_track_weather()
    store_driver_metrics()
    store_race_telemetry()


def store_race_calendar():
    all_races = None
    for year in years:
        rc = RaceCalendar(year)
        rc = rc.get_race_calendar()
        rc['year'] = year
        
        if all_races is None:
            all_races = rc.copy()
            del rc
        else:
            all_races = all_races._append(rc)
            del rc
    
    all_races.to_excel(
                'Data/Raw Data/Race Calendar.xlsx', 
                index=False
            )
    
    return all_races


def store_track_geometry():
    races = pd.read_excel('Data/Raw Data/Race Calendar.xlsx')
    races = races[['year', 'round', 'location']]
    track_data = None
    for i in range(len(races)):
        year = races.iloc[i]['year']
        location = races.iloc[i]['location']

        TGA = TrackGeometryAnalyzer(
                    year=year,
                    grand_prix=location
                    )
        
        geometry = {
                    **races.iloc[i],
                    **TGA.calculate_track_geometry()
                }
        geometry = pd.DataFrame(geometry, index=[i])
        if track_data is None:
            track_data = geometry
        else:
            track_data = pd.concat([track_data, geometry])
    
    track_data.to_excel(
        'Data/Raw Data/Track Geometry.xlsx',
        index=False
    )
    
    return track_data


def store_track_weather():
    races = pd.read_excel('Data/Raw Data/Race Calendar.xlsx')
    races = races[['year', 'round', 'location']]
    track_data = None
    for i in range(len(races)):
        year = races.iloc[i]['year']
        location = races.iloc[i]['location']

        TWA = TrackWeatherAnalyzer(
                    year=year,
                    grand_prix=location
                    )
        
        weather = {
                    **races.iloc[i],
                    **TWA.engineer_weather_features()
                }
        weather = pd.DataFrame(weather)
        
        if track_data is None:
            track_data = weather
        else:
            track_data = pd.concat([track_data, weather])
    
    track_data.to_excel(
        'Data/Raw Data/Track Weather.xlsx',
        index=False
    )

    return track_data


def store_driver_metrics():
    races = pd.read_excel('Data/Raw Data/Race Calendar.xlsx')
    races = races[['year', 'round', 'location']]
    driver_data = None
    for i in range(len(races)):
        year = races.iloc[i]['year']
        location = races.iloc[i]['location']

        DM = DriverMetrics(
                    year=year,
                    grand_prix=location
                    )
        
        metrics = {
                    **races.iloc[i],
                    **DM.get_driver_metrics()
                }
        metrics = pd.DataFrame(metrics)
        metrics['BestLapTimeDelta'] = metrics['BestLapTime'] - metrics['BestLapTime'].min()
        
        if driver_data is None:
            driver_data = metrics
        else:
            driver_data = pd.concat([driver_data, metrics])
    
    driver_data.to_excel(
        'Data/Raw Data/Driver Metrics.xlsx',
        index=False
    )
    
    return driver_data


def store_race_telemetry():
    races = pd.read_excel('Data/Raw Data/Race Calendar.xlsx')
    races = races[['year', 'round', 'location']]
    track_data = None
    for i in range(len(races)):
        year = races.iloc[i]['year']
        location = races.iloc[i]['location']

        RC = RaceTelemetry(
                    year=year,
                    grand_prix=location
                    )
        
        telemetry = {
                    **races.iloc[i],
                    **RC.get_race_telemetry()
                }
        telemetry = pd.DataFrame(telemetry)
        if track_data is None:
            track_data = telemetry
        else:
            track_data = pd.concat([track_data, telemetry])
    
    track_data.dropna()

    track_data.to_excel(
        'Data/Raw Data/Race Telemetry.xlsx',
        index=False
    )
    
    return track_data


if __name__ == "__main__":
    main()