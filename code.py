# AUTOMATED CAT FOOD DISPENSER
# AUTHOR: Joel Huffman
# LAST UPDATED: 7/22/2020
# PURPOSE: Allow cats to dispense serve themselves dry food pellets by depressing a
# push button. To prevent gourging. food will be dispensed in small quantites and only
# if specific criteria are met.
# RULES: The feeder has 2 states: ready and cooldown.
# - In ready state, if button is pressed, a small portion of food will be dispensed,
# a positive sound will be played, and the feeder will switch to cooldown state.
# - In cooldown state, button presses will play a negative sound, flash error lights 
# and NOT dispense food.  
# - After 4 hours in cooldown state, the feeder will revert to ready state and play 
# a dinner bell sound.

from time import sleep, monotonic
import board
from digitalio import DigitalInOut, Pull, Direction
from neopixel import NeoPixel

# audio setup
try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile
 
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

# color rgb values
OFF = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# neopixels
pixels = NeoPixel(board.NEOPIXEL, 10, brightness=0.2)

# red LED
led = DigitalInOut(board.D13)
led.switch_to_output()

# face button 1 (left)
button_1 = DigitalInOut(board.BUTTON_A)
button_1.switch_to_input(pull=Pull.DOWN)

# feed button
button_feed = DigitalInOut(board.A1)
button_feed.direction = Direction.INPUT
button_feed.pull = Pull.UP

# motor controller
motor = DigitalInOut(board.A2)
motor.direction = Direction.OUTPUT

# enable audio speaker
speaker = DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = Direction.OUTPUT
speaker.value = True

# blink all neopixels red 3 times
def errorBlink():
    for i in range(3):
        pixels.fill(RED)
        pixels.show()
        sleep(0.1)
        pixels.fill(OFF)
        pixels.show()
        sleep(0.1)

# runs motor for 'duration' (in seconds) then turns off motor
def runMotor(duration):
    motor.value = True
    pixels.fill(BLUE)
    pixels.show()
    sleep(duration)
    motor.value = False
    pixels.fill(OFF)
    pixels.show()

# update number of food tokens with green LEDs
def lightLeds():
    for i in range(food_tokens_max):
        if (i < food_tokens):
            pixels[i] = GREEN
        else:
            pixels[i] = OFF
    pixels.show()

# play .wav file
def playFile(filename):
    wave_file = open(filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                pass

food_tokens = 10
food_tokens_max = 10
timer_4_hours = 14400
initial = monotonic()

while True:
    now = monotonic() 

    if not button_feed.value:  # button is pushed
        if food_tokens > 0:
            food_tokens = food_tokens-1
            led.value = True
            playFile("chime.wav")
            runMotor(0.1)
        else:
            playFile("chime.wav")
            errorBlink()
        print(food_tokens)
    else:
        led.value = False

    if now - initial > timer_4_hours:
        if food_tokens < food_tokens_max:
            food_tokens = food_tokens+1
            playFile("come_get_it.wav")
        initial = now
        print(food_tokens)
    
    # update LEDs
    lightLeds()

    sleep(0.01)