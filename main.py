import threading
from Broadcast import Broadcast

B = Broadcast()

# broadcast reciever
t1 = threading.Thread(target = B.recieve_broadcast)

# tcp data reciever
t2 = threading.Thread(target = B.recieve_data)

# im alive broadcast
t3 = threading.Thread(target = B.imAlive)

t1.start()
t2.start()
t3.start()

while True:
	msg = raw_input()
	B.broadcast_block(msg)
	print "len msg", len(msg)