#!/usr/bin/python3

from lxml import html
import untangle
import requests
import string
import json
import os
import re

class SpecParser(object):

	cgl_categories = {
		'AVL': 'availability',
		'CFH': 'cluster',
		'CSM': 'cluster',
		'CCM': 'cluster',
		'CAF': 'cluster',
		'CCON': 'cluster',
		'CDIAG': 'cluster',
		'SMM': 'serviceability',
		'SFA': 'serviceability',
		'SPM': 'serviceability',
		'PRF': 'performance',
		'STD': 'standard',
		'SEC': 'security',
		'PMT': 'hardware',
		'PMS': 'hardware'}

	agl_layers = {
		'3': 'app',
		'4': 'framework',
		'5': 'os',
		'6': 'security',
		'7': 'services'}

	cgl_target = "https://wiki.linuxfoundation.org/en/Carrier_Grade_Linux/CGL_Requirements"

	database_path = "../database/"

	@classmethod
	def parse_cgl(cls, force=False):
		cache_incomplete = False
		base_path = cls.database_path + 'cgl/'
		if not force:
			for cat_id, cat_name in cls.cgl_categories.items():
				if not os.path.exists(base_path + cat_name + '/'):
					cache_incomplete = True
					break
				else:
					print(base_path + cat_name, "\t[ OK ]")
			if not cache_incomplete:
				return
		print("Parsing CGL...")
		page = requests.get(cls.cgl_target)
		tree = html.fromstring(page.content)
		reqs = tree.xpath('//h3/span/text()')
		reqs = list(filter(lambda x: x[0:3] in cls.cgl_categories.keys(), reqs[:-2]))
		req_ids = []
		req_names = []
		for x in reqs:
			fields = x.split()
			if len(fields) >= 2:
				req_ids.append(fields[0])
				req_names.append(x[len(fields[0])+1:])
			else:
				req_ids.append(fields[0])
				req_names.append("")
		req_priorities = tree.xpath('//h3/following-sibling::p[1]/text()')
		req_priorities = [x.strip() for x in req_priorities]
		# this is buggy and wrong, some requirements have longer description than one
		# paragraph, try to grab all of it
		req_descriptions = tree.xpath('//h3/following-sibling::p[2]/text()')
		req_descriptions = [x.strip() for x in req_descriptions]
		cls.__generate_cgl_spec(req_ids, req_names, req_priorities, req_descriptions)
		print("CGL parse complete!")

	@classmethod
	def __generate_cgl_spec(cls, ids, names, prs, descr):
		print("lens: ", len(ids), len(names), len(prs), len(descr))
		base_path = cls.database_path + 'cgl/'
		for cat_id, cat_name in cls.cgl_categories.items():
			os.makedirs(base_path + cat_name, exist_ok=True)
		for i in range(len(ids)):
			file_path = base_path + cls.cgl_categories[ids[i][0:3]] + '/' + ids[i] + '.json'
			new_req = {}
			new_req['id'] = ids[i]
			new_req['name'] = names[i]
			new_req['priority'] = prs[i]
			new_req['description'] = descr[i]
			new_req['category'] = cls.cgl_categories[ids[i][0:3]]
			new_req['spec'] = "CGL"
			new_req['dependencies'] = []
			new_req['type'] = ""
			with open(file_path, 'w+') as req_file:
				json.dump(new_req, req_file, sort_keys=True, indent=4)

	@classmethod
	def parse_agl(cls):
		base_path = cls.database_path + 'agl/'
		""" check if file exists <<<<<<<<<<<<<<<<<<<< """
		spec_path = base_path + "agl.xml"
		for cat_id, cat_name in cls.agl_layers.items():
			os.makedirs(base_path + cat_name, exist_ok=True)
		print("Parsing AGL...")
		obj = untangle.parse(spec_path)
		spec_list = obj.root.children
		cls.__generate_agl_spec(spec_list)
		print("AGL parse complete!")

	@classmethod
	def __generate_agl_spec(cls, spec_list):
		base_path = cls.database_path + 'agl/'
		for req in spec_list:
			if req.cdata:
				layer = req.cdata[0]
				new_req = {}
				req_id =  re.findall(r'\d+', req.cdata)[0]
				file_path = base_path + cls.agl_layers[layer] + '/' + "AGL." + req_id + '.json'
				new_req['id'] = req_id
				new_req['name'] = req.cdata[len(req_id):].strip()
				new_req['spec'] = "AGL"
				new_req['description'] = ""
				new_req['dependencies'] = []
				new_req['type'] = ""
				with open(file_path, 'w+') as req_file:
					json.dump(new_req, req_file, sort_keys=True, indent=4)


def main():
	# SpecParser.parse_cgl()
	SpecParser.parse_agl()

if __name__ == '__main__':
	main()
