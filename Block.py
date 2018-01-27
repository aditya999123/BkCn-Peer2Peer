from general import assert_valid
from Transaction import Transaction
import hashlib, datetime, json

block_size = 2

class Block:
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def __init__(self, txns = [], previous_block = None):
		self.txns = txns
		if previous_block is not None:
			self.previous_block_hash = previous_block.hashed
			self.block_number = previous_block.block_number + 1
		else :
			self.previous_block_hash = self.gen_hash('genesis')
			self.block_number = 0
		self.time = str(datetime.datetime.now())
	
	def generate_txns_hash(self, block=None):
		if block is None:
			block = self

		to_be_hashed = {
			"txns":str(block.txns),
			"time":block.time,
			"block_number":block.block_number,
			"previous_block_hash":block.previous_block_hash
		}
		
		to_be_hashed = json.dumps(to_be_hashed)
		return hashlib.sha256(to_be_hashed).digest().encode('hex')

	def pow(self):
		hashed = self.generate_txns_hash()
		self.hashed = hashed
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

	def validate(self, block, previous_block):
		try:
			assert_valid(previous_block.hashed == block.previous_block_hash, "prv bloc hash")
			assert_valid(previous_block.block_number + 1 == block.block_number, "block num")
			for txn in block.txns:
				nTxn = Transaction(txn.sender_public_key, txn.reciever_public_key, txn.product_hash, txn.hashed)
				assert_valid(nTxn.authenticated, "auth")
				assert_valid(nTxn.validated, "valid")
			assert_valid(self.generate_txns_hash(block) == block.hashed, "hash")
			assert_valid(self.gen_hash(block.hashed, block.nonce) == block.pow, "pow")

			return True
		except Exception as e:
			print str(e)
			return False
