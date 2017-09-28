import configparser
from os import environ
from os.path import dirname, abspath
#Initialize parser for reading config file
config = configparser.ConfigParser()

#Read from config file in the above directory
config.read(dirname(dirname(abspath(__file__))) + "/config.ini")


java_path = config['JAVA']['java-path']
if java_path:
    environ['JAVAHOME'] = java_path