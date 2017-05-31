#!/bin/bash

# The serial port (something like /dev/ttyACM0)
# If the baud rate needs changing (eg to 9600)
# stty -F /dev/PORT_NAME_HERE 9600 cread
# or do it in com port
DIR="/tmp/f"

# The hex codes
ESC=1B
ICC=51
CONFIGURE_DATA_RESPONSE=4A
REQUEST_DATA=24
PAW=00
Q=01
V=03
# Uses the program "bc" to sum hexcodes
CHKSUM=$(echo "obase=16;ibase=16;$ESC+$CONFIGURE_DATA_RESPONSE+$REQUEST_DATA+$PAW+$Q+$V" | bc)
CR=0D

# Command to send
COMMAND="$ESC$CONFIGURE_DATA_RESPONSE$REQUEST_DATA$PAW$Q$V$CHKSUM$CR"

while true; do
    echo "$COMMAND" >> $DIR
    sleep 2
done
