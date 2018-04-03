#!/usr/bin/env python
try:
    next
except NameError:
	def next(*args):
		return getattr(a, 'next')(*args)

class iteropt:
	class StringObj:
		def __init__(self, s):
			self.s = s
		def __str__(self):
			return self.s
# constructor:
	def __init__(self, a = None):
		if not a:
			from sys import argv
			a = iter(argv)
			try: # skip prog name
				next(a)
			except StopIteration:
				a = None
		else:
			a = iter(a)
		self.reset()
		self._arg = None
		self._argsrcs = []
		a and self._argsrcs.append(a)
# private:
	def _shift(self, jump = None):
		ss = self._argsrcs
		while len(ss) > 0:
			s = ss[0]
			try:
				return next(s)
			except StopIteration:
				pass
			ss.pop(0), self.reset()
			if jump:
				break
		return None
# public:
	def reset(self):
		self._plain = None
# public:
	def is_plain(self, *a):
		r = self.get_plain(*a)
		if r is None:
			return None
		self.plain = r
		return True
	def is_bool(self, *a):
		#~ say2('is_bool', repr(self), repr(a))
		r = self.get_bool(*a)
		if r is None:
			return None
		self.bool = not not r.value
		self.name = r.name
		return True
	def is_true(self, *a):
		if not self.is_bool(*a):
			return None
		elif not self.bool:
			raise RuntimeError('Unexpected false boolean for: ' + self.name)
		return True
	def is_string(self, *a):
		r = self.get_value(*a)
		if r is None:
			return None
		self.string = r.value
		self.name = r.name
		return True
	def is_integer(self, *a):
		r = self.get_value(*a)
		if r is None:
			return None
		self.integer = int(r.value)
		self.name = r.name
		return True
	def is_float(self, *a):
		r = self.get_value(*a)
		if r is None:
			return None
		self.float = float(r.value)
		self.name = r.name
		return True
# public:
	def is_plain_form(self):
		return self._plain and self._arg and (not hasattr(self._arg, 's'))
	def is_long_form(self):
		return self._arg and hasattr(self._arg, 's') and (not hasattr(self._arg, 'bundle'))
	def is_short_form(self):
		return self._arg and hasattr(self._arg, 's') and hasattr(self._arg, 'bundle')
	def is_valid(self):
		return self._arg and True
# private:
	def _get_p(self, *args):
		r = self._arg
		if args and (r not in args):
			return None
		self._arg = None
		return r
	def _get_d_b(self, *args):
		#~ say2('_get_d_b', repr(self), repr(args))
		r = self._arg
		if r.name2 in args:
			r.index += 1
			(r.name, r.value) = (r.name2, True)
			if r.index < len(r.bundle):
				(r.name2, r.proceed)  = (r.bundle[ r.index ], True)
			else:
				self._arg = None
			return r
		return None
	def _get_d_v(self, *args):
		r = self._arg
		if r.name2 in args:
			r.index += 1
			#~ raise ValueError(str(self._arg))
			r.value = (r.index < len(r.bundle)) and r.bundle[ self._arg.index : ] or self._shift()
			if r.value is not None:
				(r.name, self._arg) = (r.name2, None)
			return r
		return None
	def _get_dd_v(self, *args):
		key = self._arg.name2
		for name in args:
			if key == name:
				self._arg.name = name
				self._arg.value = self._shift()
				if self._arg.value is not None:
					key = self._arg
					self._arg = None
					return key
				raise ValueError(str(self._arg))
		return None
	def _get_dde_v(self, *args):
		key = self._arg.name
		for name in args:
			if key == name:
				key = self._arg
				self._arg = None
				return key
		return None
	def _get_dd_b(self, *args):
		key = self._arg.name
		for name in args:
			if key == name:
				key = self._arg
				self._arg = None
				return key
		return None
