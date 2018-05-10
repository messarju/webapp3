from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
	try:
		from django.conf import settings
		settings.DEFAULT_CONTENT_TYPE = "image/png"
		REQ = request.POST or request.GET
		_ = REQ.get('_')
		if _:
			return getattr(__import__(__package__, fromlist=[_,]), _).index(request)
		raise RuntimeError("No command")
	except:
		from traceback import format_exc
		return HttpResponse(format_exc(), status=500)
