import threading, json
from Broadcast import Broadcast
from Chain import Chain, get_lock, release_lock
from chain_utils import get_blocks, append_block
from Transaction import txnBuffer
from Block import block_size, Block

CH = Chain()

BR = Broadcast()


# broadcast reciever
t1 = threading.Thread(target = BR.recieve_broadcast)

# tcp data reciever
t2 = threading.Thread(target = BR.recieve_data)

# im alive broadcast
t3 = threading.Thread(target = BR.imAlive)

t1.start()
t2.start()
t3.start()

while True:
	# print "length:", len(txnBuffer)
	if len(txnBuffer) >= block_size:
		txns = txnBuffer[:block_size]
		txnBuffer = txnBuffer[block_size:]
		# print "bbbbbbbbbblock: ", get_blocks()
		B = Block(txns, get_blocks()[-1])
		B.pow()
		get_lock()
		if B.validate(B, get_blocks()[-1]):
			append_block(B)
			release_lock()
			BR.broadcast_block(B)