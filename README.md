# Stepper_uln2003
## ULN2003 stepper motor driver code for Raspberry Pi

This is a minimal Python program to drive a stepper motor using a Raspberry Pi and a driver board with the **ULN2003** IC. These boards are widely available and are often bundled with a 28BYJ-48 motor for practically nothing (< $2).

I make absolutely no reprsentations as to the portability of this code. It runs on my Pi, an 8GB Model 4B running Raspberry Pi OS Bookworm (AKA Debian 12), with Python 3.12 and the rpi-lgpio package. The out-of-the box RPi.GPIO apt package is basically useless; you're better off purging it and installing the lgpio variant which actually seems to work. Even better is to run the code in a venv.

As always, YMMV.
