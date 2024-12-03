import fastf1
import pandas as pd
import numpy as np

# Enable Caching
fastf1.Cache.enable_cache('Cache/')

class DriverMetrics():
    def __init__(self, year:int, grand_prix):
        self.year = year
        self.grand_prix = grand_prix
        self.session = fastf1.get_session(year, grand_prix, 'Q')
        self.session.load()

    def get_scores_before(self):
        # Fetch the event schedule to confirm the year's events
        schedule = pd.read_excel('Data/Raw Data/Race Calendar.xlsx')
        events = schedule[(schedule['location'] == self.grand_prix)\
                            & (schedule['year'] == self.year)].index[0]

        events = schedule[:events][['year', 'location']]
        if len(events) == 0:
            event = schedule.iloc[0][['year', 'location']]
            session = fastf1.get_session(event.year, event.location, 'Race')
            session.load()

            points = pd.DataFrame({
                'DriverNumber': session.drivers,
                'PointsAtStart': [0] * len(session.results)
            })
        else:
            points = None
            for event in events.itertuples():
                session = fastf1.get_session(event.year, event.location, 'Race')
                session.load()
                
                # Get race results
                results = session.results[['DriverNumber', 'Points']]
                if points is None:
                    points = results.reset_index().drop('index', axis=1)
                else:
                    points = pd.concat([points, results])
                points = points.reset_index().drop('index', axis=1)

            points = points.groupby('DriverNumber')\
                        .agg(['sum'])\
                        .reset_index()

            points = pd.DataFrame({
                'DriverNumber': points[('DriverNumber','')],
                'PointsAtStart': points[('Points', 'sum')]
            })
            
        return points
    

    def get_fastest_qualifying(self):        
        # Prepare to store best laps
        best_laps = []
        
        # Iterate through each driver
        for driver in self.session.drivers:
            # Get driver information
            driver_info = self.session.get_driver(driver)
            
            # Get the driver's fastest qualifying lap
            fastest_lap = self.session.laps.pick_drivers(driver).pick_fastest()
            if isinstance(fastest_lap.LapTime, float):
                continue
            # Extract lap details
            lap_data = {
                # Driver Information
                'DriverNumber': driver,
                
                # Qualifying Lap Details
                'BestLapTime': fastest_lap.LapTime.total_seconds() \
                                if fastest_lap.LapTime else np.nan,
                'QualifyingPosition': driver_info.Position,
                
                # Lap Specifics
                'QualiCompound': fastest_lap.Compound,
                'QualiSector1Time': fastest_lap.Sector1Time.total_seconds(),
                'QualiSector2Time': fastest_lap.Sector2Time.total_seconds(),
                'QualiSector3Time': fastest_lap.Sector3Time.total_seconds(),
            }
            
            best_laps.append(lap_data)
        
        # Convert to DataFrame
        df = pd.DataFrame(best_laps)
        
        # Sort by best lap time
        df = df.reset_index()\
                .drop('index', axis=1)
        
        return df


    def get_driver_metrics(self):
        quali = self.get_fastest_qualifying()
        quali['DriverNumber'] = quali['DriverNumber'].astype(int)
        quali = quali.set_index('DriverNumber')

        points = self.get_scores_before()
        points['DriverNumber'] = points['DriverNumber'].astype(int)
        points = points.set_index('DriverNumber')

        df = quali.join(points, how='inner', rsuffix='_r')
        df = df.reset_index()
        
        return df