"""bagile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.admin import site as admin_site
from django.contrib.auth import views as auth_views


def home(request):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    return render_to_response('home.html', context=RequestContext(request))

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^admin/', admin_site.urls),
    url('^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url('^logout/', auth_views.logout, {'template_name': 'logout.html'}),
    url(r'^scrumboard/', include('scrumboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,  document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,   document_root=settings.MEDIA_ROOT)
