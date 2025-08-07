import socket

broker_ip = str(socket.gethostbyname('broker.hivemq.com'))
broker_port = '1883'
username = ''  # if not needed - delete
password = ''  # if not needed - delete
conn_time = 0  # 0 stands for endless

room_ID = "Playroom "  # will be different in every room
topic = "airQuality/areas/" + room_ID
relay_topic = topic + "/relay"
DHT_topic = topic + "/DHT"
AQS_topic = topic + "/AQS"

db_init =  False   #False # True if need reinit
db_name = 'airQuality.db' # SQLite
