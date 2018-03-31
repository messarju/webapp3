from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def cmd(r):
	try:
		g = r.POST or r.GET
		o = {}
		detached=None
		stdin=None
		shell=None


		return HttpResponse('No URL', content_type="image/png")
	except:
		from traceback import format_exc
		return HttpResponse(format_exc(), status=500, content_type="image/png")



