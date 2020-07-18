# AUTOMATED CAT FOOD DISPENSER
# AUTHOR: Joel Huffman
# LAST UPDATED: 7/18/2020
# PURPOSE: Allow cats to dispense serve themselves dry food pellets by depressing a
# push button. To prevent gourging. food will be dispensed in small quantites and only
# if specific criteria are met.
# RULES: The day starts with 10 food tokens at 6AM
# - At 6AM the number of food tokens is set to 10
# - Each button press removes a food token, dispenses 1 oz of dry food and plays sound
# - If no food tokens remain, a button press only plays a sad trombone sound
# - If a button press occurs within 10 minutes of a prior button press it does not 
# remove a food token or dispense food


from time import sleep, monotonic
import board
from digitalio import DigitalInOut, Pull, Direction
from neopixel import NeoPixel

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

food_tokens = 10
food_tokens_max = 10
timer_5_min = 60
initial = monotonic()

while True:
    now = monotonic() 

    if not button_feed.value:  # button is pushed
        if food_tokens > 0:
            food_tokens = food_tokens-1
            led.value = True
            runMotor(0.1)
        else:
            errorBlink()
        print(food_tokens)
    else:
        led.value = False

    if now - initial > timer_5_min:
        if food_tokens < food_tokens_max:
            food_tokens = food_tokens+1
        initial = now
        print(food_tokens)
    
    # update LEDs
    lightLeds()

    sleep(0.01)