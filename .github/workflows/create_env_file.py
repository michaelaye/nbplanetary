from configparser import ConfigParser
import subprocess

config = ConfigParser(delimiters=["="])
config.read("settings.ini")
cfg = config["DEFAULT"]
requirements = cfg.get("requirements", "").split()

with open("environment.yml", "w") as f:
    f.write("name: my-env\n")
    f.write("dependencies:\n")
    f.writelines([f"  - {r}\n" for r in requirements])
