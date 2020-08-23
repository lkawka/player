import os
from subprocess import Popen
from time import sleep


MOVIE_PATH = 'assets/phone.avi'


def play(movie_path):
    os.system('killall omxplayer.bin')
    omxc = Popen(['omxplayer', '-b', movie_path])


print('play 1')
play(MOVIE_PATH)
sleep(7)

print('play 2')
play(MOVIE_PATH)
sleep(2)
print('play 3')
play(MOVIE_PATH)
