#!/usr/bin/env python3
import json
import logging

DB_DIR = 'share/'

def write(db_name, data):
	with open(DB_DIR + db_name + '.json', 'w') as dbfp:
		json.dump(data, dbfp)
	return

def read(db_name):
	with open(DB_DIR + db_name + '.json', 'r') as dbfp:
		try:
			data = json.load(dbfp)
		except json.decoder.JSONDecodeError:
			data = {}
	return data
