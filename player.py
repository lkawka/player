import RPi.GPIO as GPIO
import os
from subprocess import Popen
from omxplayer.player import OMXPlayer
from time import sleep
import json
from datetime import datetime

PREFIX = '/home/pi/Desktop/player/'


def read_config():
    with open(PREFIX + 'config.json') as f:
        config = json.load(f)
        print('Initialized with config:', config)
        return config


def setup(input_pin_number, background_path):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin_number, GPIO.IN)
    os.environ["DISPLAY"] = ":0.0"

    hide_mouse = Popen(['unclutter', '-idle', '0'])
    img = Popen(['feh', '-B', '--hide-pointer', '-F', '-x', '-q', '--auto-zoom',
                 '-B', 'black', '-g', '1280x800', background_path])


def create_player(movie_path):
    player = OMXPlayer(movie_path)
    player.pause()
    player.hide_video()

    return player


def play(movie_path):
    os.system('killall omxplayer.bin')
    omxc = Popen(['omxplayer', '-b', movie_path])


def check_GPIO(input_pin_number):
    return GPIO.input(input_pin_number)
    # return False


if __name__ == '__main__':
    config = read_config()
    background_path = PREFIX + config['backgroundPath']
    movie_path = PREFIX + config['moviePath']
    input_pin_number = config['inputPinNumber']
    
    setup(input_pin_number, background_path)

    player = create_player(movie_path)
    sleep(2.5)

    running = True
    while running:
        try:
            if check_GPIO(input_pin_number):
                player.play()
                sleep(player.duration())
                player.quit()
                player = create_player(movie_path)
        except Exception as e:
            print(e)
            player = create_player(movie_path)
            sleep(2.5)
