from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

from hello import views, echo

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^echo', echo.echo, name='echo'),
    url(r'^lave', views.lave, name='lave'),
    url(r'^inb', views.inb, name='inb'),
    url(r'^db', views.db, name='db'),
    path('admin/', admin.site.urls),
]
