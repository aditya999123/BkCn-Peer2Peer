import select, socket, time, json

NORMAL_PORT = 8002
BROADCASTING_PORT = 8001
bufferSize = 2048 # may be changed for faster responses (incase of smaller messages)

ALIVE_OBJ = {
	"message" : "",
	"myIp" : ""
	}

NEW_BLOCK_OBJ = {
	"message" : "",
	"block": ""
	}

imalive = "I'm alive"
newTransaction = "new Transaction"
newBlock = "new Block"

class Broadcast:
	def __init__(self):
		self.peers = []
		self.myIp = self.getMyIp()

	def getMyIp(self):
		tmp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tmp_sock.connect(('www.google.com', 80))
		return tmp_sock.getsockname()[0]

	def message(self, message):
		broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		broadcast_socket.bind(('', 0))
		broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		broadcast_socket.sendto(message, ('<broadcast>', BROADCASTING_PORT))
		# print "broadcasted"

	def imAlive(self):
		while True:
			self.message(imalive_Obj%(imalive, self.myIp))
			# wait for 10s before broadcasting again
			# to be able to break the thread with ctrl-c
			for i in range(10):
				sleep(1)

	def recieve_broadcast(self):
		reciever_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		reciever_socket.bind(('<broadcast>', BROADCASTING_PORT))
		reciever_socket.setblocking(0)
		while True:
			try:
				result = select.select([reciever_socket], [], [], 2)
				msg = result[0][0].recv(bufferSize)
				# print msg
				if msg:
					obj = json.loads(msg)
					try:
						if(obj['message'] == imalive):
							if obj['myIp'] not in self.peers and obj['myIp'] != self.myIp:
								self.peers.append(obj['myIp'])

						if(obj['message'] == newTransaction):
							txnBuffer.append(Transaction(obj['senderPubKey'], obj['recieverPubKey'], obj['hashed']))
					except:
						print "message is not a json \n msg: ",msg
			except:
				# if no connection is avialable
				pass

	def broadcast_block(self, block):
		for peer in self.peers:
			# multi programming can be used in here(future plans)
			block = json.dumps(block)
			data = newBlock_obj%(newBlock, block)
			self.transmit_data(peer, data)

	def transmit_data(self, Ip, data):
		transmit_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			transmit_socket.connect((Ip, NORMAL_PORT))
			total_sent = 0
			while(total_sent < len(data)):
				# print "total_sent:", total_sent
				# print "data: ", len(data)
				sent = transmit_socket.send(data[total_sent:])
				# print "sent:",sent
				total_sent = total_sent + sent
				if sent == 0:
					break
		except Exception as e:
			print str(e)
			# disconnected peer
			self.peers.remove(Ip)
	
	def recieve_data(self):
		reciever_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		reciever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		reciever_socket.bind((self.myIp, NORMAL_PORT))
		reciever_socket.setblocking(0)
		reciever_socket.listen(2)

		while True:
			try:
				result = select.select([reciever_socket],[],[],2)
				reciever_socket=result[0][0]
				conn, addr = reciever_socket.accept()
				if addr[0] != self.myIp:
					msg = ''
					while 1:
						data = conn.recv(bufferSize)
						if not data: break
						msg = msg + data
					obj = json.loads(msg)
			except Exception as e:
				pass