import fastf1
import pandas as pd
import numpy as np


class DriverMetrics():
    def __init__(self, year:int, grand_prix):
        self.year = year
        self.grand_prix = grand_prix
        self.session = fastf1.get_session(year, grand_prix, 'Q')
        self.session.load()


    def get_fastest_qualifying(self):        
        # Prepare to store best laps
        best_laps = []
        
        # Iterate through each driver
        for driver in self.session.drivers:
            # Get driver information
            driver_info = self.session.get_driver(driver)
            
            # Get the driver's fastest qualifying lap
            fastest_lap = self.session.laps.pick_drivers(driver).pick_fastest()
            
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
        df_sorted = df.sort_values('BestLapTime')
        
        return df_sorted
