# Hva er dette?

Salves prosjekt som han har jobbet med på Attraktor (Hamburg), Nürnberg
Fablab (Nürnberg) og på Hackeriet.


For å sette opp:

0. Plugg 16 neopixler til D3, 3v3 og GND
1. Flash en ESP8266 med micropython
2. Konfigurer wifi og mqtt variabler i farnsworth.json
3. Last opp kode med ampy
```shell
    pip install adafruit-ampy
    export AMPY_PORT=/dev/ttyUSB0
    ampy put farnsworth.json farnsworth.json
	ampy put main.py main.py
```
4. Reset devicet ved å trykke på reset knappen 

5. Send mqtt-melding til konfigurert mqtt server og topic:
```shell
	mosquitto_pub -t $MQTT_TOPIC -h $MQTT_SERVER -m "foobar"
```
# Takk til

- Gjengen på Attraktor
- Gjengen på Fablab Nürnberg
- stigo@hackeriet
- Alle andre som har gitt råd og tipset!
