# Hva er dette?

Salves prosjekt som han har jobbet med på Attraktor (Hamburg), Nürnberg
Fablab (Nürnberg) og på Hackeriet.


For å sette opp:

0. Plugg 16 neopixler til D3, 3v3 og GND
1. Flash en ESP8266 med micropython
2. Last opp main.py med ampy eller webrepl_cli.py

	ampy  -p $PORT put main.py
	
	webrepl_cli.py -p $PASSWD main.py $IP:/main.py	

3. Reset devicet ved å trykke på reset knappen 

4. Send mqtt-melding med api kommandoer, f.eks:
	
	mosquitto_pub -t '/hackeriet/farnsworth' -h $MQTT_SERVER -m "blink"

# Takk til

- Gjengen på Attraktor
- Gjengen på Fablab Nürnberg
- stigo@hackeriet
- Alle andre som har gitt råd og tipset!
