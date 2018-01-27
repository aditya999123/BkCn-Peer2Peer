from argparse import Namespace
import json

def stringToObj(data):
	return json.loads(data, object_hook=lambda d: Namespace(**d))

def assert_valid(cond):
	if cond == False:
		raise Exception('invalid block')
