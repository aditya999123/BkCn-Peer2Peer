import select, socket, time, json
from Transaction import Transaction
from general import stringToObj
from Block import Block
from Chain import get_lock, release_lock
from chain_utils import get_blocks, append_block
txnBuffer = []
NORMAL_PORT = 8002
BROADCASTING_PORT = 8001
DEDICATED_PORT = 8003

bufferSize = 2048 # may be changed for faster responses (incase of smaller messages)

iMAliveMsg = "I'm alive"
newTransactionMsg = "new Transaction"
newBlockMsg = "new Block"
getBlocks = "get Block"

IMALIVE_OBJ = {
	"message" : iMAliveMsg,
	"myIp" : ""
	}

NEW_BLOCK_OBJ = {
	"message" : newBlockMsg,
	"block": ""
	}

BLOCKS = {
	"blocks":[]
}

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
			IMALIVE_OBJ['myIp'] = self.myIp
			self.message(json.dumps(IMALIVE_OBJ))
			# wait for 10s before broadcasting again
			# to be able to break the thread with ctrl-c
			for i in range(10):
				time.sleep(1)

	def recieve_broadcast(self):
		global txnBuffer
		reciever_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		reciever_socket.bind(('<broadcast>', BROADCASTING_PORT))
		reciever_socket.setblocking(0)
		while True:
			try:
				result = select.select([reciever_socket], [], [], 2)
				msg = result[0][0].recv(bufferSize)
				# print msg
				if msg:
					try:
						obj = stringToObj(msg)
						if(obj.message == iMAliveMsg):
							if obj.myIp not in self.peers and obj.myIp != self.myIp:
								self.peers.append(obj.myIp)

						if(obj.message == newTransactionMsg):
							print "transaction recieved"
							txn = Transaction(obj.sender_public_key, obj.reciever_public_key, obj.product_hash, obj.hashed)
							if txn.validated and txn.authenticated:
								print "validated"
								txnBuffer.append(txn)
					except Exception as e:
						print "msg: ",msg
						print "e: ", str(e)

			except:
				# if no connection is avialable
				pass

	def broadcast_block(self, block):
		for peer in self.peers:
			# multi programming can be used in here(future plans)
			NEW_BLOCK_OBJ['block'] = block.toJSON()
			data = json.dumps(NEW_BLOCK_OBJ)
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
				# print "timed"
				reciever_socket=result[0][0]
				conn, addr = reciever_socket.accept()
				if addr[0] != self.myIp:
					msg = ''
					while 1:
						data = conn.recv(bufferSize)
						if not data: break
						msg = msg + data
					print "from: ",addr, msg
					obj = stringToObj(msg)
					if obj.message == newBlockMsg:
						block = obj.block
						B = Block()
						B.__jsonToObj__(block)
						get_lock()
						if B.validate(B, get_blocks()[-1]):
							append_block(B)
							release_lock()
							B.broadcast_block(B)
							for txn in B.txns:
								if txn in txnBuffer:
									txnBuffer.remove(txn)
			except Exception as e:
				pass

	def shareChain(self):
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind(('', DEDICATED_PORT))
		# serversocket.setblocking(0)
		serversocket.listen(2)
		while True:
			print "1"
			conn, addr = serversocket.accept()
			# blocks = []
			# for block in get_blocks():
			# 	blocks.append()
			data  = {
				"blocks":get_blocks(True)
			}
			# print data
			conn.send(json.dumps(data))
			conn.close()
