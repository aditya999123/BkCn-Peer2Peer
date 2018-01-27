from general import stringToObj
from chain_utils import get_blocks,append_block
from Block import Block

semaphore = 1

def get_lock():
	global semaphore
	while semaphore <= 0:
		pass
	semaphore = semaphore - 1

def release_lock():
	global semaphore
	semaphore = semaphore + 1

class Chain:
	def __init__(self):
		print "init"
		if len(get_blocks()) == 0:
			self.append(self.gen_genesis_block())

	def append(self, block):
		append_block(block)

	def gen_genesis_block(self):
		print"here"
		B = Block()
		B.pow()
		return B