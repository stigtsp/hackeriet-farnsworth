import sys
import network
import time
import machine
import ubinascii
import ujson

import neopixel # for blinky flashy thingy

from umqtt.simple import MQTTClient
from machine import Timer



with open('farnsworth.json') as fp:
    config = ujson.loads(fp.read())

station = network.WLAN(network.STA_IF)


station.active(True)
station.connect(config['wifi']['ssid'],config['wifi']['psk'])

while not station.isconnected():
    machine.idle()

ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
  ap_if.active(False)

# Pin 0 is D3 on the NodeMCU, 16 is the number of neopixels
np = neopixel.NeoPixel(machine.Pin(0), 16)


fade_i=0
default =   [(28, 251, 255)]*8+\
            [(255, 232, 150]*8


def standard(np):
    for i in range(np.n):
        np[i] = default[i]
    np.write()


standard(np)
time.sleep(1)

CLIENT_ID = ubinascii.hexlify(machine.unique_id())

def apply_colors(m):
   for i in range(16):
       try:
           t=m[i]
           np[i]=t
           default[i]=t
       except IndexError:
           pass
   np.write()


def flash(c=(255,255,255),times=4):
  for i in range(times * np.n):
      for j in range(np.n):
          np[j] = (0, 0, 0)
          np[i % np.n] = c
      np.write()
  time.sleep_ms(10)
  apply_colors(default)

def bounce():
    for i in range(4 * np.n):
        for j in range(np.n):
            np[j] = (0, 0, 128)
        if (i // np.n) % 2 == 0:
            np[i % np.n] = (0, 0, 0)
        else:
            np[np.n - 1 - (i % np.n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

def blink():
  for i in range(0, 4 * 256, 8):
    for j in range(np.n):
        if (i // 256) % 2 == 0:
            val = i & 0xff
        else:
            val = 255 - (i & 0xff)
        np[j] = (val, 0, 0)
    np.write()
  apply_colors(default)

def fade_one(i):
    n = np.n
    for j in range(n):
        val = i
        d = default[j]
        np[j] = (int(d[0] * (val/255)), int(d[1] * (val/255)),  int(d[2] * (val/255)))
        np.write()



def fade_timer(t=False):
    global fade_i
    global fade_going

    if not fade_going:
        return fade_i

    fade_one(abs(fade_i))
    if fade_i >= 255:
        fade_i = -255
    else:
        fade_i = fade_i+2
    return fade_i
    

#timer.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(2))
timer = Timer(-1)
fade_i=0
fade_going=True
timer.init(period=50, mode=Timer.PERIODIC, callback=lambda t: fade_timer(t))





def on_receive(t, m):
    global fade_going
    fade_going=False
    flash(times=1)
    blink()
    flash(times=3)
    blink()
    flash(times=1)
    fade_going=True


while True:
    try:
        c = MQTTClient(client_id = CLIENT_ID,
                       server     = config['mqtt']['server'],
                       user       = config['mqtt']['user'],
                       password   = config['mqtt']['password'],
                       port       = config['mqtt']['port'],
                       ssl        = config['mqtt']['ssl']
        )
        c.set_callback(on_receive)
        c.connect()
        c.subscribe(config['mqtt']['topic'])
        
        while True:
            c.wait_msg()

    except OSError as e:
        print("Woops, trying to do stuff again\n")




