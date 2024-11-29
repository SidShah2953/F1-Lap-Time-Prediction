import fastf1
import pandas as pd

# Enable Caching
fastf1.Cache.enable_cache('Cache/')

class TrackWeatherAnalyzer:
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


    def engineer_weather_features(self):
        """
        Create advanced weather features for machine learning
        """
        features = pd.DataFrame({
            'Time': self.session.weather_data['Time'],
            
            # Temperature-related features
            'AirTemp': self.session.weather_data['AirTemp'],
            'TrackTemp': self.session.weather_data['TrackTemp'],
            'Rain': self.session.weather_data['Rainfall'],

            # Humidity and wind complexity
            'HumidityWindInteraction': \
                self.session.weather_data['Humidity'] \
                    * self.session.weather_data['WindSpeed'],
            'WindChillFactor': \
                self.calculate_wind_chill(
                            self.session.weather_data['AirTemp'], 
                            self.session.weather_data['WindSpeed']
                        ),
            
            # Track surface condition indicators
            'SurfaceGripIndex': self.calculate_surface_grip(
                self.session.weather_data['TrackTemp'], 
                self.session.weather_data['Humidity']
            )
        })
        return features


    def calculate_wind_chill(self, temp, wind_speed):
        """
        Calculate wind chill factor
        """
        return 13.12 + (0.6215 * temp) - (11.37 * (wind_speed**0.16)) + (0.3965 * temp * (wind_speed**0.16))


    def calculate_surface_grip(self, temp, humidity):
        """
        Estimate track surface grip based on weather conditions
        """
        # Complex calculation considering temperature and humidity
        return (temp * (100 - humidity)) / 100