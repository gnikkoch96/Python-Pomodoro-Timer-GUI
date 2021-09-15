import os
from playsound import playsound

pkg_dir = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(pkg_dir, '../resources/sounds/chime.wav')
print(file)
path = file
playsound(path)
print('playing sound now')