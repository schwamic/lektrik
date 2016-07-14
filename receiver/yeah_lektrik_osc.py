# -*- coding: utf-8 -*-
""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
"""

import OSC
import time
import threading
import serial
import serial.tools.list_ports
import struct
#++++++++++++++++++++++++++++++++++ GLOBAL VAR +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


lamp_values = []
old_lamp_values = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
clear_values = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

#++++++++++++++++++++++++++++++++++ SERIAL +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

print serial.tools.list_ports.comports()
# configure the serial connections (the parameters differs on the device you are connecting to)

# open first serial port
ser = serial.Serial() #Make sure you connect to the right serial_connection.
ser.port = 'COM3'        #Make sure you connect to the right serial port. "0" is probably the wrong one.
ser.baudrate = 9600
print ser.baudrate
ser.open() #Open the serial connection
print ser.isOpen()
print ser.name


#++++++++++++++++++++++++++++++++++ OSC +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = ('0.0.0.0', 9600)

# OSC Server. there are three different types of server.
s = OSC.OSCServer(receive_address)  # basic

# this registers a 'default' handler (for unmatched messages),
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()

# define a message-handler function for the server to call.
def action_handler(addr, tags, stuff, source):
    #print "---"
    #print "received new osc msg from %s" % OSC.getUrlStr(source)
    #print "with addr : %s" % addr
    #print "typetags %s" % tags
    #print "data %s" % stuff
    #print "old values %s" %old_lamp_values

    send_serial(stuff)

    #print "---"

# get the values from osc and send them as serials
def send_serial(osc_list):
    global lamp_values

    if isinstance(osc_list[0], str):
        #print "sweet message."
        lamp_values = list(osc_list[0])
        #print "WERTE: %s" % lamp_values
        send(lamp_values)

    elif isinstance(osc_list[0], int):
        #print "sweet number."
        #encode to binary string
        lamp_values = list(str(bin(osc_list[0]))[2:])
        send(lamp_values)

    else:
        return -1

#Interpret strings as packed binary data
def prepare_value_for_osccontroller(n):
	return struct.pack('>B', n)
#Interpret strings as packed binary data
def ser_write(n):
	ser.write(prepare_value_for_osccontroller(n))
# this goes throw the lamp_list and sends every value to the osc_to_serial_controller
def send(lamp_values):
    global old_lamp_values, clear_values

    if len(lamp_values) == 105:
        index = 1
        counter = 0
        for value in lamp_values:
            index = isLamp(index)
            if value != old_lamp_values[counter]:
                #print '---'
                #print '255'
                #print index
                #print value
                #print '---'

                ser.write(struct.pack('!B',int(255)))
                ser.write(struct.pack('!B',int(index)))
                ser.write(struct.pack('!B',int(value)))

            index = index + 1
            counter = counter +1
        old_lamp_values = lamp_values

    elif len(lamp_values) == 8:
        index = 1
        for value in clear_values:
            index = isLamp(index)
            #print '---'
            #print '255'
            #print index
            #print value
            #print '---'

            ser.write(struct.pack('!B',int(255)))
            ser.write(struct.pack('!B',int(index)))
            ser.write(struct.pack('!B',int(value)))

            index = index + 1
        old_lamp_values = clear_values

    else:
        print "wrong array"

#checks if the adress is a relais. if the adress is a relais we add a 1 to the value to get to the next adress which is a lamp
def isLamp(value):
    if value % 8 != 0:
        return value
    else:
        return value + 1
s.addMsgHandler("/print", action_handler)  # adding our function

# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr

# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread(target=s.serve_forever)
st.start()


try:
    while 1:
        time.sleep(5)

except KeyboardInterrupt:
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join()  ##!!!
    print "Done"



