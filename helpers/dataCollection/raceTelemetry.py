import fastf1
import pandas as pd
import numpy as np


# Enable Caching
fastf1.Cache.enable_cache('Cache/')

class RaceTelemetry():
    def __init__(self, year:int, grand_prix):
        self.year = year
        self.grand_prix = grand_prix
        self.session = fastf1.get_session(year, grand_prix, 'Race')
        self.session.load()


    def get_race_telemetry(self):
        laps = self.session.laps
        
        # Prepare comprehensive data
        comprehensive_data = []
        
        for driver in self.session.drivers:
            driver_laps = laps.pick_drivers(driver)
            
            for lap in driver_laps.itertuples():
                # Gather detailed information for each lap
                lap_data = {
                    # Driver Information
                    'DriverNumber': driver,
                    
                    'LapStartTime': lap.LapStartTime,
                    # Lap Performance Data
                    'LapTime': lap.LapTime.total_seconds() if lap.LapTime else np.nan,
                    'LapNumber': lap.LapNumber,
                    
                    # Tire Information
                    'Compound': lap.Compound,
                    'TyreLife': lap.TyreLife,
                    
                    # Sector Times
                    'Sector1Time': lap.Sector1Time.total_seconds(),
                    'Sector2Time': lap.Sector2Time.total_seconds(),
                    'Sector3Time': lap.Sector3Time.total_seconds(),
                    
                    # Track Conditions
                    'TrackStatus': lap.TrackStatus,
                    
                    # Additional Performance Metrics
                    'IsPersonalBest': lap.IsPersonalBest,
                    'Deleted': lap.Deleted
                }
                
                comprehensive_data.append(lap_data)
        
        # Convert to DataFrame
        df = pd.DataFrame(comprehensive_data)
        
        return df