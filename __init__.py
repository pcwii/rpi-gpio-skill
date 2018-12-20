from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util.log import LOG

import RPi.GPIO as GPIO

import re

__author__ = 'PCWii'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)


# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class GPIOSkill(MycroftSkill):

    # The constructor of the skill, which calls Mycroft Skill's constructor
    def __init__(self):
        super(GPIOSkill, self).__init__(name="GPIOSkill")

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.io_pins = [3, 5, 7, 29, 31, 26, 24, 21, 19, 23, 32, 33, 8, 10, 36, 11, 12, 35, 38, 40, 15, 16, 18, 22, 37, 13]
        GPIO.setmode(GPIO.BOARD)
        self.load_data_files(dirname(__file__))
        gpio_intent = IntentBuilder("GPIOIntent").\
            require("GpioKeyword").\
            one_of("OnKeyword", "OffKeyword").build()
        self.register_intent(gpio_intent, self.handle_gpio_intent)

    def handle_gpio_intent(self, message):
        str_remainder = str(message.utterance_remainder())
        if str_remainder.find('for') or str_remainder.find('four'):
            str_limits = [4]
        else:
        str_limits = re.findall('\d+', str_remainder)
        if str_limits:
            gpio_request = int(str_limits[0])
            if (gpio_request > 1) and (gpio_request < 28):
                pin_index = gpio_request - 2
                board_pin = self.io_pins[pin_index]
                LOG.info('The pin number requested was: ' + str(board_pin))
                if "OnKeyword" in message.data:
                    self.gpio_on(board_pin, gpio_request)
                if "OffKeyword" in message.data:
                    self.gpio_off(board_pin, gpio_request)
            else:
                self.speak_dialog("error", data={"result": str(gpio_request)})
        else:
            self.speak('No GPIO Pin was specified')

    def gpio_on(self, board_number, gpio_request_number):
        GPIO.setup(board_number, GPIO.OUT, initial=0)
        GPIO.output(board_number, True)
        LOG.info('Turning On GPIO Number: ' + str(gpio_request_number))
        self.speak_dialog("on", data={"result": str(gpio_request_number)})

    def gpio_off(self, board_number, gpio_request_number):
        GPIO.setup(board_number, GPIO.OUT, initial=0)
        GPIO.output(board_number, False)
        LOG.info('Turning Off GPIO Number: ' + str(gpio_request_number))
        self.speak_dialog("off", data={"result": str(gpio_request_number)})

    def stop(self):
        pass


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return GPIOSkill()
