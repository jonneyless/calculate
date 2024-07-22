from configparser import ConfigParser

# instantiate
config = ConfigParser()

# parse existing file
config.read('config/setting.ini')
