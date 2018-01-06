Vanligvis er umqtt installert i micropython, for ESP32 måtte jeg paste umqtt.simple inn i main.py. import funka ikke når det var en egen fil.


Firmware flash (ESP32):

esptool.py --port /dev/cu.usbmodem1411 --baud 115200 erase_flash
esptool.py --port /dev/cu.usbmodem1411 --baud 115200 write_flash -z 0x1000 esp32-20180106-v1.9.3-238-g42c4dd09.bin


Ampy last opp kode:
  ampy  -p /dev/cu.usbmodem1411 -b 115200 put main.py


CLI:
  screen /dev/cu.usbmodem1411 115200



TODO: Bruke umqtt, og NodeMCU/ESP8266 (må bytte pin fra 25 til noe annet som mapper på NodeMCU)
