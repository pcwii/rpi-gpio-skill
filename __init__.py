
from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util.log import LOG

# from gpiozero import LED
import RPi.GPIO as GPIO

import re
import random

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
        GPIO.setmode(GPIO.BOARD)
        self.load_data_files(dirname(__file__))
        gpio_intent = IntentBuilder("GPIOIntent").\
            require("GpioKeyword").\
            one_of("OnKeyword", "OffKeyword").build()
        self.register_intent(gpio_intent, self.handle_gpio_intent)

    def handle_gpio_intent(self, message):
        str_remainder = str(message.utterance_remainder())
        str_limits = re.findall('\d+', str_remainder)
        int_first = int(str_limits[0])
        LOG.info('The pin number requested was: ' + str(int_first))
        if (int_first > 1) and (int_first < 28):
            if "OnKeyword":
                self.gpio_on(int_first)
            if "OffKeyword":
                self.gpio_off(int_first)
        else:
            self.speak_dialog("error", data={"result": str(int_first)})

    def gpio_on(self, pin_number):
        GPIO.setup(pin_number, GPIO.OUT, initial=0)
        GPIO.output(pin_number, True)
        LOG.info('Turning On GPIO Pin Number: ' + str(pin_number))
        # led.on()
        self.speak_dialog("on", data={"result": str(pin_number)})

    def gpio_off(self, pin_number):
        #led = LED(pin_number)
        GPIO.setup(pin_number, GPIO.OUT, initial=0)
        GPIO.output(pin_number, False)
        LOG.info('Turning Off GPIO Pin Number: ' + str(pin_number))

        # led.on()
        self.speak_dialog("on", data={"result": str(pin_number)})

    def stop(self):
        pass


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return GPIOSkill()
