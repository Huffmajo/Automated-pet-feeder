# AUTOMATED CAT FOOD DISPENSER
# AUTHOR: Joel Huffman
# LAST UPDATED: 7/8/2020
# PURPOSE: Allow cats to dispense serve themselves dry food pellets by depressing a
# push button. To prevent gourging. food will be dispensed in small quantites and only
# if specific criteria are met.
# RULES: The day starts with 10 food tokens at 6AM
# - At 6AM the number of food tokens is set to 10
# - Each button press removes a food token, dispenses 1 oz of dry food and plays sound
# - If no food tokens remain, a button press only plays a sad trombone sound
# - If a button press occurs within 10 minutes of a prior button press it does not 
# remove a food token or dispense food


from time import sleep
import board
from digitalio import DigitalInOut, Pull, Direction

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

food_tokens = 10
food_tokens_max = 10

# runs motor for 'duration' (in seconds) then turns off motor
def runMotor(duration):
	motor.value = True
	sleep(duration)
	motor.value = False


while True:
    if not button_feed.value:  # button is pushed
        led.value = True
        runMotor(2)
    else:
        led.value = False
    sleep(0.01)