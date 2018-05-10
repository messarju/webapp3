from django.http import HttpResponse

def index(request):
	from requests import head
	REQ = request.POST or request.GET
	url = REQ.get('url')
	if not url:
		raise RuntimeError("%s: No URL " % (__name__,))
	h = head(url, allow_redirects=True).headers
	return HttpResponse("\n".join(["%s: %s" % (k, h[k]) for k in h]))
