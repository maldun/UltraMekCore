from . import client
import json

with open("UltraMekPy/config.json",'r') as conf:
    conf_dict = json.load(conf)
    client = client.UDPClient(**conf_dict['connection'])
    client.send("Hello from Python!")
    data, (recv_ip,recv_port) = client.recieve(return_port_info=True)
    print(f"Recieved: '{data.decode()}' {recv_ip}:{recv_port}")
