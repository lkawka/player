import RPi.GPIO as GPIO
import os
from subprocess import Popen
from time import sleep
import json
from datetime import datetime
import logging

PREFIX = '/home/pi/Desktop/player/'


def setup_logger():
    logger = logging.getLogger('player')
    hdlr = logging.FileHandler(PREFIX + 'player.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)
    return logger


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
    img = Popen(['feh', '-B', '--hide-pointer', '-F', '-x', '-q', '--zoom', 'fill',
                 '-B', 'black', background_path])


def play(movie_path):
    try:
      os.system('killall omxplayer.bin')
    finally:
      omxc = Popen(['omxplayer', '-o', 'local', '--blank=#00FFFFFF', movie_path])
      sleep(94)


if __name__ == '__main__':
    logger = setup_logger()
    logger.info('Player started')

    config = read_config()
    background_path = PREFIX + config['backgroundPath']
    movie_path = PREFIX + config['moviePath']
    input_pin_number = config['inputPinNumber']

    setup(input_pin_number, background_path)

    running = True
    while running:
        try:
            curr_input = GPIO.input(input_pin_number)
            if curr_input:
              play(movie_path)
        except Exception as e:
            print(e)
            logger.error(e)
