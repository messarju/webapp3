from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def echo(r):
	try:
		g = r.POST or r.GET
		body = g.get('body')
		if body:
			body = json.loads(body)
			return supply(body)
		u = g.get('u')
		if u:
			a = g.get('a')
			while 1:
				if u.startswith("file://"):
					import os
					u = u[7:]
					if a:
						a = int(a)
						b = int(g.get('b'))
						with open(u, 'rb') as f:
							n = b - a + 1
							f.seek(a)
							r = f.read(n)
					else:
						with open(u, 'rb') as f:
							r = f.read()
					break
				if ('check_cache' in g):
					p = get_url_cache_path('.dbu', u)
					if p:
						if a:
							a = int(a)
							b = int(g.get('b'))
							with open(p, 'rb') as f:
								n = b - a + 1
								f.seek(a)
								r = f.read(n)
						else:
							with open(p, 'rb') as f:
								r = f.read()
						break
				if a:
					b = g.get('b')
					r = requests.get(u, headers={'Range': 'bytes=%s-%s' % (a, b)})
				else:
					r = requests.get(u)
				break
			return HttpResponse(r, content_type=(g.get('t') or 'image/png'))
		u = g.get('h')
		if u:
			h = None
			while 1:
				if u.startswith("file://"):
					import os
					u = u[7:]
					h = {'Accept-Ranges': 'bytes', 'Content-Length' : os.stat(u).st_size}
					if g.get('hash') == 'md5':
						from hashlib import md5
						d = md5()
						with open(u, 'rb') as f:
							r = f.read(1024*1024)
							while r:
								d.update(r)
								r = f.read(1024*1024)
							h['Hash'] = d.hexdigest()
					break
				if ('check_cache' in g):
					p = get_url_cache_path('.dbu', u)
					if p:
						import os
						h = {'Accept-Ranges': 'bytes', 'Content-Length' : os.stat(p).st_size}
						if g.get('hash') == 'md5':
							from hashlib import md5
							d = md5()
							with open(p, 'rb') as f:
								r = f.read(1024*1024)
								while r:
									d.update(r)
									r = f.read(1024*1024)
								h['Hash'] = d.hexdigest()
						break
				h = requests.head(u, allow_redirects=True).headers
				break
			if h:
				return HttpResponse("\n".join(["%s: %s" % (k, h[k]) for k in h]), content_type=(g.get('t') or 'image/png'))
			return HttpResponse('No headers', content_type="image/png")
		u = g.get('l')
		if u:
			a = g.get('a')
			t = g.get('t')
			if a:
				a = int(a)
				import os
				s = os.stat(u).st_size
				assert (s >= 0)
				b = int(g.get('b'))
				b = min(b, s - 1)
				assert (b >= 0)
				assert (b > a)
				with open(u, 'rb') as o:
					n = (b - a) + 1
					o.seek(a)
					r = o.read(n)
			else:
				o = open(u, 'rb')
				r = o.read()
				o.close()
			return HttpResponse(r, content_type=(t or 'image/png'))
		return HttpResponse('No URL', content_type="image/png")
	except:
		from traceback import format_exc
		return HttpResponse(format_exc(), status=500, content_type="image/png")



