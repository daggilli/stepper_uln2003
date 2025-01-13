# pylint: disable = missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=unused-import
import RPi.GPIO as GPIO
import time
import sys
from typing import Literal

GPIO17 = 17

STEP_IN1 = 18
STEP_IN2 = 27
STEP_IN3 = 22
STEP_IN4 = 23

STEP_PINS = [STEP_IN1, STEP_IN2, STEP_IN3, STEP_IN4]

STEP_SLEEP = 0.002

STEP_COUNT = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

STEP_SEQ: list[list[Literal[0, 1]]] =[
    [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH],
    [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW],
    [GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH],
    [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH]
]

DIR_CW = Literal[False]
DIR_ACW = Literal[True]

def setup() -> None:
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use SOC pin numbering
    for pin in STEP_PINS:    
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


def cleanup():
    for pin in STEP_PINS:
        GPIO.output(pin, GPIO.LOW)

    GPIO.cleanup()


def main(argv: list[str]) -> None:
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use SOC pin numbering
    setup()

    step_ctr = 0
    step_increment: int = 1 if (len(argv) < 2 or argv[1] == '1') else -1 

    try:
        for i in range(STEP_COUNT):
            for ix, pin in enumerate(STEP_PINS):
                GPIO.output(pin, STEP_SEQ[step_ctr][ix])
            
            step_ctr = (step_ctr + step_increment) % 8
            
            time.sleep(STEP_SLEEP)

    except KeyboardInterrupt:
        print("KBD IRQ")
        cleanup()
        exit(0)

    cleanup()

if __name__ == "__main__":
    main(sys.argv)

