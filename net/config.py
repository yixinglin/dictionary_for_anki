import platform
from pathlib import Path
import os

sysstr = platform.system()

# Defalt Paths
if sysstr == "Windows":
  HTML_PATH = "D://anki/html"
  AUDIO_PATH = "D://anki/audio"
  PIC_PATH = "D://anki/picture"
else:  # sysstr == "Linux"
  HTML_PATH = os.environ['HOME'] + "/Documents/anki/html"
  AUDIO_PATH = os.environ['HOME'] + "/Documents/anki/audio"
  PIC_PATH = os.environ['HOME'] + "/Documents/anki/picture"

print("System: ", sysstr)
print("Home path: ", str(Path.home()))
print("Html path: ", HTML_PATH)
print("Audio path: ", AUDIO_PATH)
print("Picture path: ", PIC_PATH)