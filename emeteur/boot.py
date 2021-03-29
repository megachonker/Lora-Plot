from network import LoRa#pour géré le module lora
import socket 			#pour envoyer des trames
from pytrack import Pytrack
from L76GNSV4 import L76GNSS
import machine, time
import pycom

pycom.heartbeat(False)  # disable the heartbeat LED
pycom.rgbled(0x010005)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=1,preamble=10, sf=12,tx_power=20,coding_rate=1)#
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora

print("up")
py = Pytrack()
L76 = L76GNSS(pytrack=py)
L76.setAlwaysOn()

print("print gsv")
# returns the info about sattelites in view at this moment
# even without the gps being fixed
print(L76.gps_message('GSV',debug=True))

print("gga")
# returns the number of sattelites in view at this moment
# even without the gps being fixed
print(L76.gps_message('GGA',debug=True)['NumberOfSV'])

L76.get_fix(debug=True)
pycom.heartbeat(0)
if L76.fixed():
    pycom.rgbled(0x000f00)
else:
    pycom.rgbled(0x0f0000)
print("coordinates")
# returns the coordinates
# with debug true you see the messages parsed by the
# library until you get a the gps is fixed
print(L76.coordinates(debug=True))
print(L76.getUTCDateTime(debug=True))

while True:
	coordoner=L76.coordinates(debug=False)
	print(coordoner)
	if coordoner[0]==None or coordoner[1]==None:
		pycom.rgbled(0x30000b)
	else:
		print("coordoner:"+coordoner[0]+","+coordoner[1])
		data=pack('8h8h',coordoner[0],coordoner[1])
		print(data)
		s.send(data)
		pycom.rgbled(0x003011)
