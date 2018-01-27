import threading, json, time
from Broadcast import Broadcast
import Broadcast as bd
from Chain import Chain, get_lock, release_lock
from chain_utils import get_blocks, append_block
# from Transaction import Broadcast.txnBuffer
from Block import block_size, Block

CH = Chain()

BR = Broadcast()


# broadcast reciever
t1 = threading.Thread(target = BR.recieve_broadcast)

# tcp data reciever
t2 = threading.Thread(target = BR.recieve_data)

# im alive broadcast
t3 = threading.Thread(target = BR.imAlive)

# im alive broadcast
t4 = threading.Thread(target = BR.shareChain)

t1.start()
t2.start()
t3.start()
t4.start()

while True:
	# Broadcast.txnBuffer
	# print "length:", len(Broadcast.txnBuffer)
	# print "len :",len(bd.txnBuffer)
	time.sleep(1)	
	if len(bd.txnBuffer) >= block_size:
		txns = bd.txnBuffer[:block_size]
		bd.txnBuffer = bd.txnBuffer[block_size:]
		# print "bbbbbbbbbblock: ", get_blocks()
		B = Block(txns, get_blocks()[-1])
		B.pow()
		# get_lock()
		if B.validate(B, get_blocks()[-1]):
			append_block(B)
			print "I solved It"
			# release_lock()
			BR.broadcast_block(B)
			print "Broadcasted"