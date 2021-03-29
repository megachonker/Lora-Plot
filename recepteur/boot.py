from mqtt import MQTTClient
from network import WLAN
import os
import machine
import time
from network import LoRa#pour géré le module lora
import socket 			#pour envoyer des trames
import pycom			#Pour Mieux dormire la nuit DIsable Blink  !
from struct import *

uart = machine.UART(0, 115200)
os.dupterm(uart)

pycom.heartbeat(False)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=1,preamble=10, sf=12,tx_power=20,coding_rate=1)#
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora


known_nets = {
    'wifilocal': {'pwd': 'PWD','wlan_config':  ('192.168.x.x', '255.255.x.x', '192.168.x.x', '1.1.1.1')},
    'hotspot': {'pwd': 'PWD'}
}

if machine.reset_cause() != machine.SOFT_RESET:
    from network import WLAN
    wlan = WLAN()
    wlan.mode(WLAN.STA)
    original_ssid = wlan.ssid()
    original_auth = wlan.auth()

    print("Scanning for known wifi nets")
    available_nets = wlan.scan()
    nets = frozenset([e.ssid for e in available_nets])

    known_nets_names = frozenset([key for key in known_nets])
    net_to_use = list(nets & known_nets_names)
    try:
        net_to_use = net_to_use[0]
        net_properties = known_nets[net_to_use]
        pwd = net_properties['pwd']
        sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
        if 'wlan_config' in net_properties:
            wlan.ifconfig(config=net_properties['wlan_config'])
        wlan.connect(net_to_use, (sec, pwd), timeout=10000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print("Connected to "+net_to_use+" with IP address:" + wlan.ifconfig()[0])

    except Exception as e:
        print("Failed to connect to any known network, going into AP mode")
        wlan.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)

# import network
# server = network.Server()
# server.deinit() # disable the server
# server.init(login=('user', 'password'), timeout=600

client = MQTTClient("deviceid", "x.x.x.x",user="xxxx", password="xxx", port=xxxx)
client.connect()



client.publish(topic="coordoner", msg="lon,lat,rssi,snr")
print("lon,lat,rssi,snr")
while True:
    data=s.recv(16)#corriger la  taille  d'un packet !
    try:
        coordoner=unpack('ff',data)
        #               lont    ,          lat               ,     rssi              ,     snr
        data=str(coordoner[0])+","+str(coordoner[1])+","+str(lora.stats()[1])+","+str(lora.stats()[2])
        print(data)
        client.publish(topic="coordoner", msg=data)
        time.sleep(1)
    except Exception as e:
        print("exeption:"+str(data))
