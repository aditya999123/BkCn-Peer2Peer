import ecdsa, hashlib
from chain_utils import get_blocks

txnBuffer = []

class Transaction:
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def __init__(self, sender_public_key, reciever_public_key, product_hash, hashed):
		self.sender_public_key = sender_public_key
		self.reciever_public_key = reciever_public_key
		self.product_hash = product_hash
		self.hashed = hashed
		self.authenticated = self.authenticate(sender_public_key, reciever_public_key, product_hash, hashed)

		self.validated, owner = self.validate(self.sender_public_key, self.reciever_public_key, self.product_hash)

		if sender_public_key == reciever_public_key and owner == None and self.validated == False:
			self.validated = True

	def authenticate(self, sender_public_key, reciever_public_key, product_hash, hashed):
		vk = ecdsa.VerifyingKey.from_string(sender_public_key.decode('hex'), curve=ecdsa.SECP256k1)
		return vk.verify(hashed.decode('hex'), sender_public_key + reciever_public_key + product_hash)

	def validate(self, sender_public_key, reciever_public_key, product_hash):
		owner = None
		for block in get_blocks():
			for txn in block.txns:
				if(txn.product_hash == product_hash):
					owner = txn.reciever_public_key
		if(owner != None and owner == sender_public_key and sender_public_key != reciever_public_key):
			return True, owner
		return False, owner