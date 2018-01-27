blocks = []
CHAIN_DATA = 'chain.json'
DELIMITER = "<<<--EOB-->>>"
from general import stringToObj

def get_blocks(flag = False):
	global  blocks
	if len(blocks) == 0 or flag == True:
		content = ''
		with open(CHAIN_DATA) as f:
			content = f.read()
		# print content
		content = content.replace('\n','') 
		# print content

		content = content.split(DELIMITER)
		# print content

		blocks = []
		print "flag"
		if flag == True:
			print"2222222222222222222222222"
			return content
		else:			
			for block in content:
				if block != "":
					blocks.append(stringToObj(block))
			# need serious testing
	return blocks

def append_block(block):
	print "append"
	with open(CHAIN_DATA, "a") as chain:
		chain.write("%s\n%s\n"%(block.toJSON(),DELIMITER))
