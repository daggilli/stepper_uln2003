# Copyright (c) 2025, David Gillies
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pylint: disable = missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=unused-import
import sys
import time
from typing import Literal
import RPi.GPIO as GPIO

# Any four standard GPIO pins will work
STEP_IN1 = 18
STEP_IN2 = 27
STEP_IN3 = 22
STEP_IN4 = 23

STEP_PINS = [STEP_IN1, STEP_IN2, STEP_IN3, STEP_IN4]

STEP_SLEEP = 0.001  # this is possibly marginal under load
STEPS_PER_REVOLUTION = 4096  # 64 steps, internal gearbox is 64:1

STEP_SEQ: list[list[Literal[0, 1]]] = [
    [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH],
    [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW],
    [GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH],
    [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH],
]

# Winding activation pattern
# *..* 9
# *... 8
# **.. 12
# .*.. 4
# .**. 6
# ..*. 2
# ..** 3
# ...* 1

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
    setup()

    step_index = 0
    step_increment: int = 1 if (len(argv) < 2 or argv[1] == "1") else -1

    try:
        for _ in range(STEPS_PER_REVOLUTION):
            for ix, pin in enumerate(STEP_PINS):
                GPIO.output(pin, STEP_SEQ[step_index][ix])

            step_index = (step_index + step_increment) % 8

            time.sleep(STEP_SLEEP)
    except KeyboardInterrupt:
        cleanup()
        exit(0)

    cleanup()


if __name__ == "__main__":
    main(sys.argv)
