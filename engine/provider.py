class Provider(object):

	def __init__(self, ptype=None):
		self.provider_type = ptype

	@classmethod
	def get_logs(cls, ptype):
		ptype = ptype.strip().lower()
		if ptype == 'ltp':
			pass
		elif ptype == 'lynis':
			pass
		elif ptype == 'imgtst':
			pass
		elif ptype == 'phoronix':
			pass
		elif ptype == 'lltng':
			pass
		else:
			pass # handle standalone tests

	@classmethod
	def get_runscript(cls, ptype):
		ptype = ptype.strip().lower()
		if ptype == 'ltp':
			pass
		elif ptype == 'lynis':
			pass
		elif ptype == 'imgtst':
			pass
		elif ptype == 'phoronix':
			pass
		elif ptype == 'lltng':
			pass
		else:
			pass # handle standalone tests