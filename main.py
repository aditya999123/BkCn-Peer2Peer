import threading
from Broadcast import Broadcast
from Chain import Chain, get_lock, release_lock
from Transaction import txnBuffer
from Block import block_size, Block
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

CH = Chain()

while True:
	if len(txnBuffer) >= block_size:
		txns = txnBuffer[:block_size]
		txnBuffer = txnBuffer[block_size:]
		B = Block(txns, CH.blocks[-1])
		B.pow()
		get_lock()
		if B.validate(B, CH.blocks[-1]):
			CH.append_block(B)
			release_lock()
			BR.broadcast_block(B)