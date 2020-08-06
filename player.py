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
        return json.load(f)


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


def check_GPIO(input_pin_number):
    # return GPIO.input(input_pin_number)
    return False


def check_dates(activation_times):
    now = datetime.now()
    for a in activation_times:
        h, m = a.split(':')
        delta =  (now.hour*3600+now.minute*60+now.second) - (int(h)*3600+int(m)*60)
        if delta >= 0 and delta < 2:
            return True
    return False


if __name__ == '__main__':
    config = read_config()
    print('Initialized with config:', config)
    activation_times = config["activationTimes"]
    background_path = PREFIX + config['backgroundPath']
    movie_path = PREFIX + config['moviePath']
    input_pin_number = config['inputPinNumber']
    
    setup(input_pin_number, background_path)

    player = create_player(movie_path)
    sleep(2.5)

    running = True
    while running:
        try:
            if check_GPIO(input_pin_number) or check_dates(activation_times):
                player.play()
                sleep(player.duration())
                player.quit()
                player = create_player(movie_path)
        except Exception as e:
            print(e)
            player = create_player(movie_path)
            sleep(2.5)
