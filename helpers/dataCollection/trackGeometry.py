import numpy as np
import fastf1
from scipy.spatial.distance import euclidean

# Enable Caching
fastf1.Cache.enable_cache('Cache/')

class TrackGeometryAnalyzer:
    def __init__(self,
                 year,
                 grand_prix):
        """
        Parameters:
        - year: Racing season year
        - grand_prix: Name of the Grand Prix event
        """
        self.session = fastf1.get_session(year, grand_prix, 'Race')
        self.session.load()
        self.driver = self.session.drivers[0]
        self.circuit_info = self.session.get_circuit_info()
    
    
    def calculate_track_geometry(self):
        """
        Comprehensive track geometry calculation
        """
        # Collect all laps' telemetry
        telemetry = self.session\
                        .laps\
                        .pick_drivers(self.driver)\
                        .get_telemetry()
        
        # Default unit is 1/10 metres
        for col in ['X', 'Y', 'Z']:
            telemetry[col] = telemetry[col] / 10
        
        # Calculate track length
        def calculate_track_length(telemetry):
            # Calculate cumulative distance using Euclidean distance between points
            distances = [
                            euclidean(
                                telemetry.iloc[i][['X', 'Y', 'Z']], 
                                telemetry.iloc[i + 1][['X', 'Y', 'Z']]
                            ) 
                            for i in range(len(telemetry) - 1)
                        ]
            return np.sum(distances) / self.session.total_laps
        
        # Calculate elevation changes
        def calculate_elevation_profile(telemetry):
            z_data = telemetry['Z']
            return {
                'MaxElevation': z_data.max(),
                'MinElevation': z_data.min(),
                'TotalElevationChange': z_data.max() - z_data.min(),
                'ElevationSD': z_data.std()
            }
        
        # Calculate track curvature
        def calculate_track_curvature(telemetry):
            # Calculate angle changes between consecutive points
            dx = np.diff(telemetry['X'])
            dy = np.diff(telemetry['Y'])
            angles = np.arctan2(dy, dx)
            angle_changes = np.diff(angles)
            
            return {
                'NumberOfCorners': len(self.circuit_info.corners),
                'TotalCurvature': np.sum(np.abs(angle_changes)) / self.session.total_laps,
                'MaxCurvature': np.max(np.abs(angle_changes)),
                'CurvatureSD': np.std(angle_changes)
            }
        
        # Return comprehensive track geometry
        return {
            'TrackLength': calculate_track_length(telemetry),
            'TotalLaps': self.session.total_laps,
            **calculate_elevation_profile(telemetry),
            **calculate_track_curvature(telemetry)
        }