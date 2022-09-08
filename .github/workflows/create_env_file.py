from configparser import ConfigParser
import subprocess

config = ConfigParser(delimiters=["="])
config.read("settings.ini")
cfg = config["DEFAULT"]
requirements = cfg.get("requirements", "").split()

with open("environment.yml", "w") as f:
    f.write("name: testenv\n")
    f.write("channels: conda-forge\n")
    f.write("dependencies:\n")
    f.writelines([f"  - {r}\n" for r in requirements])
