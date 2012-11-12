#!/bin/sh
#
# This is a simple script which initalizes the required gpio pin
# and writes down a few strings.
#
#
#
##############################################

gpio_pin=14
export GPIO_PIN=gpio$gpio_pin

#Is gpio aviable?
if [ ! -d "/sys/class/gpio/gpio$gpio_pin"  ]
then
        echo "$gpio_pin" > /sys/class/gpio/export
        echo out > "/sys/class/gpio/gpio$gpio_pin/direction"
        echo 0 > "/sys/class/gpio/gpio$gpio_pin/value"
        echo "if applied"
fi

#Starting the "embedded projects" app

dog-app -w "embedded" -n
dog-app -w "projects" -o 194  
dog-app -s "+5"
dog-app -s "-5"
dog-app -n
dog-app -w "First Display App in use" -o 128
dog-app -s -10
dog-app -n -s 10








