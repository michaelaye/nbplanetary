from configparser import ConfigParser
import subprocess

config = ConfigParser(delimiters=['='])
config.read('settings.ini')
cfg = config['DEFAULT']
requirements = cfg.get('requirements', '')
cmd = "mamba install " + requirements + " -y"
print("Command to run:", cmd)
ret = subprocess.call(cmd, shell=True)
print("returned_value:", ret)
