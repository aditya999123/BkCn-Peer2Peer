import ecdsa, hashlib

txnBuffer = []

class Txn:
	def __init__(self, senderPublicKey, recieverPublicKey, product, txnHash):
		self.sender = senderPublicKey
		self.reciever = recieverPublicKey
		self.product = product
		self.txnHash = txnHash
		self.nonce = None

		self.authenticated = self.authenticate(senderPublicKey, recieverPublicKey, txnHash)
		self.validated = self.validate(self.sender, self.product)

	def authenticate(senderPubKey, recieverPubKey, hashed):
		vk = ecdsa.VerifyingKey.from_string(senderPubKey.decode('hex'), curve=ecdsa.SECP256k1)
		return vk.verify(hashed.decode('hex'), senderPubKey + recieverPubKey)

	def validate(sender, product):
		owner = {}
		for block in chain.blocks:
			for txn in block.txns:
				if(txn.product == product):
					owner = txn.reciever
		if(owner == sender):
			return True
		return False