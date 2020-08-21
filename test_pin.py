import sys
import RPi.GPIO as GPIO


if __name__ == '__main__':
    if(len(sys.argv) != 2):
        raise Exception('There must be only 1 argument provided: input pin number')
    input_pin_number = int(sys.argv[1])

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin_number, GPIO.IN)

    while True:
        try:
            print(GPIO.input(input_pin_number))
        except Exception as e:
            print(e)
