from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def _readb(f, w):
	with open(u, 'rb') as f:
		if w:
			n = w[1] - w[0] + 1
			f.seek(w[0])
			return f.read(n)
		else:
			return f.read()

def _add_hash(f, n, h):
	if n == 'md5':
		from hashlib import md5
		d = md5()
		with open(f, 'rb') as f:
			r = f.read(1024*1024)
			while r:
				d.update(r)
				r = f.read(1024*1024)
			h['Hash'] = d.hexdigest()

def E404(x):
	return HttpResponse("Not found %r" % x, content_type='image/png', status=404)

@csrf_exempt
def echo(r):
	try:
		import requests, os
		g = r.POST or r.GET
		body = g.get('body')
		if body:
			body = json.loads(body)
			return supply(body)
		u = g.get('u')
		if u:
			a = g.get('a')
			if u.startswith("file://"):
				p = u[7:]
				if os.path.exists(p):
					_ = _readb(p, a and [int(a), int(g.get('b'))])
					return HttpResponse(_, content_type=g.get('t', 'image/png'))
				else:
					return E404(p)
			cache = g.get('cache')
			if cache in ('check', 'use'):
				from . import dbu
				p = dbu.Download().urlPath(u)
				if os.path.exists(p):
					_ = _readb(p, a and [int(a), int(g.get('b'))])
					open('cache.log', 'a').write("HIT %s %s\n" % (p, a))
					return HttpResponse(_, content_type=g.get('t', 'image/png'))
				elif cache == 'use':
					return E404(p)
			if a:
				b = g.get('b')
				r = requests.get(u, headers={'Range': 'bytes=%s-%s' % (a, b)})
			else:
				r = requests.get(u)
			return HttpResponse(r, content_type=g.get('t', 'image/png'), status=r.status_code)
		u = g.get('h')
		if u:
			h = None
			while 1:
				if u.startswith("file://"):
					p = u[7:]
					if not os.path.exists(p):
						return E404(p)
					h = {'Accept-Ranges': 'bytes', 'Content-Length' : os.stat(p).st_size}
					_ = g.get('hash')
					_ and _add_hash(p, _, h)
					break
				cache = g.get('cache')
				if cache in ('check', 'use'):
					from . import dbu
					p = dbu.Download().urlPath(u)
					if os.path.exists(p):
						import os
						h = {'Accept-Ranges': 'bytes', 'Content-Length' : os.stat(p).st_size}
						_ = g.get('hash')
						_ and _add_hash(p, _, h)
						open('cache.log', 'a').write("HED %s %s\n" % (p, h['Content-Length']))
						break
					elif cache == 'use':
						return E404(p)
				h = requests.head(u, allow_redirects=True).headers
				break
			if h:
				return HttpResponse("\n".join(["%s: %s" % (k, h[k]) for k in h]), content_type=g.get('t', 'image/png'))
			return HttpResponse('No headers', content_type="image/png")
		p = g.get('l')
		if p:
			if os.path.exists(p):
				a = g.get('a')
				_ = _readb(p, a and [int(a), int(g.get('b'))])
				return HttpResponse(_, content_type=g.get('t', 'image/png'))
			else:
				return E404(p)
		sub = g.get('_')
		if not sub:
			pass
		elif sub == 'cache_urls':
			v = r.FILES
			if v:
				v = v.get('urls')
				if v:
					from . import dbu
					dlr = dbu.Download()
					for l in v:
					    dlr.fetch(l.strip())
			return HttpResponse('OK', content_type="image/png")
		return HttpResponse('No URL', content_type="image/png", status=400)
	except:
		from traceback import format_exc
		return HttpResponse(format_exc(), status=500, content_type="image/png")
