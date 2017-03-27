from pysony import SonyAPI, payload_header
import urllib2
camera = SonyAPI()
camera.QX_ADDR = "http://192.168.122.1:8080"
# print(camera.getAvailableApiList())
live = camera.startLiveview()
liveview_url = live['result'][0]
f = urllib2.urlopen("http://192.168.122.1:8080/liveview/liveviewstream")
while 1:
	data = f.read(8)
	data = f.read(128)
	payload = payload_header(data)
	live = open('./static/live.jpg', 'w')
	live.write(f.read(payload['jpeg_data_size']))
	live.close()
	# if t == 0:
	# 	save = shutil.copy('./static/live.jpg', './static/saved/' + str(int(time.time()))+'.jpg')
	# 	t = timer
	f.read(payload['padding_size'])
	# time.sleep(1)