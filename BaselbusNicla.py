from pyb import UART, LED

import sensor
import time
import pyb
import math

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.ioctl(sensor.IOCTL_SET_FOV_WIDE, True)
sensor.set_framesize(sensor.HQVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
sensor.set_vflip(True)  # Flip the image vertically

r_LED = LED(1)  # The red LED
g_LED = LED(2)  # The green LED
b_LED = LED(3)  # The blue LED
g_LED.on()
r_LED.off()
b_LED.off()
clock = time.clock()  # Create a clock object to track the FPS.
uart = UART("LP1", 115200, timeout_char=2000) # (TX, RX) = (P1, P0) = (PB14, PB15)

# Thresholds and constants for blob detection
thresholdsGreenBall = (100, 0, -128, -17, -128, 127)
#(0, 100, -128, 127, -128, -21)
#(0, 100, -128, 127, -18, 127)
#

def checksum(arr, initial= 0):
    """ The last pair of byte is the checksum on iBus
    """
    sum = initial
    for a in arr:
        sum += a
    checksum = 0xFFFF - sum
    chA = checksum >> 8
    chB = checksum & 0xFF
    return chA, chB

def IBus_message(message_arr_to_send):
    msg = bytearray(32)
    msg[0] = 0x20
    msg[1] = 0x40
    for i in range(len(message_arr_to_send)):
        msg_byte_tuple = bytearray(message_arr_to_send[i].to_bytes(2, 'little'))
        msg[int(2*i + 2)] = msg_byte_tuple[0]
        msg[int(2*i + 3)] = msg_byte_tuple[1]

    # Perform the checksume
    chA, chB = checksum(msg[:-2], 0)
    msg[-1] = chA
    msg[-2] = chB

    uart.write(msg)

def refreshIbusConnection():
    if uart.any():
        uart_input = uart.read()

while True:

    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot()  # Take a picture and return the image.
    print(clock.fps())

   # Blob detection
    blobs = img.find_blobs([thresholdsGreenBall], merge=True)
    for blob in blobs:
        img.draw_rectangle(blob.rect(), color=(0, 255, 0))
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 255, 0))


    width = sensor.width()
    height = sensor.height()

    # calculate the middle coordinates
    middle_x = width // 2
    middle_y = height // 2

    blobx = middle_x
    bloby = middle_y
    blobw = width
    blobh = height

    flag = 0
    if (blobs):
        g_LED.off()
        r_LED.off()
        b_LED.on()
        flag = 1 # when a color is detected make this flag 1
        blobx = blob.cx()
        bloby = blob.cy()
        blobw = blob.w()
        blobh = blob.h()
    else:
        g_LED.on()
        r_LED.off()
        b_LED.off()
        blobx = middle_x
        bloby = middle_y
        blobw = width
        blobh = height

    pixels_x = blobx # put your x center in pixels
    pixels_y = bloby # put your y center in pixels
    pixels_w = blobw # put your width in pixels (these have almost no affect on control (for now))
    pixels_h = blobh # put your height center in pixels (these have almost no affect on control (for now))

    messageToSend = [flag, pixels_x, pixels_y, pixels_w, pixels_h]

    IBus_message(messageToSend)
    refreshIbusConnection()
#from pyb import UART, LED

#import sensor
#import time

#sensor.reset()  # Reset and initialize the sensor.
#sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
#sensor.ioctl(sensor.IOCTL_SET_FOV_WIDE, True)
#sensor.set_framesize(sensor.HQVGA)  # Set frame size to QVGA (320x240)
#sensor.skip_frames(time=2000)  # Wait for settings take effect.

#r_LED = LED(1)  # The red LED
#g_LED = LED(2)  # The green LED
#b_LED = LED(3)  # The blue LED
#g_LED.on()
#r_LED.off()
#b_LED.off()
#clock = time.clock()  # Create a clock object to track the FPS.
#uart = UART("LP1", 115200, timeout_char=2000) # (TX, RX) = (P1, P0) = (PB14, PB15)

#def checksum(arr, initial= 0):
#    """ The last pair of byte is the checksum on iBus
#    """
#    sum = initial
#    for a in arr:
#        sum += a
#    checksum = 0xFFFF - sum
#    chA = checksum >> 8
#    chB = checksum & 0xFF
#    return chA, chB

#def IBus_message(message_arr_to_send):
#    msg = bytearray(32)
#    msg[0] = 0x20
#    msg[1] = 0x40
#    for i in range(len(message_arr_to_send)):
#        msg_byte_tuple = bytearray(message_arr_to_send[i].to_bytes(2, 'little'))
#        msg[int(2*i + 2)] = msg_byte_tuple[0]
#        msg[int(2*i + 3)] = msg_byte_tuple[1]

#    # Perform the checksume
#    chA, chB = checksum(msg[:-2], 0)
#    msg[-1] = chA
#    msg[-2] = chB

#    uart.write(msg)

#def refreshIbusConnection():
#    if uart.any():
#        uart_input = uart.read()




#while True:
#    ############### Color detection here ###############

#    #put color detection and such here


#    clock.tick()  # Update the FPS clock.
#    img = sensor.snapshot()  # Take a picture and return the image.
#    print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
#    # to the IDE. The FPS should increase once disconnected.


#    color_is_detected = False # replace this with your method


#    flag = 0
#    if (color_is_detected):
#        g_LED.off()
#        r_LED.off()
#        b_LED.on()
#        flag = 1 # when a color is detected make this flag 1
#    else:
#        g_LED.on()
#        r_LED.off()
#        b_LED.off()
#    pixels_x = 0 # put your x center in pixels
#    pixels_y = 0 # put your y center in pixels
#    pixels_w = 0 # put your width in pixels (these have almost no affect on control (for now))
#    pixels_h = 0 # put your height center in pixels (these have almost no affect on control (for now))
#    ###############################




#    messageToSend = [flag, pixels_x, pixels_y, pixels_w, pixels_h]

#    IBus_message(messageToSend)
#    refreshIbusConnection()
