import paho.mqtt.client as mqtt
from string import Template
import requests, json, datetime, pytz

url = 'http://loki-mqtt:3101/api/prom/push'
host = 'listener.py'

def on_connect(client, userdata, flags, rc):
	print("CONNECTED"+str(rc))
	client.subscribe("#")

def status(type, sens):
	stat = ""
	if type == "DOOR_OK":
		if sens == "0":
			stat = "Buka"
		else :
			stat = "Tutup"
	elif type == "PROX_OK":
		if sens == "0":
			stat = "Ada Tabung"
		else :
			stat = "Kosong"
	else:
		stat = "YNTKTS"
	return stat

def message_type(payload):
	parser = payload.decode('utf-8')
	parser = parser.split(',')
	if parser[0] == "DOOR_OK" or parser[0] == "PROX_OK":
		d = {'loker1' : status(parser[0],parser[1]), 'loker2' : status(parser[0],parser[2]),'loker3' : status(parser[0],parser[3]),'loker4' : status(parser[0],parser[4]),'loker5' : status(parser[0],parser[5]),'loker6' : status(parser[0],parser[6]),'loker7' : status(parser[0],parser[7]),'loker8' : status(parser[0],parser[8]),'loker9' : status(parser[0],parser[9]),'loker10' : status(parser[0],parser[10]),'loker11' : status(parser[0],parser[11]),'loker12' : status(parser[0],parser[12]),'loker13' : status(parser[0],parser[13]),'loker14' : status(parser[0],parser[14])}
		line = '''
		Loker 1: {loker1}
		Loker 2: {loker2}
		Loker 3: {loker3}
		Loker 4: {loker4}
		Loker 5: {loker5}
		Loker 6: {loker6}
		Loker 7: {loker7}
		Loker 8: {loker8}
		Loker 9: {loker9}
		Loker 10: {loker10}
		Loker 11: {loker11}
		Loker 12: {loker12}
		Loker 13: {loker13}
		Loker 14: {loker14}
		'''.format(**d)
		return line
	else :
		return "YNTKTS"

def on_message(client, userdata, msg):
	ms = msg.payload
	mt = message_type(ms)
	curdat = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
	curdat = curdat.isoformat('T')
	headers = {
    'Content-type': 'application/json'
	}
	payload = {
	    'streams': [
	        {
	            'labels': '{source=\"KiosMQTT\",topic = \"' + msg.topic + '\", job=\"all-topics-listener\", host=\"' + host + '\"}',
	            'entries': [
	                {
	                    'ts': curdat,
	                    'line': mt
	                }
	            ]
	        }
	    ]
	}
	print(payload,"\n")
	payload = json.dumps(payload)
	a = requests.post(url,data=payload,headers=headers)
	print("response: "+str(a))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("gliggy", "protokolnyamuk")
client.connect("172.17.0.1", 1883, 60)

client.loop_forever()
