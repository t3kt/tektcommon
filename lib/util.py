
print('core util.py initializing')

def dumpobj(obj, underscores=False, methods=False):
	print('Dump ' + repr(obj) + ' type:' + repr(type(obj)))
	if isinstance(obj, (list, tuple)):
		for i in range(len(obj)):
			print('  [' + str(i) + ']: ' + repr(obj[i]))
	else:
		for key in dir(obj):
			if key.startswith('_') and not underscores:
				continue
			try:
				val = getattr(obj, key)
			except Exception as e:
				print('  ' + key + ': [ERROR]', e)
				continue
			if callable(val) and not methods:
				continue
			print('  ' + key + ': ' + repr(val))


def setattrs(obj, **attrs):
	if isinstance(obj, (tuple, list)):
		for o in obj:
			setattrs(o, **attrs)
	else:
		for key in attrs:
			setattr(obj, key, attrs[key])

def _ProcessClones(master, action, predicate=None):
	if not master or not hasattr(master, 'clones'):
		return
	for c in master.clones:
		if predicate is not None and not predicate(c):
			continue
		action(c)

def DumpClones(master, predicate=None):
	print('Clones of ' + master.path)
	_ProcessClones(master, lambda c: print('  ' + c.path), predicate=predicate)

_EXPORTS = {
	'dumpobj': dumpobj,
	'setattrs': setattrs,
	'DumpClones': DumpClones,
}

def EXPORT(console_locals):
	"""Export utility functions to the console.
	Usage: op.core.mod.core_utils.EXPORT(locals())
	:param console_locals: dict of local variables to export into
	"""
	console_locals.update(_EXPORTS)