# public:
	def next(self):
		m = None
		if self._arg is not None:
			if getattr(self._arg, 'proceed', None):
				self._arg.proceed = None
				return 1
			else:
				raise RuntimeError('Invalid argument: ' + str(self._arg))
		self.get_value = lambda *a: None
		self.get_bool = lambda *a: None
		self.get_plain = lambda *a: None
		for _ in ('plain','bool','string','integer','float','name'):
			hasattr(self, _) and delattr(self, _)

		self._arg = self._shift(True)
		if self._arg is None:
			return None
		elif self._plain or ('-' == self._arg):
			pass
		elif ('--' == self._arg):
			self._plain = True
			self._arg = self._shift()
			if self._arg is None:
				return None
		elif self._arg.startswith('--') and ('=' in self._arg):
			m = self._arg
			self._arg = self.StringObj(m)
			m = m.split('=', 2)
			self._arg.name = m[0][2:]
			self._arg.value = m[1]
			self.get_value = self._get_dde_v
			return True
		elif self._arg.startswith('--'):
			m = self._arg
			self._arg = self.StringObj(m)
			m = m[2:]
			self._arg.name2 = m
			if m.startswith('no-'):
				self._arg.name = m[3:]
				self._arg.value = False
			elif m.startswith('no'):
				self._arg.name = m[2:]
				self._arg.value = False
			else:
				self._arg.name = m
				self._arg.value = True
			self.get_value = self._get_dd_v
			self.get_bool = self._get_dd_b
			return True
		elif self._arg.startswith('-'):
			m = self._arg
			self._arg = self.StringObj(m)
			m = m[1:]
			self._arg.bundle = m
			self._arg.index = 0
			self._arg.name2 = m[ self._arg.index ]
			self.get_value = self._get_d_v
			self.get_bool = self._get_d_b
			return True
		self.get_plain = self._get_p
		return True

class Download(object):
	def __getattr__(self, name):
		if False:
			pass
		elif name == 'logPath':
			import os
			self.__dict__[name] = os.path.join(self.dirRoot, 'logs')
		elif name == 'dirRoot':
			import os
			home = os.environ.get('HOME')
			self.__dict__[name] = os.path.join(home, '.dbu')
		elif name == 'log':
			import os
			p = self.logPath
			d = os.path.dirname(p)
			if not os.path.exists(d):
				os.makedirs(d)
			self.__dict__[name] = open(p, "a")
		else:
			raise AttributeError(name)
		return self.__dict__[name]
	def fetch(self, url):
		import os
		f = self.urlPath(url)
		if os.path.exists(f):
			self.log.write("FND %s %s\n" % (f, url))
			return
		else:
			d = os.path.dirname(f)
			os.path.exists(d) or os.makedirs(d)
		t = f + ".tmp"
		import requests
		try:
			r = requests.get(url, allow_redirects=True, stream=True)
			self.log.write("%03d %s %s\n" % (r.status_code, f, url))
			if r.status_code == 200:
				with open(t, 'wb') as fd:
					for chunk in r.iter_content(chunk_size=1024*1024):
						fd.write(chunk)
				os.rename(t, f)
		except:
			self.log.write("EXC %s %s\n" % (f, url))
	def urlPath(self, url):
		import os
		from hashlib import md5
		h = md5()
		h.update(url.encode("UTF-8"))
		h = h.hexdigest()
		a = h[0:2]
		b = h[2:]
		return os.path.join(self.dirRoot, a, b)
	def pathOf(self, url):
		f = self.urlPath(url)
		return os.path.exists(f) or f


def main(opt):
	args = []
	dlr = Download()
	urlLists = None
	while opt.next():
		if False:
			pass
		elif opt.is_plain():
			args.append(opt.plain)
		elif opt.is_string('l', 'log'):
			dlr.logPath = opt.string
		elif opt.is_string('r', 'root'):
			dlr.dirRoot = opt.string
		elif opt.is_string('i', 'urls'):
			urlLists = opt.string
	def eachu():
		inp = None
		if not urlLists:
			pass
		elif urlLists == '-':
			from sys import stdin
			inp = stdin
		else:
			inp = open(urlLists, 'r')
		if inp:
			with inp:
				for l in inp:
					l = l.strip()
					if (not l) or l.startswith('#'):
						continue
					else:
						yield l
		for l in args:
			yield l
	for u in eachu():
		dlr.fetch(u)

if __name__ == "__main__":
	main(iteropt())

r"""
( pushd /mnt/META/wrx/python/fbpdl ; make .build/dbu.src )
"https://z-m-scontent.fmnl4-4.fna.fbcdn.net/v/t39.2081-6/c0.0.76.76/p75x75/16781258_1055311757946376_5073889426497601536_n.png?_nc_cat=0&_nc_ad=z-m&_nc_cid=1066&oh=38423a1e4966f6574cfe2612d5673179&oe=5B32B14E"
"""
