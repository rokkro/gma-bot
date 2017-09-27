import configparser
from os.path import dirname, abspath
#Initialize parser for reading config file
config = configparser.ConfigParser()

#Read from config file in the above directory
config.read(dirname(dirname(abspath(__file__))) + "/config.ini")