import os
import fastf1

def setup_cache_directory():
    """
    Create a 'Cache' folder in the current working directory 
    if it doesn't already exist
    """
    cache_path = os.path.join(os.getcwd(), 'Cache')
    os.makedirs(cache_path, exist_ok=True)
    
    fastf1.Cache.enable_cache(cache_path)


def setup_data_directory():
    """
    Create a 'Data' folder in the current working directory 
    if it doesn't already exist
    """
    data_path = os.path.join(os.getcwd(), 'Data')
    os.makedirs(data_path, exist_ok=True)