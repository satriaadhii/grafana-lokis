import paho.mqtt.client as mqtt
import requests, json, datetime, pytz

url = 'http://loki-mqtt:3101/api/prom/push'
host = 'listener.py'

def on_connect(client, userdata, flags, rc):
	print("CONNECTED"+str(rc))
	client.subscribe("#")

def on_message(client, userdata, msg):
	ms = msg.payload
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
	                    'line': ms.decode('utf-8')
	                }
	            ]
	        }
	    ]
	}
	print(payload)
	payload = json.dumps(payload)
	a = requests.post(url,data=payload,headers=headers)
	print("response: "+str(a))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("gliggy", "protokolnyamuk")
client.connect("172.17.0.1", 1883, 60)

client.loop_forever()
