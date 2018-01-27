CHAIN_DATA = 'chain.json'
DELIMITER = "<<<--EOB-->>>"

class Chain:
	def __init__(self):
		self.blocks = self.get_blocks()
		if len(self.blocks) == 0:
			self.append_block(self.gen_genesis_block())

	def get_blocks(self):
		content = ''
		with open(CHAIN_DATA) as f:
			content = f.readlines()
		content = [x.strip() for x in content] 
		content = content.join('').split(DELIMITER)

		blocks = []
		for block in content:
			blocks.append(json.loads(block))

		return blocks

	def append_block(self, block):
		self.blocks.append(block)
		with open(CHAIN_DATA, "a") as chain:
			chain.write("%s\n%s\n"%(block.toJSON(),DELIMITER))


	def gen_genesis_block(self):
		