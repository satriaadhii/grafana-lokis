import paho.mqtt.client as mqtt
import requests, json, datetime, pytz

url = 'http://172.17.0.4:3101/api/prom/push'
host = 'loki-mqtt'
curdat = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
curdat = curdat.isoformat('T')

def on_connect(client, userdata, flags, rc):
	print("CONNECTED"+str(rc))
	client.subscribe("#")

def on_message(client, userdata, msg):
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
	                    'line': '[INFO] ' + str(msg.payload)
	                }
	            ]
	        }
	    ]
	}
	print(payload)
	payload = json.dumps(payload)
	a = requests.post(url,data=payload,headers=headers)
	print(a)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("gliggy", "protokolnyamuk")
client.connect("host.docker.internal", 1883, 60)

client.loop_forever()
