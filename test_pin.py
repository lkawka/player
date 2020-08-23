import sys
import RPi.GPIO as GPIO
from datetime import datetime


if __name__ == '__main__':
    if(len(sys.argv) != 2):
        raise Exception('There must be only 1 argument provided: input pin number')
    input_pin_number = int(sys.argv[1])

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin_number, GPIO.IN)

    while True:
        try:
            if GPIO.input(input_pin_number):
                print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), ': 1')
        except Exception as e:
            print(e)
