"""bootcamp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from abcd import views

urlpatterns = [
	path('admin/', admin.site.urls),
	url(r'^bootcamp/	',views.Home),
	url(r'^login',views.Login),
	url(r'^signup',views.Signup),
	url(r'^dashboard/',views.Dashboard),
	url(r'^home/',views.Home),
   
	url(r'^track_user/$', views.track_user, name='track_user'),
	url(r'^feed',views.Feed),
	url(r'^article',views.Article),
	url(r'^comment_post',views.comment_post),
	url(r'^logout',views.Logout),
	url(r'^query',views.query)
	]
