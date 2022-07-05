# LED Matrix controller

A simple application built in python to control an 8*8 LED matrix.

## Documentation:
https://github.lenzi.dev/MatrixDocs


## Specs:

LED Type: WS2811

Python version: 3.10.1

Pygame Version: 2.1.0



## What i'm using:

- ELEGOO NANO (Arduino nano equivalent)

- CJMCU 8*8 LED Matrix

- Random breadboard


## How to setup:

First take your Arduino, wire GND and 5V to the matrix, then wire the pin D5 on the arduino and wire to the DIN on the matrix.
Then upload the skecth 'mtrx-ino.ino' on the arduino, next change the parameter 'ARDUINO_NAME' in the file config if necessary, keep in mind that the name should be corresponding to the com port description, you can check it by running the tool 'py/COM_CHECKER.py'.
After that, run the app, and enjoy.
If you want to change the pin, just go in the arduino sketch and change values.

## Demonstration:

[![WORKING APP](https://i.ytimg.com/an_webp/wqejpU3aGb0/mqdefault_6s.webp?du=3000&sqp=CJ_BkpYG&rs=AOn4CLAIqQwrZ33uXqpA2OOlD-pVODyWkg)](https://www.youtube.com/watch?v=wqejpU3aGb0)

## TODO

- [x] Finishing docs
- [ ] Animations
- [x] COM Port detection
- [ ] Better GUI System
- [ ] Some refactoring -> expandability 
- [ ] Fixing frame speed(Synchronizing Arduino & Python)
- [x] Fixing brightness -> still in progress: buffer slow down.
- [x] Text History
- [ ] Removing Herobrine

## Special thanks
- [@MassimoSandre](https://www.github.com/MassimoSandre) suggestion about data transfer, and general help in adding text.


