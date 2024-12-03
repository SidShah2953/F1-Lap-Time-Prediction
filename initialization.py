from helpers.initialization import setup_cache_directory, setup_data_directory

def main():
    setup_cache_directory()
    setup_data_directory()

    print('Directories set up successfully!')