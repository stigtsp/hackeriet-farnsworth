import sys
import network
import time
import machine
import ubinascii
import ujson

import neopixel # for blinky flashy thingy
import CCS811 # for gas sensor

from umqtt.simple import MQTTClient


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

default = []

#ecc486 skin
#135,206,250

for i in range(8): default.append((28, 251, 255))
for i in range(8): default.append((255, 232, 150))


def standard(np):
    for i in range(np.n):
        np[i] = default[i]
    np.write()


standard(np)
time.sleep(2)

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



def on_receive(t, m):
    flash(times=1)
    blink()
    flash(times=1)



i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
s = CCS811.CCS811(i2c, addr=91)


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
            time.sleep_ms(250)
            if s.data_ready():
                print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
                # p.publish("hackeriet/environment/eCO2", str(s.eCO2), True)
                # p.publish("hackeriet/environment/tVOC", str(s.tVOC), True)
    except OSError as e:
        print("Woops, trying to do stuff again\n")




