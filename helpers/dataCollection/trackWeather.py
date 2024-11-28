import fastf1
import pandas as pd

class TrackWeatherAnalyzer:
    def __init__(self,
                 year,
                 grand_prix):
        """
        Initialize track geometry analysis for a specific race
        
        Parameters:
        - year: Racing season year
        - grand_prix: Name of the Grand Prix event
        """
        self.session = fastf1.get_session(year, grand_prix, 'Race')
        self.session.load()


    def set_race_weather(self):        
        # print(self.session.weather_data)
        # Extract weather data directly
        weather_data = {
            'air_temperature': self.session.weather_data['AirTemp'],
            'track_temperature': self.session.weather_data['TrackTemp'],
            'humidity': self.session.weather_data['Humidity'],
            'wind_speed': self.session.weather_data['WindSpeed'],
            'wind_direction': self.session.weather_data['WindDirection']
        }
        self.weather_data = weather_data


    def engineer_weather_features(self):
        """
        Create advanced weather features for machine learning
        """
        self.set_race_weather()
        weather_data = self.weather_data
        # print(weather_data)

        features = pd.DataFrame({
            # Temperature-related features
            'air_temperature': weather_data['air_temperature'],
            'track_temperature': weather_data['track_temperature'],

            # Humidity and wind complexity
            'humidity_wind_interaction': \
                weather_data['humidity'] * weather_data['wind_speed'],
            'wind_chill_factor': \
                self.calculate_wind_chill(
                            weather_data['air_temperature'], 
                            weather_data['wind_speed']
                        ),
            
            # Track surface condition indicators
            'surface_grip_index': self.calculate_surface_grip(
                weather_data['track_temperature'], 
                weather_data['humidity']
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