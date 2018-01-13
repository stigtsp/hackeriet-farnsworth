import network
import time
import machine
import neopixel
import upip
import ujson
import ubinascii
from umqtt.robust import MQTTClient
import sys

station = network.WLAN(network.STA_IF)
 
station.active(True)
station.connect("hackeriet.no","hackeriet.no")

while not station.isconnected():  
    machine.idle() 

print(station.ifconfig())

# Pin 0 is D3 on the NodeMCU, 16 is the number of neopixels
np = neopixel.NeoPixel(machine.Pin(0), 16)

default = []
for i in range(8): default.append((255,0,255))
for i in range(8): default.append((0,255,0))


def standard(np):
    for i in range(np.n):
        np[i] = default[i]
    np.write()


standard(np)
time.sleep(2)

SERVER = "iot.eclipse.org"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"/hackeriet/farnsworth"


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
    if m == b'flash':
      flash()
    elif m == b'blink':
      blink()
    elif m == b'reset':
      machine.reset()
    else:
      try:
        msg = ujson.loads(m)
        apply_colors(msg)
      except ValueError:
        print("JSON error: " + str(m));
        flash((255,0,0),1)
      except:
        flash((128,128,0),1)
        print("Some Error")
           

def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.set_callback(on_receive)
    c.connect()
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))
    while True:
        c.check_msg()
        machine.idle()

while True:
  try:
    main()
  except:
    pass
  time.sleep(1)

