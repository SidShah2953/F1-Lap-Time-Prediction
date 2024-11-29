import fastf1

# Enable Caching
fastf1.Cache.enable_cache('Cache/')

class RaceCalendar():
    def __init__(self, year:int):
        self.year = year


    def get_race_calendar(self):
        schedule = fastf1.get_event_schedule(self.year)
        
        # Select relevant columns
        races_df = schedule[['RoundNumber', 'EventName', 'Location', 'Country', 'EventDate']]
        
        # Rename columns for clarity
        races_df = races_df.rename(columns={
            'RoundNumber': 'round',
            'EventName': 'name',
            'Location': 'location',
            'Country': 'country',
            'EventDate': 'date'
        })
        
        # Skipping the Pre-season Testing
        races_df = races_df[races_df['round'] > 0] \
                    .copy() \
                    .reset_index()\
                    .drop('index', axis=1)

        return races_df
