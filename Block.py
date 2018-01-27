import hashlib
import time
from Transaction import Transaction

def assert_valid(cond):
	if cond == False:
		raise Exception('invalid block')

class Block:
	def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

	def __init__(self, txns = [], previous_block = None):
		self.txns = txns
		if previous_block is not None:
			self.previous_block_hash = previous_block.hashed
			self.block_number = previous_block.block_number + 1
		else :
			self.previous_block_hash = self.gen_hash('genesis')
			self.block_number = 0
		self.time = time.time.now()
	
	def generate_txns_hash(self, block=None):
		if block is not None:
			return hashlib.sha256(block.toJSON()).digest().encode('hex')
		
		return hashlib.sha256(self.toJSON()).digest().encode('hex')

	def pow(self):
		self.hashed = self.generate_txns_hash()
		self.pow = ''
		nonce = -1
		while self.pow[:4] != '0000':
			nonce = nonce + 1
			self.pow = hashlib.sha256(self.hashed + str(nonce)).digest().encode('hex')
		self.nonce = nonce

	def gen_hash(self, *args):
		init = ''
		for arg in args:
			init = init + str(arg)

		return hashlib.sha256(init).digest().encode('hex')

	def validate(block, previous_block):
		try:
			assert_valid(previous_block.hashed == block.previous_block_hash)
			assert_valid(previous_block.block_number == block.block_number + 1)
			for txn in block.txns:
				nTxn = Transaction(txn.senderPublicKey, txn.recieverPublicKey, txn.product, txn.txnHash)
				assert_valid(nTxn.authenticated)
				assert_valid(nTxn.validated)
			assert_valid(self.generate_txns_hash(block) == block.hashed)
			assert_valid(self.gen_hash(block.hashed, block.nonce) == block.pow)

			return True
		except Exception as e:
			print str(e)
			return False
