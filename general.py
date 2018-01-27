from argparse import Namespace
import json

def stringToObj(data):
	return json.loads(data, object_hook=lambda d: Namespace(**d))

def assert_valid(cond, message=None):
	if cond == False:
		print "msg: ", message
		raise Exception('invalid block')
