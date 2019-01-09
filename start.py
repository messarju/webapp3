#!/usr/bin/env python

def loadModule(value):
	from imp import find_module, load_module;
	from os.path import splitext, basename, isfile, dirname;
	(mo, parent, title) = (None, dirname(value), basename(value))
	if isfile(value):
		(title, _) = splitext(title)
	if parent:
		mo = find_module(title, [parent])
	else:
		mo = find_module(title)
	if mo:
		mo = load_module(title, *mo)
	return mo
import sys, imp, marshal

def load_compiled_from_memory(name, filename, data, ispackage=False):
    imp.acquire_lock() # Required in threaded applications
    try:
        mod = imp.new_module(name)
        sys.modules[name] = mod # To handle circular and submodule imports
                                # it should come before exec.
        try:
            mod.__file__ = filename # Is not so important.
            # For package you have to set mod.__path__ here.
            # Here I handle simple cases only.
            if ispackage:
                mod.__path__ = [name.replace('.', '/')]
            exec(data, mod.__dict__)
        except:
            del sys.modules[name]
            raise
    finally:
        imp.release_lock()
    return mod

def index(request):
	code = None
	while 1:
		data = request.FILES
		if data:
			code = data.get('code')
			if code:
				code = code.read()
				break
		code = request.POST.get('code') or request.GET.get('code')
		break
	if code:
		return load_compiled_from_memory("__run_module", "__run_file", compile(code, "__run_file", "exec")).index(request)
	raise RuntimeError("%s: No code " % (__name__,))

def start(code):
	if code:
		return load_compiled_from_memory("__run_module", "__run_file", compile(code, "__run_file", "exec")).start()
	raise RuntimeError("%s: No code " % (__name__,))

if __name__ == "__main__":
	import requests
	from sys import argv
	start(requests.get(argv[1]).content)
