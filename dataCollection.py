import pandas as pd
from helpers.dataCollection.raceCalendar import RaceCalendar
from helpers.dataCollection.trackGeometry import TrackGeometryAnalyzer

years = [2023]


def main():
    store_race_calendar()
    store_track_geometry()


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
                'Data/Race Calendar.xlsx', 
                index=False
            )


def store_track_geometry():
    races = pd.read_excel('Data/Race Calendar.xlsx')
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
        'Data/Track Geoemtry.xlsx',
        index=False
    )

if __name__ == "__main__":
    main()